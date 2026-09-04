# Triage pack — KVHI · KVH INDUSTRIES INC \DE\

_Generated 2026-09-04 21:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** KVHI · **Name:** KVH INDUSTRIES INC \DE\
- **CIK:** 0001007587
- **SIC:** 4899 — Communications Services, NEC
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/KVHI

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** KVH INDUSTRIES INC \DE\
- **CIK:** 1,007,587 · **SIC:** 4899 (Communications Services, NEC) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 7.07 |
| mktcap | $128.3M |
| ev | $70.5M |
| ev_ebit | n/a |
| fcf | $9.8M |
| fcf_yield | 7.6% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -12.1% |
| net_debt | -$57.7M |
| net_debt_ebit | n/a |
| cash | $57.7M |
| ltd | $0.00 |
| equity | $130.4M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $111.0M |
| revenue_prior | $113.8M |
| rev_growth | -2.5% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$11.2M |
| net_income | -$7.4M |
| cfo | $17.1M |
| capex | $7.4M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -7.0% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 18,140,962 |
| shares_py | 19,504,764 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 70.2% |
| r6m | 17.8% |
| off_52w_high | -39.5% |
| adv20 | $1.2M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.62 |
| r_ev_ebit | 0.00 |
| r_roic | 0.10 |
| r_rev_growth | 0.26 |
| r_buyback | 0.91 |
| score | 0.43 |

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
| rank | 307 |

**Screen rationale:** buying back stock -7.0%; debt data missing (net cash unverified); 12-1 momentum 70.2%


## 3. Share count trend

- Shares outstanding: **18,140,962** (CY2026Q2I) vs **19,504,764** prior year (CY2025Q2I)
- Change: **-7.0%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-02 among the 4 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 42,735 sh / $447,263 -> net $-447,263 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 13 (open-market buys 0, sales 6).

| code | rows |
|---|---|
| A | 1 |
| J | 6 |
| S | 6 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'KVH Industries Reports Second Quarter 2026 Results'; skipped 1 forward-looking-statement block(s); 6 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (q22026exhibit991.htm)

KVH Industries Reports Second Quarter 2026 Results

BRISTOL, RI, August 6, 2026 — KVH Industries, Inc. (Nasdaq: KVHI), reported financial results for the quarter ended June 30, 2026 today. The company will hold a conference call to discuss these results at 9:00 a.m. ET today, which can be accessed at investors.kvh.com. Following the call, a replay of the webcast will be available through the company's website.

Second Quarter 2026 Highlights

• Total revenues in the second quarter of 2026 increased sequentially from the first quarter of 2026 by $1.4 million, or 4%, to $33.7 million. Total revenues increased by 27% in the second quarter of 2026 from $26.6 million in the second quarter of 2025, due to a $6.7 million increase in service sales and a $0.4 million increase in product sales.

• Service revenue increased sequentially from the first quarter of 2026 by $1.6 million, or 6%, to $29.7 million in the second quarter of 2026. Service revenue increased by $6.7 million, or 29%, in the second quarter of 2026 compared to the second quarter of 2025.

• Airtime revenue increased $1.4 million, or 5%, to $27.8 million in the second quarter of 2026 from $26.4 million in the first quarter of 2026. Airtime revenue increased $6.6 million, or 31%, in the second quarter of 2026 compared to the sec ond quarter of 2025. The increase in airtime revenue was primarily due to an increase in subscribers for both Starlink and OneWeb.

• Net income in the second quarter of 2026 was $0.2 million, or $0.01 per share, compared to a net income of $0.9 million, or $0.05 per share, in the second quarter of 2025.

• Non-GAAP adjusted EBITDA was $3.0 million in the second quarter of 2026, compared to $2.7 million in the second quarter of 2025.

Commenting on the company's second quarter results, Brent C. Bruun, KVH's Chief Executive Officer, said, "Our second quarter results reflected the strength of our strategy—accelerating growth in LEO services, driven by Starlink, as we continue to outpace much of our industry through this transition. We are seeing growth in recurring service revenue, expansion of our subscriber base, and meaningful progress on strategic initiatives, including our new bundled multi-network service offerings. We remain focused on delivering innovative connectivity solutions for our customers while creating long-term value for our shareholders."

