# Triage pack — COOK · Traeger, Inc.

_Generated 2026-09-04 21:11 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** COOK · **Name:** Traeger, Inc.
- **CIK:** 0001857853
- **SIC:** 3630 — Household Appliances
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/COOK

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Traeger, Inc.
- **CIK:** 1,857,853 · **SIC:** 3630 (Household Appliances) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermNotesPayable

**Valuation**

| metric | value |
|---|---|
| price | 48.61 |
| mktcap | $136.0M |
| ev | $476.5M |
| ev_ebit | n/a |
| fcf | $13.6M |
| fcf_yield | 10.0% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -15.2% |
| net_debt | $340.5M |
| net_debt_ebit | n/a |
| cash | $59.7M |
| ltd | $400.2M |
| equity | $167.3M |
| ltd_tag | LongTermNotesPayable |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $559.5M |
| revenue_prior | $604.1M |
| rev_growth | -7.4% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$97.7M |
| net_income | -$115.2M |
| cfo | $20.5M |
| capex | $6.9M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -97.9% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 2,798,224 |
| shares_py | 135,886,236 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 8.9% |
| r6m | 26.3% |
| off_52w_high | -40.7% |
| adv20 | $2.3M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.72 |
| r_ev_ebit | 0.00 |
| r_roic | 0.08 |
| r_rev_growth | 0.13 |
| r_buyback | 1.00 |
| score | 0.44 |

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
| rank | 301 |

**Screen rationale:** buying back stock -97.9%; 12-1 momentum 8.9%


## 3. Share count trend

- Shares outstanding: **2,798,224** (CY2026Q2I) vs **135,886,236** prior year (CY2025Q2I)
- Change: **-97.9%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-03-27** — Item 5.02 (officer / director change or comp arrangement): On March 26, 2026, the Board of Directors (the "Board") of Traeger, Inc. (the "Company") reviewed the results of its 2025 annual cash incentive program and determined that the applicable performance goals were not achieved, which resulted in no payments under...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 2,750 sh / $152,070 -> net $-152,070 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 12 (open-market buys 0, sales 1).

| code | rows |
|---|---|
| A | 8 |
| F | 3 |
| S | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-05_2-02-results.md)

_Extraction: started at the first release heading, 'Operating Results for the Second Quarter'; skipped 9 forward-looking-statement block(s); 15 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (q2-26earningspressrelease.htm)

Operating Results for the Second Quarter

Total revenue decreased by 17.4% to $120.2 million, compared to $145.5 million in the second quarter last year.

• Grills decreased 17.0% to $61.6 million as compared to the second quarter last year. The decrease was pri marily driven by lower average selling prices, reflecting a shift in product mix towards more accessible price points, as well as pricing and channel actions under Project Gravity. These factors were partially offset by higher unit volumes associated with new product launches.

• Consumables decreased 9.9% to $32.8 million as compared to the second quarter last y ear. The decrease was driven by lower wood pellet sales, reflecting seasonal ordering timing, and a decrease in food consumables sales reflecting prior year channel expansion.

• Accessories decreased 26.2% to $25.8 million as compared to the second quarter last year. This decrease was driven primarily by lower sales of MEATER smart thermometers.

Gross profit decreased to $47.4 million, compared to $57.0 million in the second quarter last year. Gross profit margin was 39.5% in the second quarter, compared to 39.2% in the same period last year. The increase in gross margin was primarily driven by the benefit from the IEEPA tariff refund, timing of trade spend, and higher mix of direct import sales, partially offset by product mix.

Sales and marketing expenses were $17.1 million, compared to $24.8 million in the second quarter last year. The decrease in sales and marketing expense was driven by lower employee-related costs and reduced demand creation spend, reflecting cost reduction actions associated with Project Gravity.

General and administrative expenses were $21.8 million, compared to $26.0 million in the second quarter last year. The decrease in general and administrative expens e was driven by lower employee-related costs, reflecting cost reduction actions associated with Project Gravity .

Restructuring and other costs were $1.5 million, compared to $3.5 million in the second quarter last year. The decrease was primarily driven by lower severance and other personnel costs, as well as reduced consulting fees.

Net loss was $8.6 million in the second quarter, or $3.12 per diluted share, as compared to a net loss of $7.4 million in the second quarter of last year, or $2.77 per diluted share. 1

