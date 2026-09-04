# Triage pack — PROP · Prairie Operating Co.

_Generated 2026-09-04 16:12 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** PROP · **Name:** Prairie Operating Co.
- **CIK:** 0001162896
- **SIC:** 1311 — Crude Petroleum & Natural Gas
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/PROP

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Prairie Operating Co.
- **CIK:** 1,162,896 · **SIC:** 1311 (Crude Petroleum & Natural Gas) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermLineOfCredit

> **EARNINGS QUALITY FLAG — one-off items likely.**
> revenue growth above 50% alongside share count growth above 15% (bought, not organic).
> Reported net income is not supported by the operating engine that is supposed to produce it (typical causes: gains on sale, legal settlements, deferred-tax valuation-allowance releases, bargain-purchase gains). Reconcile net income to operating income in the earnings release (section 7) before treating any earnings-based metric here as repeatable.

**Valuation**

| metric | value |
|---|---|
| price | 0.47 |
| mktcap | $53.1M |
| ev | $489.1M |
| ev_ebit | 7.5x |
| fcf | $153.9M |
| fcf_yield | 289.7% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 7.9% |
| net_debt | $436.0M |
| net_debt_ebit | 6.6x |
| cash | $21k |
| ltd | $436.0M |
| equity | $223.0M |
| ltd_tag | LongTermLineOfCredit |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $241.6M |
| revenue_prior | $7.9M |
| rev_growth | 2,943.8% |
| rev_growth_note | share count +124.3% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | revenue growth above 50% alongside share count growth above 15% (bought, not organic) |
| ebit | $65.6M |
| net_income | $32.1M |
| cfo | $153.9M |
| capex | n/a |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 124.3% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 112,798,010 |
| shares_py | 50,277,744 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -67.6% |
| r6m | -70.6% |
| off_52w_high | -81.2% |
| adv20 | $1.8M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 1.00 |
| r_ev_ebit | 0.85 |
| r_roic | 0.64 |
| r_rev_growth | 1.00 |
| r_buyback | 0.01 |
| score | 0.60 |

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
| rank | 145 |

**Screen rationale:** top-quartile FCF yield 289.7%; cheap at 7.5x EV/EBIT; revenue +2943.8% BUT share count +124.3% yoy — growth may be acquisition/issuance-driven, not organic; EARNINGS QUALITY: revenue growth above 50% alongside share count growth above 15% (bought, not organic) — one-off items likely; WARNING 6m return below -40%


## 3. Share count trend