Financial Highlights - (in millions, except per share data)

Three Months Ended | Six Months Ended
June 30, | June 30,
2026 | 2025 | 2026 | 2025
GAAP Results
Revenue | 33.7 | 26.6 | 66.0 | 52.0
Loss from operations | (0.1) | (0.4) | (0.2) | (2.6)
Net income (loss) | 0.2 | 0.9 | 0.8 | (0.8)
Net income (loss) per share | 0.01 | 0.05 | 0.04 | (0.04)
Non-GAAP Adjusted EBITDA | 3.0 | 2.7 | 5.8 | 3.7

Second Quarter Financial Summary

Revenue was $33.7 million for the second quarter of 2026, an increase of 27% compared to $26.6 million in the second quarter of 2025.

Service revenues for the second quarter were $29.7 million, an increase of $6.7 million compared to the second quarter of 2025. The increase in service sales was primarily due to a $6.6 million increase in our airtime service sales, which reflected a substantial increase in LEO service sales driven by an increase in subscribers for both Starlink and OneWeb. This increase in LEO service sales was partially offset by a substantial decrease in VSAT service sales, which was driven primarily by a decrease in VSAT subscribers. For the three months ended June 30, 2026, LEO service sales represented over 55% of airtime service sales, as compared to less than 32% for the three months ended June 30, 2025. The increase in LEO service sales as a percentage of total airtime sales resulted from both the substantial increase in LEO service sales and the substantial decrease in VSAT service sales.

Product revenues for the second quarter were $4.0 million, an increase of 12% compared to the second quarter of 2025. The increase in product sales was primarily due to a $0.7 million increase in Starlink product sales and a $0.3 million increase in OneWeb product sales, partially offset by a $0.5 million decrease in TracVision product sales and a $0.2 million decrease in VSAT Broadband product sales. Competition from low-cost alternatives to VSAT, which include streaming capabilities, has had a significant impact on sales of our TracVision products.

Our operating expenses increased $0.9 million to $10.4 million for the second quarter of 2026, compared to $9.5 million in the second quarter of 2025. The increase was primarily due t o a $0.4 million increase in salaries, benefits and taxes, a $0.3 million increase in professional fees, a $0.3 million increase in bad debt expense, a $0.1 million increase in amortization expense and a $0.1 million increase in computer expenses, partially offset by a $0.3 million decrease in warranty expense and a $0.1 million decrease in facilities expenses.

Six Months Ended June 30 Financial Summary

Revenue was $66.0 million for the six months ended June 30, 2026, an increase of 27% compared to $52.0 million for the six months ended June 30, 2025.

Service revenues for the six months ended June 30, 2026 were $57.9 million, an increase of 29% compared to the six months ended June 30, 2025. The increase in service sales was primarily due to an overall $12.7 million increase in our airtime service sales, which reflected a sub stantial increase in LEO service sales driven by an increase in subscribers for both Starlink and OneWe b, and a substantial decrease in VSAT subscribers . For the six months ended June 30, 2026, LEO service sales represented over 50% of airtime service sales, as compared to less than 30% for the six months ended June 30, 2025. The increase in LEO service sales as a percentage of total airtime sales resulted from both a substantial increase in LEO service sales and a substantial decrease in VSAT service sales. Competing LEO service providers have continued to expand their product and service offerings, further heightening competition in the global leisure segment and in commercial and government markets.

Product revenues for the six months ended June 30, 2026 were $8.2 million, an increase of 11% compared to the six months ended June 30, 2025. The increase in product sales was primarily d ue to a $1.0 million increase in Starlink product sales, a $0.9 million increase in OneWeb product sales, and a $0.4 million increase in accessory and service parts product sales, partially offset by a $1.0 million decrease in TracVision product sales and a $0.5 million decrease in VSAT Broadband product sales. Competition from low-cost alternatives to VSAT, which include streaming capabilities, has had a significant impact on sales of our TracVision products.