Adjusted net income was $1.4 million, or $0.53 per diluted share as compared to adjusted net loss of $1.9 million, or $0.73 per diluted share in the second quarter last year. 2

Adjusted EBITDA was $17.3 million in the second quarter as compared to $14.3 million in the same period last year despite lower revenue, reflecting the benefit of Project Gravity actions, disciplined expense management and continued focus on profitability . 2

1 This press release reflects the impact of the 1-for-50 reverse stock split of the Company's common stock, par value $0.0001 per share, effective on March 17, 2026. All share and per share amounts have been retroactively adjusted to reflect the reverse stock split for all periods presented. See our Form 10-Q for the quarter ended June 30, 2026 for additional information. Additionally, all potentially dilutive securities were antidilutive for the periods presented and were therefore excluded from the computation of diluted net loss per share as of June 30, 2026 and 2025.

2 Reconciliations of GAAP to non-GAAP financial measures, as well as definitions for the non-GAAP financial measures included in this press release and the reasons for their use, are presented below.

Balance Sheet

Cash and cash equivalents at the end of the second quarter totaled $59.7 million, compared to $19.6 million at December 31, 2025.

Inventory at the end of the second quarter was $76.3 million, compared to $98.8 million at December 31, 2025.

These improvements reflect continued execution under Project Gravity and support our focus on balance sheet health and liquidity.

Guidance For Full Year Fiscal 2026

This updated outlook reflects the continued execution of Project Gravity, including approximately $50 million of value capture in fiscal 2026. The reduction in revenue guidance is primarily due to additional softness in the MEATER business and anticipated near-term channel offsets associated with the Company's distribution expansion strategy, revising our previously issued revenue guidance range of $465 million to $485 million. Adjusted EBITDA guidance is unchanged despite lower revenue expectations, and gross margin guidance has been increased to reflect favorable tariff assumptions relative to prior expectations, revising our previously issued gross margin guidance range of 39.5% to 40.5%. Free Cash Flow guidance reflects continued progress on working capital efficiency and inventory reduction initiatives.

• Total revenue is expected to be betw een $435 million and $465 million

• Gross Margin is expected to be between 40.0% and 41.0%

• Adjusted EBITDA is expected to be between $57 million and $67 million

• Free Cash Flow is expected to be at least $30 million

A reconciliation of Adjusted EBITDA and Free Cash Flow guidance to Net Loss and Net cash provided by (used in) operating activities on a forward-looking basis cannot be provided without unreasonable efforts, as the Company is unable to provide reconciling information with respect to, in the case of Adjusted EBITDA, adjustments for benefit for income taxes, interest expense, depreciation and amortization, other (income) expense, stock-based compensation, non-routine legal expenses, restructuring and other costs and employee retention tax credits , and, in the case of Free Cash Flow, adjustments for purchases of property, plant, and equipment .

Conference Call Details

A conference call to discuss the Company's second quarter results is scheduled for Wednesday, August 5, 2026, at 4:30 p.m. ET. To participate, please dial (833) 461-5787 or +1 (585) 542-9983 for international callers, conference ID 167441052. The conference call will also be webcast live at https://investors.traeger.com . A replay of the webcast will also be available approximately two hours after the conclusion of the call on the Company's website at https://investors.traeger.com . A supplemental presentation has also been posted to the Company's website at https://investors.traeger.com.

About Traeger

Traeger Grills, headquartered in Salt Lake City, is the creator and category leader of the wood pellet grill, an outdoor cooking system that ignites all-natural hardwoods to grill, smoke, bake, roast, braise, and barbecue. In 2023, Traeger entered the griddle category, further establishing its leadership position in the outdoor cooking space. Traeger grills are versatile and easy to use, empowering cooks of all skill sets to create delicious meals with flavor that cannot be replicated. Grills are at the core of our platform and are complemented by Traeger wood pellets, rubs, sauces, accessories, and MEATER smart thermometers.

The Brand Amp

Traeger@thebrandamp.com

TRAEGER, INC.

CONDENSED CONSOLIDATED BALANCE SHEETS

(in thousands, except share and per share amounts)