- Shares outstanding: **112,798,010** (CY2026Q2I) vs **50,277,744** prior year (CY2025Q2I)
- Change: **124.3%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`
- **Flag:** share count +124.3% yoy — growth may be acquisition/issuance-driven, not organic

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-31** — Item 1.01 (Entry into a Material Definitive Agreement): On August 30, 2026, the Company entered into a letter agreement (the "Letter Agreement") with Hudson Bay PH XIX LLC ("High Trail"),
- **2026-08-17** — Item 1.01 (Entry into a Material Definitive Agreement): On August 14, 2026, Prairie Operating Co. (the "Company") entered into a Third Amendment to Amended and Restated Credit Agreement
- **2026-08-10** — Item 1.01 (Entry into a Material Definitive Agreement): On August 7, 2026, Prairie Operating Co. (the "Company") entered into a letter agreement (the "Letter Agreement") with
- **2026-07-22** — Item 5.02 (officer / director change or comp arrangement): Departure of Directors or Certain Officers; Election of Directors; Appointment of Certain Officers; Compensatory Arrangements of Certain Officers.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 91,425 sh / $79,858 vs sells 0 sh / $0 -> net $79,858 (BUYING).
Distinct insiders buying (code P): 2. Largest buy: Frommer Richard N. bought 75,500 sh @ $0.87 ($65,685) on 2026-05-19.

Form 4 filings parsed: 12; transaction rows: 18 (open-market buys 2, sales 0).

| code | rows |
|---|---|
| A | 7 |
| F | 5 |
| J | 4 |
| P | 2 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-17_2-02-results.md)

_Extraction: started at the first release heading, 'Second Quarter 2026 Results Summary'; skipped 10 forward-looking-statement block(s); 5 block(s) of pre-heading matter dropped._

## EX-99.1 - EXHIBIT 99.1 (ef20079578_ex99-1.htm)

Second Quarter 2026 Results Summary

• | Produced 2.0 MMBoe, or approximately 21,866 Boe/d, with 72% liquids (50% oil).

• | Revenue of $98.9 million, an increase of approximately 45% year-over-year.

• | Reported net income attributable to Prairie Operating Co. common stockholders of $193.8 million, or $1.75 basic earnings per share and $0.23 diluted earnings per share.

• | Generated Adjusted EBITDA (1) of $34.0 million.

• | Capital expenditures of $98.5 million.

• | Net cash provided by operating activities of $52.0 million.

Key Highlights for Year-to-Date 2026

• | Total production of 4.1 MMBoe, or approximately 22,500 Boe/d, with 72% liquids (49% oil).

• | Daily production of approximately 27,000 Boe/d throughout the month of August.

• | Total revenue of $182.3 million, an increase of 125% year-over-year.

• | Adjusted EBITDA (1) of $71.1 million, an increase of 65% year-over-year.

• | Continued execution with recently drilled wells coming in below AFE.

• | Active hedging program, securing commodity price protection through the second quarter of 2029.

• | Executed partial refinancing of the Series F Preferred Stock in April, reducing outstanding balance and significantly lowering warrant-related dilution, while extending the Anniversary warrant date to August 31, 2026.

(1) Adjusted EBITDA is a Non-GAAP measure, refer to "Non-GAAP Financial Measures" for reconciliations of GAAP to non-GAAP financial measures used throughout
this press release.

Greg Patton, Chief Executive Officer, commented:

"Prairie delivered strong operational progress during the second quarter and throughout the first half of 2026. Our team continued to improve
drilling performance, execute within budget and advance our development program across multiple pads in the DJ Basin, despite a planned pause in activity related to seasonal operating restrictions. We also achieved several important technical
milestones, including successfully drilling our first three-mile lateral and testing a new wellbore design that demonstrated meaningful cost savings without changing the completion or production configuration."

"These achievements reflect the continued improvement of our operating capabilities. As we move into the second half of the year, we remain focused on
safe and consistent execution, applying proven efficiencies across our development program and allocating capital to the opportunities that generate the strongest returns. We believe this disciplined approach will support sustainable production
growth, improved capital efficiency and long-term value creation for our shareholders."

Michael Shelly, Executive Vice President and Chief Financial Officer, added:

"Prairie continued to strengthen its financial position and generated meaningful operating cash flow while continuing to fund an active capital
program, expanded our commodity hedge portfolio to provide greater visibility and coverage of our future cash flows and made important progress simplifying our capital structure and reducing potential shareholder dilution."

"As we move through the remainder of the year, our financial priorities remain centered on disciplined capital allocation, building liquidity and
strengthening the balance sheet. We will continue to align capital spending with operating performance, pursue opportunities to enhance financial flexibility and support the Company's development program in a manner designed to generate sustainable
free cash flow through a range of commodity-price environments."

Erik Thoresen, Chairman of the Board, concluded:

"During the second quarter, Prairie took several important steps to strengthen its leadership, governance and financial position. We
added key members to the management team and reinvigorated the Board by welcoming a new director whose experience and perspectives will enhance our oversight and strategic decision-making."

"These actions reflect the Board's commitment to a strong alignment with management and shareholders. Together, we remain focused on disciplined execution,
prudent capital allocation and continued cost improvement, all with the objective of creating sustainable, long-term shareholder value."

Operations Update

Prairie maintained strong drilling execution during the second quarter of 2026, drilling 12 wells, including two Codell and ten Niobrara wells. Eight of
the 12 wells were drilled in a single run, and all wells were completed below AFE. The wells consisted of two-and three-mile laterals and averaged approximately 19,100 feet in measured depth, with an average rate of penetration of 390 feet per hour
and an average spud-to-rig-release time of 6.65 days.

During the quarter, Prairie successfully drilled its first three-mile lateral, a Niobrara B well, in a single run and completed drilling operations at
the Burnett Pad. Drilling operations at the Castor pad were subsequently completed during the first month of the third quarter. Second-quarter drilling activity included a planned pause between the Opal Coalbank and Burnett pads to accommodate
seasonal restrictions associated with Colorado Parks and Wildlife.

On the Castor pad, Prairie completed two successful trials utilizing a 7-7/8-inch hole design, compared with the Company's standard 8-1/2-inch design.
The trials generated realized savings and utilized the same 5-1/2-inch production casing. As such, it does not alter the delivered well configuration for completion or production purposes. Based on these results, Prairie plans to deploy the smaller
hole design across a significant portion of its upcoming Niobrara development program.

Year to date, Prairie has drilled 27 wells, including six Codell and 21 Niobrara wells, with 19 wells drilled in a single run. On average, the wells were
delivered below AFE. Year-to-date wells averaged approximately 18,700 feet in measured depth, an average rate of penetration of 377 feet per hour and an average spud-to-rig-release time of 6.2 days. Prairie has completed drilling operations at the
Elder, Opal Coalbank, Burnett and Castor pads during 2026.

Second Quarter 2026 Results

Key Financial Highlights

(In thousands, except per share amounts) | Three Months Ended June 30, 2026
Total revenues | 98,859
Net income attributable to Prairie Operating Co. common stockholders | 193,794
Earnings per share – basic | 1.75
Earnings per share – diluted | 0.23
Adjusted EBITDA | 34,010
Capital expenditures (1) | 98,489

(1) | Excludes $12.4 million of capital costs included in accounts payable and accrued expenses as of June 30, 2026.

Revenue and Production

Revenue for the second quarter of 2026 was $98.9 million, including $93.5 million related to oil. Production for the second quarter of 2026 totaled
1,990 MBoe, or 21,866 Boe/d, and was comprised of approximately 50% oil and 72% liquids.

Three Months Ended June 30, 2026
Revenues (in thousands)
Oil revenue | 93,458
Natural gas revenue (1) | (4,292
NGL revenue | 9,693
Total revenues | 98,859
Production:
Oil (MBbls) | 992
Natural gas (MMcf) | 3,299
NGL (MBbls) | 448
Total production (MBoe) (2) | 1,990
Average sales volumes per day (Boe/d) | 21,866
Average realized price (excluding effects of derivatives):
Oil (per Bbl) | 94.21
Natural gas (per Mcf) (1) | (1.30
NGL (per Bbl) | 21.64
Average realized price (per Boe) | 49.68
Average sales price (including effects of derivatives):
Oil (per Bbl) | 59.79
Natural gas (per Mcf) (1) | (0.20
NGL (per Bbl) | 16.72
Average price (per Boe) | 33.25
Average NYMEX prices:
WTI (per Bbl) | 84.29
Henry Hub (per MBtu) | 3.81

(1) | For the three months ended June 30, 2026, we realized negative natural gas revenue and average realized prices (excluding and including the effects of derivatives) due to lower gross sales, driven by decreased pricing during the quarter, compared to gathering and processing fees.

(2) | MBoe is calculated using six MMcf of natural gas equivalent to one MBbl of oil.

Operating Costs

For the second quarter of 2026, lease operating expenses were $13.6 million, or $6.85 per Boe; transportation and processing expenses were $2.4
million, or $1.22 per Boe; ad valorem and production taxes were $8.0 million, or $4.01 per Boe; and general and administrative expenses were $12.0 million, or $6.01 per Boe.

(In thousands, except per Boe amounts) | Three Months Ended June 30, 2026
Lease operating expenses | 13,628
Lease operating expenses per Boe | 6.85
Gathering, transportation, and processing | 2,426
Gathering, transportation, and processing per Boe | 1.22
Ad valorem and production taxes | 7,983
Ad valorem and production taxes per Boe | 4.01
General and administrative expenses (1) | 11,952
General and administrative expenses per Boe | 6.01

(1) | General and administrative expenses for the three months ended June 30, 2026, includes non-cash stock-based compensation of $3.3 million, or $1.66 per Boe, and non-recurring litigation and severance settlement expenses of $0.8 million, or $0.41 per Boe.

Liquidity and Capital Resources

As of June 30, 2026, we had a working capital deficit of approximately $125.5 million and availability of $39.0 million under the reserve-based credit agreement with
Citibank, N.A. (the "Credit Facility"). As of June 30, 2026, the Credit Facility had a borrowing base of $475.0 million and aggregate elected commitments of $475.0 million.

During the six months ended June 30, 2026, our cash expenditures for the development of oil and natural gas properties totaled $132.6 million, with an additional $12.4
million incurred in accounts payable and accrued expenses.

On August 14, 2026, we entered into an amendment to our Credit Facility agreement which, among other things, modifies the Current
Ratio covenant requirements for the quarters ended June 30, 2026 through December 31, 2026. Additionally, the amendment includes a new covenant which requires our net monthly production to not fall below an average number specified in the
agreement, which will be measured on a rolling three-month average, beginning September 30, 2026. After giving effect to the amendment, we are in compliance with all covenants under the Credit Facility as of June 30, 2026.

Adjusting 2026 Guidance

Prairie adjusts full-year guidance for 2026 as follows:

• | Average Daily Production: 23,000 – 25,000 Boe/d.

• | Capital Expenditures: $185.0 million – $195.0 million.

• | Adjusted EBITDA (1) : $180.0 million – $190.0 million.

(1) Adjusted EBITDA is a Non-GAAP measure, refer to "Non-GAAP Financial Measures" for reconciliations of GAAP to non-GAAP financial measures used throughout
this press release.

Commodity Hedges

As of June 30, 2026, we had the following outstanding crude oil and natural gas derivative contracts in place, which settle monthly and are indexed to
NYMEX West Texas Intermediate, NYMEX Henry Hub, and Mont Belvieu OPIS, respectively:

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-31_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We are an independent oil and gas company focused on the acquisition and development of crude oil, natural gas, and NGLs. Our assets and operations are strategically located in the oil region of rural Weld County,
Colorado, within the DJ Basin. We believe the DJ Basin to be one of the premier resource plays in the U.S., as Weld County boasts some of the lowest break–even prices in the U.S., and has a long production history which has proven and
consistent results. The productivity of this resource is demonstrated by the integral role that Weld County holds in Colorado's energy economy, having produced approximately 83% of Colorado's oil production to date.

As of December 31, 2025, our assets included approximately 68,000 net leasehold acres in, on and under approximately 98,200 gross acres. We strive to deliver energy in an environmentally efficient manner by
deploying next–generation technology and techniques. In addition to growing production through our drilling operations, we intend to continue growing our business through accretive acquisitions, such as the NRO Acquisition, which closed in
October 2024, the Bayswater Acquisition, which closed in March 2025, the Edge Acquisition, which closed in July 2025, and the Summit and Crown acquisitions, which closed in October 2025, focusing on assets with the following criteria: (i)
producing reserves, with opportunities to add accretive, undeveloped bolt–on acreage; (ii) ample, high rate–of–return inventory of drilling locations that can be developed with cash flow reinvestment; (iii) strong well–level economics; (iv)
liquids–rich assets; and (v) accretive valuation.

Recent Developments

Recent Acquisitions

In July 2025, we entered into an agreement to acquire certain assets from Edge Energy for a total purchase price of $12.5 million, payable in cash subject to certain closing price adjustments. We closed the
Edge Acquisition on July 3, 2025, which included 13 operated wells on approximately 11,300 net acres. We funded the transaction by borrowing under our Credit Facility with Citi. Additionally, the assets we acquired in the Edge Acquisition
include the fully permitted Simpson pad, which we began developing in August 2025, as well as seven other fully permitted locations.

In August 2025, we completed the Third Exok Acquisition, acquiring approximately 5,000 net acres from Exok for $1.6 million.

In October 2025, we entered into agreements to acquire certain assets from Summit and Crown for a total purchase price of $2.3 million payable in cash, subject to certain closing adjustments. The Summit and
Crown Acquisitions included the acquisition of five operated wells on approximately 3,400 net acres.

Bayswater Acquisition and Funding Transactions

On February 6, 2025, we and certain of our subsidiaries entered into a purchase and sale agreement with Bayswater, pursuant to which we and certain of our subsidiaries agreed to acquire the Bayswater Assets from
Bayswater for a purchase price of $602.8 million, subject to certain closing price adjustments.

On March 26, 2025, we entered into our Credit Facility, which amended and restated our existing reserve–based credit agreement with Citi. The Credit Facility provides for a maximum credit commitment of $1.0
billion and is scheduled to mature on March 26, 2029. Further, on March 26, 2025, we issued Common Stock in a public offering, resulting in proceeds of $41.4 million, net of $2.4 million of underwriting discounts and commissions and $3.7
million in issuance fees. Concurrently with the public offering, we issued the Series F Preferred Stock, resulting in approximately $136.1 million of net proceeds, after deducting the advisor fees and offering expenses.

At the closing of the Bayswater Acquisition on March 26, 2025, we (i) paid approximately $482.5 million in cash to Bayswater, $15.0 million of which was deposited in escrow pending the Additional Working Interest
Acquisition, which Bayswater acquired and assigned to us on April 11, 2025, and (ii) issued 3,656,099 shares of our Common Stock to Bayswater. We funded the cash portion of the purchase price for the Bayswater Acquisition with cash on hand,
the proceeds from the issuance of Common Stock and the issuance of the Series F Preferred Stock, and borrowings under our Credit Facility. We completed the final settlement with Bayswater on October 15, 2025, resulting in a final
consideration of $475.6 million. Refer to Liquidity and Capital Resources – Significant Sources of Liquidity below for a further discussion of issuance of the Series F Preferred Stock and Credit
Facility.

Drilling and Completion Activities

On April 1, 2025, we launched the development program at our Rusch pad development in Weld County, which consists of 11 two–mile lateral wells. The Rusch wells came online late in September 2025 with initial
production measured before any deductions for fuel, flare, or vented volumes ("Two–stream") gross production per well of 475 Boe/d.

On April 28, 2025, we announced our plan to begin completions on nine previously drilled but uncompleted wells acquired in the Bayswater Acquisition. Completion activities at the Opal/Coalbank
pad began in May 2025, and the wells came online mid–July 2025 with initial average Two–stream gross production per well of 725 Boe/d.

On June 1, 2025, we moved the drilling rig to our Noble pad development in Weld County, which consists of seven wells. The Noble wells came online in November 2025 with initial average Two–stream gross production
per well of 550 Boe/d.

In September 2025, we moved the drilling rig to our then–recently acquired Simpson pad development in Weld County, which consists of six wells. Three of the Simpson pad wells came online in December 2025 and the
remainder came online in January 2026 with initial average Two–stream gross production per well of 500 Boe/d.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Revenue, Production, and Average Realized Price

The following table presents the components of our revenue, production, and average realized sales price for the years indicated:

Year Ended December 31,
2025 (1) | 2024
Revenues (in thousands)
Crude oil sales | 204,040 | 6,595
Natural gas sales | 9,472 | 551
NGL sales | 28,136 | 793
Total revenues | 241,648 | 7,939
Production:
Oil (MBbls) | 3,406 | 96
Natural gas (MMcf) | 10,753 | 245
NGL (MBbls) | 1,550 | 33
Total production (MBoe) (2) | 6,748 | 170
Average sales volumes per day (Boe/d) | 18,487 | 464
Average sales price (excluding effects of derivatives):
Oil (per MBbls) | 59.91 | 68.60
Natural gas (per MMcf) | 0.88 | 2.25
NGL (per MBbls) | 18.16 | 24.03
Average price (per MBoe) | 35.81 | 46.70
Average sales price (including effects of derivatives):
Oil (per MBbls) | 63.87 | 68.60
Natural gas (per MMcf) | 1.65 | 2.25
NGL (per MBbls) | 17.93 | 24.03
Average price (per MBoe) | 38.98 | 46.70

(1) | Total revenues and production for the year ended December 31, 2025, include revenue and production volumes from the assets acquired from Bayswater beginning on March 26, 2025, the closing date of the acquisition, through December 31, 2025.

(2) | MBoe is calculated using six MMcf of natural gas equivalent to one MBbl of oil.

Revenue and Production. For the year ended December 31, 2025, the majority of our total production volumes and revenues were attributable to properties acquired in the Bayswater Acquisition, which
closed on March 26, 2025. As such, our production and revenues for the year ended December 31, 2025 includes the production and resulting revenue from the Bayswater Acquisition from March 26, 2025 through December 31, 2025. All of our
production volumes and revenues for the year ended December 31, 2024 were derived from the assets acquired in the NRO Acquisition, which closed on October 1, 2024. We did not have any oil revenue prior to the NRO Acquisition.

Operating expenses

The following table presents the components of our operating expenses for the years indicated:

Year Ended December 31,
2025 (1) | 2024
(In thousands, except per Boe amounts)
Lease operating expenses | 41,411 | 1,265
Transportation and processing | 8,910 | 864
Ad valorem and production taxes | 21,231 | 591
Depreciation, depletion, and amortization | 48,916 | 427
Accretion of asset retirement obligation | 247 | 6
Exploration expenses | 1,332 | 734
Abandonment and impairment of unproved properties | 3,409 | —
General and administrative expenses (2) | 50,614 | 30,565
Total operating expenses | 176,070 | 34,452
Operating expenses per Boe:
Lease operating expenses | 6.14 | 7.44
Transportation and processing | 1.32 | 5.08
Ad valorem and production taxes | 3.15 | 3.48
Depreciation, depletion, and amortization | 7.25 | 2.51
Accretion of asset retirement obligation | 0.04 | 0.04
Exploration expenses | 0.20 | 4.31
Abandonment and impairment of unproved properties | 0.51 | —
General and administrative expenses (2) | 7.50 | 179.80
Total operating expenses | 26.11 | 202.66

(1) | Total operating expenses for the year ended December 31, 2025, include operating expenses for the assets acquired from Bayswater beginning on March 26, 2025, the closing date of the acquisition, through December 31, 2025. Operating expenses per Boe for the year ended December 31, 2025 are calculated over production volumes which include volumes from the assets acquired from Bayswater beginning on March 26, 2025, the closing date of the acquisition, through December 31, 2025.

(2) | General and administrative expenses for the years ended December 31, 2025 and 2024 include non–cash long–term incentive compensation expenses of $14.8 million and $8.4 million, respectively.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-31_item1_business.md)

Item 1. | Business

Overview

Prairie Operating Co. (the "Company," "we," "our" or "us") is an independent oil and natural gas company focused on the acquisition and development of crude oil, natural gas, and NGLs. Our assets and operations are
strategically located in the oil region of rural Weld County, Colorado, within the Denver–Julesburg Basin in Colorado (the "DJ Basin"). We believe the DJ Basin to be one of the premier resource plays in the United States ("U.S."), as Weld
County boasts some of the lowest break–even prices in the U.S., and has a long production history that has proven and consistent results. The productivity of this resource is demonstrated by the integral role that Weld County holds in
Colorado's energy economy, having produced 83% of Colorado's oil production as of December 2025.

We seek to deliver energy in an environmentally efficient manner by deploying next–generation technology and techniques. In addition to growing production through our drilling operations, we also seek to grow our
business through accretive acquisitions focusing on assets with the following criteria: (i) producing reserves, with opportunities to add accretive, undeveloped bolt–on acreage; (ii) ample, high rate–of–return inventory of drilling locations
that can be developed with cash flow reinvestment; (iii) strong well–level economics; (iv) liquids–rich assets; and (v) accretive valuation.

As of December 31, 2025, our assets consist of our Central Weld Assets (as defined herein), made up of approximately 45,000 net leasehold acres, on and under approximately 56,200 gross acres, and our Genesis Assets
(as defined herein), made up of approximately 23,000 net leasehold acres in, on and under approximately 42,000 gross acres. The majority of our Central Weld Assets were acquired from Nickel Road Development LLC and Nickel Road Operating LLC
(collectively, "NRO") in October 2024, from Bayswater Resources, LLC, Bayswater Fund III–A, LLC, Bayswater Fund III–B, LLC, Bayswater Fund IV–A, LP, Bayswater Fund IV–B, LP, Bayswater Fund IV–Annex, LP, and Bayswater Exploration &
Production, LLC (collectively, "Bayswater") in March 2025, and from Edge Energy II LLC ("Edge Energy") in July 2025 and the majority of our Genesis Assets were acquired in 2023.

Business Strategy

We intend to increase stakeholder value by using the following strategies to grow our reserves, production, and cash flow in a capital efficient and environmentally conscious manner:

Deliver growth through the development of extensive drilling inventory and acreage. We plan to target rich, immediately accessible permitted locations and organically
grow development through infill leasing. We believe this will allow us to increase production, reserves and cash flow which generate favourable returns.

Fund drilling program with free cash flow and retain low leverage. We aim to maintain a conservative financial position and develop primarily through available cash flow
from operations. We plan to allocate capital in a disciplined manner and proactively manage our cost structure.

Maximize returns and capital efficiency. We plan to utilize the latest technology in 3–D seismic mapping and geo–steering to decrease drill times and improve well results.
Additionally, our management's extensive experience allows us to deploy the latest drilling and completion methodologies and apply the industry best practices to increase overall estimated ultimate recovery versus prior generation wells.

Acquisition strategy focused on core area in the DJ Basin . We plan to pursue accretive acquisitions through an opportunistic roll–up strategy by continually evaluating
acquisition opportunities to expand our position. Our management team has a long track record of successfully sourcing and integrating acquisitions.

Proactively manage regulatory, environmental, safety, and community matters. Our development approach prioritizes the well–being of environment, communities, and wildlife,
and we actively engage with regulatory agencies to minimize surface impact while maximizing efficiency of our development program. Additionally, our operations emphasize utilizing technology and innovation to minimize impacts.

Our Properties and Operations

Central Weld Assets

On January 11, 2024, we and one of our subsidiaries entered into an asset purchase agreement (the "NRO Agreement") with NRO to acquire the assets of NRO (the "NRO Acquisition"). On October 1, 2024, we closed
the NRO Acquisition and paid $49.6 million to NRO in cash.

On February 6, 2025, we and certain of our subsidiaries entered into a purchase and sale agreement with Bayswater, pursuant to which we agreed to acquire certain oil and natural gas assets (the "Bayswater
Assets") for a purchase price of $602.8 million, subject to certain closing price adjustments (the "Bayswater Acquisition"). At the closing of the Bayswater Acquisition on March 26, 2025, we (i) paid approximately $482.5 million in cash to
Bayswater, $15.0 million of which was deposited in escrow pending the acquisition of additional working interest (the "Additional Working Interest Acquisition"), which Bayswater acquired and assigned to us on April 11, 2025, and (ii) issued
3,656,099 shares of our common stock, par value $0.01 per share ("Common Stock") to Bayswater (the "Equity Consideration"). We completed the final settlement with Bayswater on October 15, 2025, resulting in a final consideration of $475.6
million.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-31_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-31_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-31_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-17_2-02-results.md, 10-K_2026-03-31_item7_mdna.md, 10-K_2026-03-31_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