Our operating expenses increased $0.9 million to $20.1 million in the six months ended June 30, 2026, compared to $19.2 million in the six months ended June 30, 2025. This increase was primarily due to a $0.5 million increase in salaries, benefits and taxes, a $0.3 million increase in computer expenses, a $0.2 million increase in professional fees, a $0.2 million increase in bad debt expense and a $0.2 million increase in amortization expense, partially offset by a $0.4 million decrease in warranty expense and a $0.2 million decrease in dues and subscriptions.

Conference Call Details

KVH Industries will host a conference call today at 9:00 a.m. ET through the company's website. The conference call can be accessed at investors.kvh.com and listeners are welcome to submit questions pertaining to the earnings release and conference call to ir@kvh.com. The audio archive will be available on the company website within three hours of the completion of the call.

Non-GAAP Financial Measures

This release provides non-GAAP financial information as a supplement to our condensed consolidated financial statements, which are prepared in accordance with generally accepted accounting principles ("GAAP"). Management uses these non-GAAP financial measures internally in analyzing financial results to assess operational performance. The presentation of this financial information is not intended to be considered in isolation or as a substitute for the financial information prepared in accordance with GAAP. The non-GAAP financial measures used in this press release adjust for specified items that can be highly variable or difficult to predict. Management generally uses these non-GAAP financial measures to facilitate financial and operational decision-making, including evaluation of our historical operating results and comparison to competitors' operating results. These non-GAAP financial measures reflect an additional way of viewing aspects of our operations that, when viewed with GAAP results and the reconciliations to corresponding GAAP financial measures, may provide a more complete understanding of factors and trends affecting our business.

Some limitations of non-GAAP adjusted EBITDA include the following: non-GAAP adjusted EBITDA represents net income (loss) before, as applicable, interest income, net, income tax expense (benefit), depreciation, amortization, stock-based compensation expense, goodwill impairment charges, long-lived assets impairment charges, charges for disposal of discontinued projects, loss on unfavorable future contracts, employee termination and other variable costs, executive separation costs, prior period tax settlements, transaction-related and other variable legal and advisory fees, certain inventory write-downs, excess purchase order obligations, gains on sales of real estate and other fixed assets, gains and losses on sale of subsidiaries, and foreign exchange transaction gains and losses.

Other companies, including companies in KVH's industry, may calculate these non-GAAP financial measures differently or not at all, which will reduce their usefulness as a comparative measure.

Because non-GAAP financial measures exclude the effect of items that increase or decrease our reported results of operations, management strongly encourages investors to review our consolidated financial statements and publicly filed reports in their entirety. Reconciliations of the non-GAAP financial measures to the most directly comparable GAAP financial measures are included in the tables accompanying this release.

About KVH Industries, Inc.

KVH Industries, Inc. is a global leader in maritime and mobile connectivity delivered via the KVH ONE network. The company, founded in 1982, is based in Bristol, RI, with more than a dozen offices around the globe. KVH provides connectivity solutions for commercial maritime, leisure marine, military/government, and land mobile applications on vessels and vehicles, including the TracNet, TracPhone, and TracVision product lines, the KVH ONE OpenNet Program for non-KVH antennas, AgilePlans Connectivity as a Service (CaaS), and the KVH Link crew wellbeing content service.

KVH Industries, Inc., has used, registered, or applied to register its trademarks in the USA and other countries around the world, including but not limited to the following marks: KVH, KVH ONE, TracPhone, TracVision, AgilePlans, CommBox, and TracNet. Other trademarks are the property of their respective companies.

KVH INDUSTRIES, INC. AND SUBSIDIARIES

CONDENSED CONSOLIDATED STATEMENTS OF OPERATIONS