June 30, 2026 | December 31, 2025
(unaudited)
ASSETS
Current Assets
Cash and cash equivalents | 59,687 | 19,624
Accounts receivable, net | 74,363 | 82,122
Inventories | 76,259 | 98,831
Prepaid expenses and other current assets | 11,334 | 14,272
Total current assets | 221,643 | 214,849
Property, plant, and equipment, net | 29,124 | 33,703
Operating lease right-of-use assets | 35,766 | 38,201
Intangible assets, net | 366,205 | 387,050
Other non-current assets | 2,002 | 2,173
Total assets | 654,740 | 675,976
LIABILITIES AND STOCKHOLDERS' EQUITY
Current Liabilities
Accounts payable | 10,872 | 14,135
Accrued expenses | 50,322 | 62,668
Current portion of notes payable | 250 | 250
Current portion of operating lease liabilities | 1,757 | 2,650
Other current liabilities | 371 | 382
Total current liabilities | 63,572 | 80,085
Notes payable, net of current portion | 400,162 | 399,590
Operating leases liabilities, net of current portion | 22,177 | 23,040
Deferred tax liability | — | 1,861
Other non-current liabilities | 1,540 | 552
Total liabilities | 487,451 | 505,128
Commitments and contingencies
Stockholders' equity:
Preferred stock, $0.0001 par value; 25,000,000 shares authorized and no shares issued or outstanding as of June 30, 2026 and December 31, 2025 | — | —
Common stock, $0.0001 par value; 1,000,000,000 shares authorized
Issued and outstanding shares - 2,798,124 and 2,741,312 as of June 30, 2026 and December 31, 2025 | — | —
Additional paid-in capital | 977,114 | 974,386
Accumulated deficit | (809,701) | (804,066)
Accumulated other comprehensive income (loss) | (124) | 528
Total stockholders' equity | 167,289 | 170,848
Total liabilities and stockholders' equity | 654,740 | 675,976

TRAEGER, INC .

CONDENSED CONSOLIDATED STATEMENTS OF OPERATIONS AND COMPREHENSIVE LOSS

(unaudited)

(in thousands, except share and per share amounts)

Three Months Ended June 30, | Six Months Ended June 30,
2026 | 2025 | 2026 | 2025
Revenue | 120,163 | 145,483 | 214,229 | 288,766
Cost of revenue | 72,745 | 88,483 | 123,796 | 172,307
Gross profit | 47,418 | 57,000 | 90,433 | 116,459
Operating expenses:
Sales and marketing | 17,067 | 24,779 | 29,699 | 46,989
General and administrative | 21,791 | 26,032 | 41,204 | 51,051
Amortization of intangible assets | 8,812 | 8,816 | 17,625 | 17,634
Restructuring and other costs | 1,453 | 3,468 | 4,633 | 3,468
Total operating expense | 49,123 | 63,095 | 93,161 | 119,142
Loss from operations | (1,705) | (6,095) | (2,728) | (2,683)
Other income (expense):
Interest expense | (8,273) | (8,091) | (15,883) | (15,984)
Other income, net | 506 | 6,411 | 11,791 | 8,514
Total other expense | (7,767) | (1,680) | (4,092) | (7,470)
Loss before benefit for income taxes | (9,472) | (7,775) | (6,820) | (10,153)
Benefit for income taxes | (909) | (391) | (1,185) | (1,991)
Net loss | (8,563) | (7,384) | (5,635) | (8,162)
Net loss per share, basic and diluted | (3.12) | (2.77) | (2.06) | (3.11)
Weighted average common shares outstanding, basic and diluted | 2,748,334 | 2,665,790 | 2,731,664 | 2,626,237
Other comprehensive income (loss):
Foreign currency translation adjustments | (95) | 121 | (102) | (151)
Amortization of dedesignated cash flow hedge | — | (938) | (550) | (1,944)
Total other comprehensive loss | (95) | (817) | (652) | (2,095)
Comprehensive loss | (8,658) | (8,201) | (6,287) | (10,257)

TRAEGER, INC.

CONDENSED CONSOLIDATED STATEMENTS OF CASH FLOWS

(unaudited)

(in thousands)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-06_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

Traeger is the creator and category leader of the wood pellet grill, an outdoor cooking system that ignites all-natural hardwoods to grill, smoke, bake, roast, braise, and barbecue. Our grills are versatile and easy to use, empowering cooks of all skill sets to create delicious meals with a wood-fired flavor that cannot be replicated with gas, charcoal, or electric grills. Grills are at the core of our platform and are complemented by Traeger wood pellets, rubs, sauces, and accessories.