(in thousands, except per share amounts, unaudited)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-10_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We are a leading global provider of innovative and technology-driven connectivity solutions to primarily maritime commercial and leisure customers. We provide global high-speed Internet and Voice over Internet Protocol (VoIP) services via satellite to mobile users at sea and on land. We are also a leading provider of commercially licensed entertainment, including movies, television programming, news, and music, to commercial customers in the maritime market, along with supplemental value-added cybersecurity, email, and crew internet services.

We generate revenues in the United States and various international locations, including primarily Singapore, Canada, South American countries, European Union countries and other European countries, and countries in Africa, the Middle East and Asia/Pacific, including India. Sales to customers outside the United States accounted for 78% and 73% of our consolidated net revenues for 2025 and 2024, respectively.

We generate a substantial majority of our revenues from sales of satellite Internet airtime services. We provide, for monthly fixed fees and per-usage fees, satellite connectivity encompassing broadband Internet, data and VoIP services, to customers via our KVH ONE hybrid network, which integrates global satellite service (including Starlink, Ku-band VSAT using the SES HTS network, Eutelsat OneWeb, Iridium, and other satellite services), KVH-provided cellular service in more than 130 countries, and shore-based Wi-Fi access. Sales of our low-earth-orbit (LEO) and global high-throughput satellite (HTS) airtime services accounted for 82% and 80% of our consolidated net sales for 2025 and 2024, respectively. In March 2023, we began selling Starlink terminals and, in September 2023, we became a Starlink authorized hardware and airtime reseller offering Global Priority data plans for maritime use. In October 2024, we expanded our portfolio to include Starlink Local Priority data plans, which is suitable for fixed and mobile uses on land and inland waterways, including lakes and rivers. In 2025, Starlink products and services were our fastest growing products and services. We are also now earning usage fees from our offering of Eutelsat OneWeb maritime service, which we launched in January 2025. Revenue from our cellular airtime service supplements our satellite-only airtime revenue. In addition, we earn monthly usage fees from sales of third-party satellite connectivity for VoIP and supplemental services to our Inmarsat, Iridium, Starlink and Eutelsat OneWeb customers. In December 2024, we introduced our TracNet Coastal and TracNet Coastal Pro terminals, expanding our extensive multi-channel portfolio of maritime products and services with a standalone 5G/cellular and Wi-Fi system. We also generate service revenue from product repairs and extended warranty sales.

Our service sales also include the distribution of entertainment, including movies, television programming, news and music, to commercial customers in the maritime market through KVH Media Group, along with supplemental value-added services. Sales of content services accounted for 4% and 3% of our consolidated net revenues for 2025 and 2024, respectively.

Historically, our Ku-band VSAT communications service was the primary driver of revenue growth. However, in recent years these services have represented a declining percentage of our revenues in the face of increased demand for and competition from emerging LEO services. Our satellite-only and hybrid products enable marine customers to receive data, VoIP, and value-added services via satellite, cellular, and shore-based Wi-Fi networks onboard commercial and leisure vessels. In addition, our in-motion television terminals permit customers to receive live digital television via regional satellite services on marine vessels and on recreational vehicles, buses and automobiles. We sell our products through an extensive international network of dealers and distributors. We also sell and lease products to service providers and end users. Product sales accounted for 11% and 15% of our consolidated net sales for 2025 and 2024, respectively.

Manufacturing Wind-down; Restructuring

In February 2024, we announced a staged wind-down of our product manufacturing operations at our Middletown, Rhode Island location. The wind-down was driven by reduced demand for our hardware products in the face of intensifying competition in the third and fourth quarters of 2023. We concluded that we should discontinue our capital-intensive manufacturing activities and concentrate our efforts on growing sales of our multi-orbit, multi-channel, integrated communications solutions. We expect that we will continue our product manufacturing activities in order to generate a targeted amount of inventory of maritime satellite connectivity and satellite television terminals to meet anticipated demand and that we will cease substantially all manufacturing activity by the end of 2026. This wind-down has been extended because our reduced workforce has been prioritizing fulfilling LEO product orders and refurbishing AgilePlans terminals over manufacturing new units. We expect to continue to facilitate customer transition to third-party hardware products compatible with our mobile satellite communications services. We also plan to continue to conduct maintenance, service, warehousing, shipping and receiving activities at the Middletown, Rhode Island location until our anticipated relocation in the spring of 2026.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The following table provides, for the periods indicated, certain financial data expressed as a percentage of net sales:

Year Ended December 31,
2025 | 2024
Sales:
Service | 88.6 | % | 84.7 | %
Product | 11.4 | 15.3
Net sales | 100.0 | 100.0
Costs and expenses:
Costs of service sales | 57.4 | 52.7
Costs of product sales | 17.4 | 16.3
Research and development | 3.1 | 7.4
Sales, marketing and support | 18.4 | 18.5
General and administrative | 13.8 | 14.5
Long-lived assets impairment charge | — | 1.0
Total costs and expenses | 110.1 | 110.4
Loss from operations | (10.1) | (10.4)
Interest income | 2.3 | 2.7
Interest expense | — | —
Other income (expense), net | 1.0 | (1.6)
Loss before income tax (benefit) expense | (6.8) | (9.3)
Income tax (benefit) expense | (0.1) | 0.4
Net loss | (6.7) | % | (9.7) | %

Years ended December 31, 2025 and 2024

Our net sales for 2025 and 2024 were as follows:

Change
Year Ended December 31, | 2025 vs. 2024
2025 | 2024 | %
(in thousands)
Service sales | 98,407 | 96,446 | 1,961 | 2 | %
Product sales | 12,602 | 17,382 | (4,780) | (27) | %
Net sales | 111,009 | 113,828 | (2,819) | (2) | %

Net sales decreased by $2.8 million, or 2%, in 2025 as compared to 2024. Service sales increased by $2.0 million, or 2%, to $98.4 million in 2025 from $96.4 million in 2024.

The increase in service sales was primarily due to a $0.9 million increase in CommBox Edge service sales, a $0.6 million increase in our content services sales, and a $0.5 million increase in our airtime service sales. The increase in our airtime services sales reflected a substantial increase in LEO service sales driven by an increase in subscribers for both Starlink and Eutelsat OneWeb. This increase in LEO service sales was largely offset by a substantial decrease in VSAT service sales, which was driven primarily by a decrease in VSAT subscribers, as well as a $7.7 million reduction in sales related to the U.S. Coast Guard contract downgrade in the third quarter of 2024. For 2025, LEO services sales represented over 30% of airtime services sales, as compared to less than 15% for 2024. The increase in LEO service sales as a percentage of total airtime sales resulted from both the substantial increase in LEO service sales and the substantial decrease in VSAT service sales. LEO service providers have continued to expand their product and service offerings, further heightening competition in the global commercial markets and in the leisure segment. We expect that the trend of intensifying competition from LEO satellite service providers will continue and that our revenues from VSAT service sales will continue to decline on a year-over-year basis. It is possible that the rate of reduction will accelerate.

Product sales decreased by $4.8 million, or 27%, to $12.6 million in 2025 from $17.4 million in 2024. The decrease in product sales was primarily due to a $2.2 million decrease in Starlink product sales, a $1.6 million decrease in TracVision product sales, a $1.1 million decrease in VSAT Broadband product sales and a $0.8 million decrease in accessory and service parts product sales, partially offset by a $1.0 million increase in Eutelsat OneWeb product sales. The decline in Starlink product sales was primarily driven by discounted pricing, whereas declines in other product sales was primarily driven by product mix and discounted pricing on VSAT Broadband products. Competition from low-cost alternatives to VSAT, which include streaming capabilities, has had a significant impact on sales of our TracVision products.

Costs of Sales

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-10_item1_business.md)

ITEM 1. | Business

Cautionary Statement Regarding Forward-Looking Information