In May 2025, we commenced Project Gravity, a multi-step strategic optimization plan intended to streamline our organizational structure and rebalance our cost base, including a reduction in force, centralization of our MEATER business into our Salt Lake City infrastructure, discontinuation of the Costco roadshow program, exit from the Traeger direct to consumer business by redirecting Traeger.com consumers to retail partners, transition to a distributor model in certain European markets that operate under a direct model, and pellet mill consolidation.

Our marketing strategy has been instrumental in building our brand and driving customer advocacy and revenue. We have disrupted the outdoor cooking market and created a passionate community, the Traegerhood, which includes foodies, pitmasters, backyard heroes, moms and dads, professional athletes, outdoorsmen and outdoorswomen, and world-class chefs. This community, together with our various marketing initiatives, has helped to promote our brand and products to the wider consumer population and supported our efforts to redefine outdoor cooking as an experience accessible to everyone. We have an active online and social media presence and a content-rich website that drives significant customer engagement and brings our Traegerhood together. We also directly engage with our current and target customers by sponsoring and participating in a variety of events, including live shows, outdoor festivals, rodeos, music and film festivals, barbecue competitions, fishing tournaments, and retailer events. We believe the style and authenticity of our customer engagement reinforces our brand and drives new and existing customer interest in our products and community.

Our revenue is primarily generated through the sale of our wood pellet grills, consumables, and accessories. We currently offer eight series of grills – Woodridge, Ironwood, Timberline, Pro (with and without WiFIRE), and Flatrock – as well as a selection of smaller, portable grills within our Portable Series and a special Club Lineup through targeted channels. Our grills are available in a number of different sizes and can be upgraded through a variety of accessories. The majority of our grills feature WiFIRE technology, which allows users to monitor and adjust their grills remotely using our Traeger app. Our consumables include our wood pellets, which are made from natural, virgin hardwood and are available in a variety of flavors, as well as rubs and sauces. Our accessories include MEATER smart thermometers, P.A.L. Pop-And-Lock accessory rails, grill covers, liners, tools, apparel, and other ancillary items.

We sell our grills using an omnichannel distribution strategy that consists primarily of retail and direct to consumer ( " DTC") channels. Our retail channel covers brick-and-mortar retailers, e-commerce platforms, and multichannel retailers, who, in turn, sell our grills to their end customers. Our retailers include Ace Hardware, Amazon, Costco, The Home Depot, and Best Buy, among others, as well as a significant number of independent retailers that cater to local communities and specific categories, such as hardware, camping, outdoor, farm, ranch, barbecue, and other categories. Our DTC channel covers sales directly to customers through our website and Traeger app, as well as certain country- and region-specific Traeger or distributor websites. Our consumables and accessories are available through the same channels as our grills. As part of Project Gravity, we are undertaking a broader channel optimization strategy that includes exiting the Traeger-operated DTC business. In connection with this shift, we have begun redirecting consumers from Traeger.com to our retail partners' websites, aligning our distribution model more closely with our retail-focused strategy. However, we will continue to offer our MEATER smart thermometer accessories through the DTC channel, as this model remains well‑suited to the MEATER brand and consumer base.

Over the last several years, we have made significant investments in our supply chain and manufacturing operations. Our supply chain includes third-party manufacturers for our grills and accessories and pellet production facilities for our wood pellets that we own or lease. We work closely with our manufacturers to evolve on design, manufacturing process, and product

quality. Our grills are currently manufactured in China and Vietnam, our wood pellets are produced at facilities located in New York, Oregon, Georgia, Virginia, Texas, and Poland, and our MEATER smart thermometer accessories are currently manufactured in Taiwan. We have entered into manufacturing agreements covering the supply of substantially all of our grills and accessories, pursuant to which we make purchases on a purchase order basis. We rely on several third-party suppliers for the components used in our grills, including integrated circuits, processors, and system on chips.

Our revenue decreased by 7.4% to $559.5 million for the year ended December 31, 2025, compared to $604.1 million for the year ended December 31, 2024. We recorded a net loss of $115.2 million for the year ended December 31, 2025, compared to a net loss of $34.0 million for the year ended December 31, 2024.

Key Factors Affecting Our Financial Condition and Results of Operations

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The following tables summarize key components of our results of operations for the periods presented (dollars in thousands). The period-to-period comparisons of our historical results are not necessarily indicative of the results that may be expected in the future.