In addition to historical facts, this annual report contains forward-looking statements. Forward-looking statements are merely our current predictions of future events. These statements are inherently uncertain, and actual events could differ materially from our predictions. Important factors that could cause actual events to vary from our predictions include those discussed in this annual report under the headings "Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations," and "Item 1A. Risk Factors." We assume no obligation to update our forward-looking statements to reflect new information or developments. We urge readers to review carefully the risk factors described in this annual report and in the other documents that we file with the Securities and Exchange Commission.

Additional Information Available

Our principal Internet address is www.kvh.com . Our website provides a hyperlink to a third-party website through which our annual, quarterly, and current reports, as well as amendments to those reports, are available free of charge. We believe these reports are made available as soon as reasonably practicable after we electronically file them with, or furnish them to, the SEC. We do not provide any information regarding our SEC filings directly to the third-party website, and we do not check its accuracy or completeness. The SEC maintains an Internet site at http://www.sec.gov that contains reports, proxy and information statements, and other information regarding issuers that file electronically with the SEC.

Introduction

We are a leading global provider of innovative and technology-driven connectivity solutions to primarily maritime commercial and leisure customers. We provide global high-speed Internet and Voice over Internet Protocol (VoIP) services via satellite and integrated 5G/LTE cellular communications to mobile users at sea and on land. We are also a leading provider of commercially licensed entertainment, including movies, television programming, news, and music, to commercial customers in the maritime market, along with supplemental value-added network and bandwidth management cybersecurity, email, and crew Internet services.

We currently manufacture our products in Middletown, Rhode Island, and we generate revenues in the United States and various international locations, including primarily Singapore, Canada, South American countries, European Union countries and other European countries, and countries in Africa, the Middle East and Asia/Pacific, including India. We are winding down our product manufacturing operations and currently plan to discontinue substantially all manufacturing activities by the end of 2026.

We are headquartered in Middletown, Rhode Island and plan to migrate to Bristol, Rhode Island in the spring of 2026. We have active operations in Denmark, the United Kingdom, the Philippines, and Singapore. KVH is a Delaware corporation formed in 1985.

Our Business

We provide integrated, end-to-end services, software, and hardware that support our customers' need for access to the Internet, VoIP, operations content, and entertainment services while on the move. On the services side of our business, sales of our low-earth-orbit (LEO) and global high-throughput satellite (HTS) airtime service accounted for 82% and 80% of our consolidated net sales for 2025 and 2024, respectively. Sales of content services accounted for 4% and 3% of our consolidated net sales for 2025 and 2024, respectively. On the hardware side of our business, we primarily distribute products manufactured by third-parties that support LEO satellite services. In addition, we currently manufacture and distribute a comprehensive family of mobile satellite antenna products that provide two-way access to the Internet and VoIP services using Ku-band VSAT service with integrated 5G/LTE cellular service and support for shore-based Wi-Fi. We also manufacture in-motion, stabilized antennas that provide receive-only satellite television services. Product sales accounted for 11% and 15% of our consolidated net sales for 2025 and 2024, respectively.

In the global maritime market, we believe that there is significant demand for mobile access to the Internet, operational data, voice services, entertainment content, and satellite television. For mobile access to the Internet and VoIP services, which we refer to collectively as our airtime services, we offer communication services using global satellite service (including Ku-band VSAT using the SES HTS network along with Starlink, Eutelsat OneWeb, Iridium, Inmarsat and other satellite services), 5G/LTE cellular service, and shore-based Wi-Fi access, which are marketed under the KVH ONE hybrid network brand. For customer access to our airtime services, we currently offer a family of parabolic hybrid mobile satellite antenna products, which are marketed under the TracNet hybrid terminal network brand. Under our KVH ONE OpenNet program, customers using non-KVH Ku-band VSAT terminals can subscribe to our airtime services. We are also an authorized reseller of airtime and terminals supporting the Starlink and Eutelsat OneWeb LEO services. In addition to satellite communications-based services, we also offer TracNet Coastal, a 5G/cellular and Wi-Fi based solution intended for use along coastal waterways with cellular service offered in more than 130 countries.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-10_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-10_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-10_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-03-10_item7_mdna.md, 10-K_2026-03-10_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