Year-ended December 31, | Change
2025 | 2024 | Amount | %
Revenue | 559,520 | 604,072 | (44,552) | (7.4) | %
Cost of revenue | 340,174 | 348,603 | (8,429) | (2.4) | %
Gross profit | 219,346 | 255,469 | (36,123) | (14.1) | %
Operating expense:
Sales and marketing | 90,217 | 109,656 | (19,439) | (17.7) | %
General and administrative | 95,031 | 113,483 | (18,452) | (16.3) | %
Amortization of intangible assets | 35,260 | 35,274 | (14) | — | %
Goodwill impairment | 74,725 | — | 74,725 | *
Restructuring and other costs | 21,840 | — | 21,840 | *
Total operating expense | 317,073 | 258,413 | 58,660 | 22.7 | %
Loss from operations | (97,727) | (2,944) | 94,783 | 3219.5 | %
Other income (expense):
Interest expense | (31,350) | (33,500) | (2,150) | (6.4) | %
Other income, net | 9,755 | 480 | 9,275 | 1932.3 | %
Total other expense | (21,595) | (33,020) | (11,425) | (34.6) | %
Loss before benefit from income taxes | (119,322) | (35,964) | 83,358 | 231.8 | %
Benefit from income taxes | (4,141) | (1,956) | (2,185) | 111.7 | %
Net loss | (115,181) | (34,008) | 81,173 | 238.7 | %

* Not meaningful

Comparison of the Year Ended December 31, 2025 and 2024

Revenue

Year-ended December 31, | Change
2025 | 2024 | Amount | %
(dollars in thousands)
Revenue:
Grills | 298,026 | 324,702 | (26,676) | (8.2) | %
Consumables | 127,474 | 119,299 | 8,175 | 6.9 | %
Accessories | 134,020 | 160,071 | (26,051) | (16.3) | %
Total Revenue | 559,520 | 604,072 | (44,552) | (7.4) | %

Revenue decreased by $44.6 million, or 7.4%, to $559.5 million for the year ended December 31, 2025 compared to $604.1 million for the year ended December 31, 2024. This decrease was primarily driven by lower sales from our grills and accessories, partially offset by higher sales from our consumables.

Revenue from our grills decreased by $26.7 million, or 8.2%, to $298.0 million for the year ended December 31, 2025 compared to $324.7 million for the year ended December 31, 2024. The decrease was primarily driven by a mid-single digit decline in average selling price and mid-single digit reduction in unit volume. The lower average selling price ("ASP") reflected a mix shift to lower priced grills, while the decrease in unit volume was driven by the impact of pricing actions on demand, partially offset by higher orders of lower ASP grills.

Revenue from our consumables increased by $8.2 million, or 6.9%, to $127.5 million for the year ended December 31, 2025 compared to $119.3 million for the year ended December 31, 2024. The increase was primarily driven by a high-single digit increase in wood pellet and food consumable sales. The wood pellet sales were driven by high-single digit increase in average selling price from our strategic alignment with certain wholesale partners. The food consumables increase in sales was primarily due to expansion in distribution.

Revenue from our accessories decreased by $26.1 million, or 16.3%, to $134.0 million for the year ended December 31, 2025 compared to $160.1 million for the year ended December 31, 2024. This decrease was driven primarily by lower sales of MEATER smart thermometers, partially offset by low-double digit increases in average selling prices and unit volumes in Traeger branded accessories.

Gross Profit

Year-ended December 31, | Change
2025 | 2024 | Amount | %
(dollars in thousands)
Gross profit | 219,346 | 255,469 | (36,123) | (14.1) | %
Gross margin (Gross profit as a percentage of revenue) | 39.2 | % | 42.3 | %

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-06_item1_business.md)

Item 1. Business.

Overview

Welcome to the Traegerhood

Our mission is to bring people together to create a more flavorful world.

Traeger is the creator and category leader of the wood pellet grill, an outdoor cooking system that ignites all-natural hardwoods to grill, smoke, bake, roast, braise, and barbecue. Our Traeger grills are versatile and easy to use, empowering cooks of all skill sets to create delicious meals with a wood-fired flavor that cannot be replicated with gas, charcoal, or electric grills.

At the heart of our brand is a passionate and engaged community called the Traegerhood, which includes everyone from casual grillers to competition pitmasters and professional chefs. Our flagship wood pellet grills are internet of things ( " IoT") devices that allow owners to program, monitor, and control their grill through our Traeger app, which engaged 2.8 million active users for the fiscal year ended December 31, 2025. We complement our innovative cooking technologies with an extensive digital library of original recipes and Traeger cooking classes. In addition, we offer consumable products, such as wood pellets, rubs, and sauces, that drive recurring revenue.

Leveraging our authentic brand and the Traegerhood, we have established an omnichannel distribution strategy led by retailers ranging from Ace Hardware and The Home Depot to Amazon and Best Buy. We complement this retail channel with direct to consumer ( " DTC") sales through our website and Traeger app.

Today, we estimate that 78 million households in the United States own a grill, representing the total addressable market. With approximately 2.7 million Traeger grills sold in the United States from 2020 to 2025, we estimate that our U.S. household penetration is only 3.4% of this total addressable market. As a result, we believe our potential market opportunity is massive and that our ability to grow within and beyond the outdoor grill market is unrivaled. We see opportunities to expand our integrated, connected cooking platform with new types of technologies and experiences. Together with the Traegerhood, we are disrupting home cooking.

Recent Developments-Project Gravity

In May 2025, we launched "Project Gravity," a multi-step strategic optimization plan to streamline our organizational structure and rebalance our cost base. Actions include a reduction in force, centralization of our MEATER business into our Salt Lake City infrastructure, discontinuation of the Costco roadshow program, redirection of Traeger.com consumers to retail partners as part of our exit from the Traeger direct-to-consumer business, transition to a distributor model in certain European markets that currently operate under a direct model, and pellet mill consolidation. We recorded $24.9 million of total restructuring and other costs related to these actions in fiscal year 2025 and expect the program to be substantially completed by the end of fiscal year 2026.

Overview of Our Products and Integrated, Connected Cooking Platform

The Original

In 1987, we invented the original wood pellet grill. The original Traeger helped to transform outdoor cooking by making it easy to enjoy the delicious flavors of wood-fired food. Prior to the original Traeger, cooking with wood fire was difficult and there was no efficient way to ignite the wood, maintain consistent temperatures, and create the right amount of smoke. The original Traeger helped to solve these challenges, making it easier for home cooks to achieve extraordinary culinary results.

The Reinvented Original

We've come a long way since 1987 and have made significant improvements to our grills and technologies. Along the way, our product design has been centered on our core concepts of taste, versatility, ease of use, consistency, and community.

Beginning in 2014, we pioneered a digital outdoor cooking experience. Using software, internet connectivity, and cloud technology, we reinvented the original Traeger to be an IoT device, featuring a variety of modern technologies, including:

• WiFIRE technology – Utilizes cloud-computing, our Traeger app, and our cloud-connected grills to enable users to automate recipe steps and control and monitor their grill from anywhere in the world using their smartphone.

• D2 Direct Drive – An automated control system that maintains grill temperature to +/-5 degrees of set temperature through fans and DC auger control.

• Super Smoke Mode – A proprietary cooking mode that maximizes production of hardwood smoke to infuse flavors into food.

• Pellet Sensor – A connected sensor that measures wood pellet levels and communicates with our Traeger app, enabling users to monitor fuel levels and receive alerts when fuel gets low.

• TurboTemp – A rapid startup system that brings the grill to cooking temperature and reacts quickly to temperature changes.

• Smart Combustion – A proprietary technology that helps our grills maintain consistent cooking temperatures.

• EZ Clean – A 2-in-1 grease and ash collection system.

Today, our wood pellet grills feature modern, updated designs that improve upon the original. Our grills use an auger to feed natural hardwood pellets into a fire pot, where they are ignited by a hot rod to create heat and flavorful smoke. A fan stokes the fire and creates convection, which is key to the versatility of our grills. Drip trays funnel grease, fat, and oil for easy clean-up and to help prevent flareups.

Our Integrated Platform

Our integrated platform includes six types of products: wood pellet grills, gas griddles, digital content, the Traeger app, consumables and grilling accessories. We integrate these products to optimize the cooking experience and produce valuable feedback loops with consumers. As a result, our integrated platform can drive grill usage, brand affinity, word of mouth, and purchases of our consumables.

Products

Our Grills

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-06_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-06_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-06_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-05_2-02-results.md, 10-K_2026-03-06_item7_mdna.md, 10-K_2026-03-06_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
