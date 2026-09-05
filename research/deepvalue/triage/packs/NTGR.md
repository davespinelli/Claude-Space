# Triage pack — NTGR · NETGEAR, INC.

_Generated 2026-09-05 00:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** NTGR · **Name:** NETGEAR, INC.
- **CIK:** 0001122904
- **SIC:** 3576 — Computer Communications Equipment
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/NTGR

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** NETGEAR, INC.
- **CIK:** 1,122,904 · **SIC:** 3576 (Computer Communications Equipment) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 21.09 |
| mktcap | $573.2M |
| ev | $398.9M |
| ev_ebit | n/a |
| fcf | -$18.9M |
| fcf_yield | -3.3% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -9.6% |
| net_debt | -$174.3M |
| net_debt_ebit | n/a |
| cash | $174.3M |
| ltd | $0.00 |
| equity | $456.4M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $699.6M |
| revenue_prior | $673.8M |
| rev_growth | 3.8% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$34.2M |
| net_income | -$18.0M |
| cfo | $1.6M |
| capex | $20.5M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -6.3% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 27,179,021 |
| shares_py | 29,008,557 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -10.7% |
| r6m | 0.5% |
| off_52w_high | -41.4% |
| adv20 | $7.4M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.14 |
| r_ev_ebit | 0.00 |
| r_roic | 0.13 |
| r_rev_growth | 0.49 |
| r_buyback | 0.90 |
| score | 0.33 |

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
| rank | 382 |

**Screen rationale:** buying back stock -6.3%; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **27,179,021** (CY2026Q2I) vs **29,008,557** prior year (CY2025Q2I)
- Change: **-6.3%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-06** — Item 5.02 (officer / director change or comp arrangement): (d) On August 3, 2026, the Board of Directors (the "Board") of NETGEAR elected Douglas Murray to serve as a member of the Board, effective immediately.
- **2026-04-16** — Item 5.02 (officer / director change or comp arrangement): (b) On April 12, 2026, Bradley L. Maiorino, a member of the Board of Directors (the "Board") of NETGEAR, Inc. (the "Company"), informed the Company that he will not stand for re-election at the upcoming 2026 Annual Meeting of Stockholders (Annual Meeting).

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 6,381 sh / $162,531 -> net $-162,531 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 16 (open-market buys 0, sales 4).

| code | rows |
|---|---|
| A | 7 |
| F | 5 |
| S | 4 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'NETGEAR ® REPORTS SECOND QUARTER 2026 RESULTS'; skipped 12 forward-looking-statement block(s); 5 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (ntgr-ex99_1.htm)

NETGEAR ® REPORTS SECOND QUARTER 2026 RESULTS

Revenue and operating margin above the high end of guidance

Enterprise segment grows 7.7% year over year and delivers all-time-high non-GAAP gross margin of 54.1%

ARR from subscription and services of approximately $42 million

Douglas Murray, enterprise networking and security veteran, joins Board of Directors

SAN JOSE, California – August 6, 2026 - NETGEAR, Inc. (NASDAQ: NTGR), a global leader in intelligent networking solutions designed to power extraordinary experiences, today reported financial results for the second quarter ended June 28, 2026.

Q2 2026

•
Net revenue of $168.6 million, down 1.2% as compared to Q2 prior year

•
GAAP gross margin of 40.2 %, up 270 basis points year over year

Non-GAAP gross margin of 41.4 %, up 360 basis points year over year

•
GAAP operating income of $(8.4) million compared to $(9.5) million from Q2 prior year

Non-GAAP operating income of $4.0 million compared to $(1.2) million from Q2 prior year

•
GAAP EPS of $(0.27) compared to $(0.22) from Q2 prior year

Non-GAAP EPS of $0.16 compared to $0.06 from Q2 prior year

The accompanying schedules provide a reconciliation of financial measures computed on a GAAP basis to financial measures computed on a non-GAAP basis.

CJ Prober, Chief Executive Officer, commented, "We delivered another strong quarter of disciplined execution and improved profitability, led by the continued momentum in our Enterprise business. Our growing Enterprise business now represents more than half of our topline and approximately 69% of our non-GAAP gross profit, so we remain encouraged that the investments here are driving the intended results. We are also pleased to welcome Douglas Murray to our Board of Directors, whose deep enterprise networking and security leadership over the past 30 years at companies like Juniper Networks, Extreme Networks and in his current role as CEO of Auvik, will be a tremendous asset. We remain well positioned to create long term value for shareholders by continuing to profitably scale our Enterprise business while preserving optionality for our Consumer business as the supply and regulatory landscape evolves."

Bryan Murray, Chief Financial Officer, added, "Our second quarter results are another proof point of the second phase of our transformation, allowing NETGEAR to drive strong top and bottom-line performance even in the face of a difficult macroeconomic and supply environment. In concert with strong operational discipline, an improved revenue mix toward higher-margin Enterprise products and services allowed us to deliver topline and profitability above the high end of our guidance range. Continuing our opportunistic approach to stock repurchases, we repurchased $12.9 million of shares, bringing our total to over $116 million since the beginning of 2024, and we have approximately $75 million reserved in our current authorization. Additionally, we are pleased to share that, with our Enterprise revenue mix exceeding 50% each quarter this year, we have been able to update our SIC code to align with the other companies we are competing with in this market."

Enterprise Segment Results

•
Revenue was $89.0 million, up 7.7% year over year

•
Non-GAAP gross margin was 54.1%, up 740 basis points year over year

•
Non-GAAP contribution margin was 25.9%, up 660 basis points year over year

Mr. Prober continued, "Enterprise continued to strengthen its position as NETGEAR's primary near-term growth engine, delivering another quarter of topline growth and an all-time high non-GAAP gross margin of more than 54%, reinforcing the progress we are making toward a higher-margin growth profile. Software is becoming an increasingly important differentiator, supported by our strategic acquisitions of VAAG, Exium and the source code for our managed switch portfolio. Despite supply chain headwinds, pricing actions helped preserve robust margins and contributed to an outstanding segment contribution margin of nearly 26%, our highest in over seven years. We also continued to expand our partner and customer ecosystem, surpassing 600 ProAV manufacturing partners, extending our presence in the broadcast and education verticals, and securing several significant customer wins. With the launches of Align and Insight 10.0, growing adoption of Engage, and new go-to-market leadership in APAC, NETGEAR remains well positioned to strengthen its competitive position and deliver continued profitable growth in Enterprise."

Consumer Segment Results

•
Revenue was $79.6 million, down 9.4% year over year

•
Non-GAAP gross margin was 27.3%, down 210 basis points year over year

•
Non-GAAP contribution margin was (2.2)%, down 590 basis points year over year

Mr. Prober continued, "In Consumer, we continued to execute our transformation with discipline, prioritizing gross profit in core home networking while managing the service provider business for value as we navigate the memory-cost environment. Although revenue remained constrained, the recurring revenue component of our home networking business continued to perform well, driving 15% year-over-year growth in annual recurring revenue. At the same time, the in-house software development capabilities we have built are reducing our reliance on outside partners and strengthening our ability to deliver differentiated products and services. With an experienced leadership team, a more efficient operating model, continued innovation and regulatory tailwinds, we remain optimistic about the long-term growth potential of our Consumer business."

Business Outlook

Mr. Murray continued, "Within Enterprise, we expect continued growth led by the strong demand for our ProAV line of managed switches. On the Consumer side, while we have our broader product portfolio to address the market, we will continue to prioritize gross profit over revenue to mitigate the effect of the rising cost of memory. For Service Provider and related products, we expect revenue to be approximately $22 million, which would be a decline of approximately 19% as compared to the third quarter of 2025. Accordingly, we expect third quarter net revenue to be in the range of $165 million to $175 million. We continue to have visibility of cost impacts for the balance of the year due to the great progress in accessing supply directly from memory manufacturers. In the third quarter we expect the memory impact to continue to be nominal for our Enterprise business given the relatively higher ASPs and margins and the offset provided by our recent price increases. On the Consumer side we expect increased impact from these headwinds, despite mitigation from actions being taken with our channel partners. The memory cost challenge is expanding to other parts of the BOM, and we are also experiencing modest production delays given the tightening environment. All together, we are continuing to expect approximately 200 basis point headwind to our combined gross margin in the second half compared to the first half with the impact skewed to Q3 due to near-term supply constraints. Accordingly, we expect our third quarter GAAP operating margin to be in the range of (12.0)% to (9.0)%, and non-GAAP operating margin to be in the range of (3.0)% to 0.0%. Our GAAP tax expense is expected to be in the range of $0.5 million to $1.5 million, and our non-GAAP tax expense is expected to be in the range of $1.0 to $2.0 million for the third quarter of 2026."

A reconciliation between the Business Outlook on a GAAP and non-GAAP basis is provided in the following table:

Three months ending
September 27, 2026
(In millions, except for percentage data) | Operating Margin Rate | Tax Expense
GAAP | (12.0)% - (9.0)% | $0.5-$1.5
Estimated adjustments for 1 :
Stock-based compensation expense | 5.8% | -
Amortization of intangible assets | 0.8% | -
Restructuring and other charges | 2.4% | -
Non-GAAP tax adjustments | - | 0.5
Non-GAAP | (3.0)% - 0.0% | $1.0 - $2.0

1 Business outlook does not include estimates for any currently unknown income and expense items which, by their nature, could arise late in a quarter, including: litigation reserves, net; acquisition-related charges; impairment charges; restructuring and other charges and discrete tax benefits or detriments that cannot be forecasted (e.g., windfalls or shortfalls from equity awards or items related to the resolution of uncertain tax positions). New material income and expense items such as these could have a significant effect on our guidance and future GAAP results.

Investor Conference Call / Webcast Details

NETGEAR will review the second quarter results and discuss management's expectations for the third quarter of 2026 today, Thursday, August 6, 2026 at 5 p.m. ET (2 p.m. PT). The toll-free dial-in number for the live audio call is (833) 461-5787. The international dial-in number for the live audio call is (585) 542-9983. The conference ID for the call is 839 828 152. A live webcast of the conference call will be available on NETGEAR's Investor Relations website at http://investor.netgear.com. A replay of the call will be available via the web at http://investor.netgear.com.

About NETGEAR, Inc.

Founded in 1996 and headquartered in the USA, NETGEAR® (NASDAQ: NTGR) is a global leader in innovative networking technologies for businesses, homes, and service providers. NETGEAR delivers a wide range of award-winning, intelligent solutions designed to unleash the full potential of connectivity and power extraordinary experiences. For businesses, NETGEAR offers reliable, easy-to-use, high-performance networking solutions, including switches, routers, access points, software, and AV over IP technologies, tailored to meet the diverse needs of small and medium enterprises.

© 2026 NETGEAR, Inc. NETGEAR and the NETGEAR logo are trademarks or registered trademarks of NETGEAR, Inc. and its affiliates in the United States and/or other countries. Other brand and product names are trademarks or registered trademarks of their respective holders. The information contained herein is subject to change without notice. NETGEAR shall not be liable for technical or editorial errors or omissions contained herein. All rights reserved.

Source: NETGEAR-F

Contact:

NETGEAR Investor Relations

Erik Bylin

investors@netgear.com

Other items consist of certain items that are the result of either unique or unplanned events, including, when applicable: acquisition related expenses, restructuring and other charges, litigation reserves, net, and gain/loss on investments and others. It is difficult to predict the occurrence or estimate the amount or timing of these items in advance. Although these events are reflected in our GAAP financial statements, these unique transactions may limit the comparability of our on-going operations with prior and future periods. The amounts result from events that often arise from unforeseen circumstances, which often occur outside of the ordinary course of continuing operations. Therefore, the amounts do not accurately reflect the underlying performance of our continuing business operations for the period in which they are incurred.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-13_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Business Overview

The enterprise, consumer, and service provider markets are intensely competitive and subject to rapid technological change. We expect competition to continue to intensify. We believe that the principal competitive factors

in the business, consumer, and service provider markets for networking products include product breadth, price points, brand name, security and privacy, performance, features, functionality and reliability, product availability, timeliness of new product introductions, size and scope of the sales channel, ease-of-installation, maintenance and use, and customer service and support. We seek to differentiate our offerings through integrated hardware and software solutions, partner relationships, centralized management capabilities, and services. To remain competitive, we focus on investing in differentiated connectivity solutions across a range of performance tiers, complemented by subscription-based services, expanding and supporting our sales channels, strengthening engagement with customers and partners, and maintaining a high level of customer satisfaction. Our investments align with our strategic priorities, including investments in enterprise and Pro AV initiatives and selective acquisitions intended to enhance software and security capabilities.

We sell our products through multiple sales channels worldwide, including traditional and online retailers, wholesale distributors, direct market resellers ("DMRs"), managed service providers ("MSPs"), broadband service providers, and through our direct online store at www.netgear.com. Our main wholesale distributors include Ingram Micro, TD Synnex, and D&H Distribution Company. Our retail channel includes traditional and online retail locations both domestically and internationally, such as Amazon.com (worldwide), Best Buy, Wal-Mart, Staples, Office Depot, Target, Electra (Sweden), Fnac Darty (Europe), JB HiFi (Australia), Elkjop (Norway), and Boulanger (France). Our DMRs include CDW Corporation, Insight Corporation, and PC Connection in domestic markets. In addition, we also sell products directly to broadband service providers in the United States and internationally providing WiFi, cable and 4G/5G mobile broadband products. Some of these retailers and broadband service providers purchase directly from us, while others are fulfilled through wholesale distributors around the world. A substantial portion of our net revenue is derived from a limited number of wholesale distributors, service providers and retailers. While we expect these channels to continue to be a significant part of our sales strategy, increasingly, customers are choosing to purchase products and services directly from us. We expect revenue through our direct online store or in-app offerings to continue to increase as a percentage of overall revenue for the foreseeable future.

Financial Overview

During the year ended December 31, 2025, our net revenue increased by $25.9 million, compared to the prior year, mainly driven by an increase of $54.2 million in our Enterprise segment, partially offset by a decrease of $28.4 million in our Consumer segment. The year-over-year increase in Enterprise net revenue was primarily attributable to continued strong demand for our Pro AV product line of managed switches, which experienced double-digit end-market sales growth, driven by higher average selling prices and increased unit volumes. The decrease in Consumer net revenue was primarily driven by lower net revenue in the service provider channel. Our gross margin percentage increased by 890 basis points, compared to the prior year, primarily attributable to a favorable product mix weighted toward Enterprise, which generally carry higher gross margin, lower inventory costs resulting from the depletion of older, and higher-cost inventory, reduced sales returns, and lower charges for excess and obsolete inventory. The prior year operating income included a $92.7 million contra-expense recognized in litigation reserves related to the successful settlement of TP-Link litigation, as well as a $10.9 million reduction in general and administrative expenses to offset related legal fees. Excluding these items, the prior year would have reflected an operating loss of $91.4 million, compared to an operating loss of $34.2 million in 2025.

Geographically, net revenue from Enterprise increased in all three regions, whereas net revenue from Consumer decreased in all three regions, during the year ended December 31, 2025, compared to the prior year.

Global Events Affecting our Business and Operations

Macroeconomic and geopolitical trends have continued to create uncertainty in the global economic environment. Contributing factors include persistent inflation, elevated interest rates, foreign exchange rate fluctuations, particularly involving the U.S. dollar, and ongoing trade policy shifts, including tariffs related to the U.S. and key international countries as well as U.S. tariffs and intensified trade actions. Trade policy uncertainty, including the potential for expanded or modified tariff regimes, continues to affect global commerce and supply chain planning. Geopolitical tensions and episodic maritime security incidents, to the extent that disrupt global shipping routes, along with evolving supply chain disruptions and volatile ocean freight spot rates, have added complexity to the global operating environment. Ongoing geopolitical conflicts and regional instability, including disruptions affecting key global shipping routes, have contributed to continued volatility in logistics, freight availability, and transportation

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The following table sets forth, for the periods presented, the consolidated statements of operations data, which is derived from the accompanying consolidated financial statements:

Year Ended December 31,
(In thousands, except percentage data) | 2025 | 2024 | 2023
Net revenue | 699,621 | 100.0% | $673,759 | 100.0% | 740,840 | 100.0%
Cost of revenue | 433,430 | 62.0% | 477,832 | 70.9% | 491,588 | 66.4%
Gross profit | 266,191 | 38.0% | 195,927 | 29.1% | 249,252 | 33.6%
Operating expenses:
Research and development | 85,721 | 12.3% | 81,082 | 12.0% | 83,295 | 11.2%
Sales and marketing | 127,733 | 18.2% | 123,694 | 18.4% | 127,778 | 17.4%
General and administrative | 78,916 | 11.3% | 63,468 | 9.4% | 66,243 | 8.9%
Litigation reserves, net | 209 | 0.0% | (89,012) | (13.2)% | 178 | 0.0%
Restructuring and other charges | 7,764 | 1.1% | 4,479 | 0.7% | 3,962 | 0.5%
Intangible assets impairment | — | —% | — | —% | 1,071 | 0.1 %
Total operating expenses | 300,343 | 42.9% | 183,711 | 27.3% | 282,527 | 38.1%
Income (loss) from operations | (34,152) | (4.9)% | 12,216 | 1.8% | (33,275) | (4.5)%
Other income, net | 17,376 | 2.5% | 12,672 | 1.9% | 14,139 | 1.9%
Income (loss) before income taxes | (16,776) | (2.4)% | 24,888 | 3.7% | (19,136) | (2.6)%
Provision for income taxes | 1,147 | 0.2% | 12,525 | 1.9% | 85,631 | 11.5%
Net income (loss) | (17,923) | (2.6)% | $12,363 | 1.8% | (104,767) | (14.1)%

Net Revenue by Geographic Region

Our net revenue consists of gross product shipments and service revenue, less allowances for estimated sales returns, price protection, end-user customer rebates and other channel sales incentives deemed to be a reduction of revenue per the authoritative guidance for revenue recognition, and net changes in deferred revenue.

For reporting purposes, revenue is generally attributed to each geographic region based upon the location of the customer.

Year Ended December 31,
(In thousands, except percentage data) | 2025 | % Change | 2024 | % Change | 2023
Americas | 476,020 | 4.4% | 456,040 | (9.6)% | 504,349
Percentage of net revenue | 68.0 % | 67.7 % | 68.1 %
EMEA | 139,602 | 9.7% | 127,260 | (14.5)% | 148,922
Percentage of net revenue | 20.0 % | 18.9 % | 20.1 %
APAC | 83,999 | (7.1)% | 90,459 | 3.3% | 87,569
Percentage of net revenue | 12.0 % | 13.4 % | 11.8 %
Total net revenue | 699,621 | 3.8% | 673,759 | (9.1)% | 740,840

2025 vs 2024

Americas

Net revenue in Americas increased in the year ended December 31, 2025, primarily attributable to an increase of 22.5% in Enterprise segment's net revenue, partially offset by a decline of 4.0% in Consumer segment's net revenue compared to the prior year. Enterprise net revenue increased primarily due to higher demand for Pro AV product line of managed switches, in addition to benefitting from inventory optimization efforts with channel partners completed in the first half of the prior year. The decline in Consumer segment's net revenue was mainly due to lower net revenue in the service provider channel.

EMEA

Net revenue in EMEA increased in the year ended December 31, 2025, compared to the prior year, primarily attributable to a 19.6% increase in Enterprise segment's net revenue , partially offset by a 13.2% decrease in Consumer segment net revenue. The net revenue increase in Enterprise was mainly driven by continued strong demand for the Pro AV product line of managed switches in addition to benefitting from inventory optimization efforts with channel partners completed in the first half of the prior year. The decline in Consumer segment's net revenue was mainly due to lower net revenue in both the retail and the service provider channels.

APAC

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-13_item1_business.md)

Item 1. B usiness

General

We are a global provider of networking technologies for businesses, homes, and service providers. We deliver a wide range of networking hardware, software, and services designed to enable reliable connectivity and security.

Our purpose is to power extraordinary experiences, and our mission is to unleash the full potential of connectivity with intelligent solutions that delight and protect. As part of the ongoing development of our business, we are executing a multi-phase transformation to strengthen execution, reinforce our core businesses, and support long-term growth and margin expansion, while exercising strong operational discipline. The first phase of this transformation, which began in 2024, has been completed and focused on establishing foundational capabilities, including organizational alignment, capital allocation priorities, and operational processes. The second phase, which we are now entering, is focused on strengthening our core businesses through improved execution across product development, go-to-market activities, and cost structure. Subject to market conditions and business performance, a subsequent phase is expected to focus on accelerating growth initiatives, including selective inorganic opportunities.

In the first quarter of 2025, we realigned our business structure by separating the previously disclosed Connected Home segment into two reportable segments: Home Networking and Mobile. Effective January 1, 2025, we operated and reported in three segments for the first three fiscal quarters of 2025: NETGEAR for Business, Home Networking, and Mobile. Beginning on the first day of the fourth fiscal quarter of 2025, we streamlined our operating and reporting structure and returned to two reportable segments: Enterprise (formerly NETGEAR for Business) and Consumer (formerly Connected Home), with Consumer comprising the former Home Networking and Mobile businesses. These realignments align our financial reporting more closely with our then and go-forward business strategy and customer focus. Refer to the Note 12, Segment Information, in Notes to Consolidated Financial Statements in Item 8 of Part II of this Annual Report on Form 10-K for additional information. The Enterprise segment focuses on small and medium

enterprises and provides solutions for audio and video over Ethernet for AV applications, enterprise networking solutions, including wireless local area network ("LAN") and cloud-managed networking capabilities, software platforms for deployment and remote management, and security offerings, including firewall and secure access service edge ("SASE") functionality, designed to address the networking, security, and manageability requirements of organizations seeking reliable and cost-effective connectivity solutions. The Consumer segment focuses on consumers and provides high-performance, dependable and easy-to-use WiFi internet networking solutions such as multi-band WiFi 7 mesh systems and routers, subscription services offering performance, security, privacy and support, and 4G/5G mobile products, including WiFi 7 and WiFi 6/6E-enabled portable mobile hotspots and mobile routers, designed to address the demand for reliable, high-speed connectivity at home and on the go. We conduct business across three geographic territories: Americas; Europe, Middle East and Africa ("EMEA"); and Asia Pacific ("APAC").

In the years ended December 31, 2025, 2024, and 2023, we generated net revenue of $699.6 million, $673.8 million, and $740.8 million, respectively.

Markets

Our mission is to unleash the full potential of connectivity with intelligent solutions that delight and help protect businesses, consumers, and service providers. Demand for networking solutions continues to be driven by the need for reliable, high-speed connectivity, increasing device density, and growing requirements for security and manageability across a broad range of environments.

The professional audio and video ("AV") market continues to expand as organizations increase the use of digital displays, video walls, conferencing systems, and other video-intensive applications. As video formats evolve to higher resolutions and greater pixel density, AV deployments require increased network capacity, reliability, and predictable performance. The AV industry is also transitioning from legacy, matrix-based switching architectures to IP-based networking solutions, which offer greater scalability, flexibility, and cost efficiency. While AV systems are increasingly built on IP infrastructure, we design our solutions to simplify IP network setup for AV integrator partners. As a result, networking has become a critical component of modern AV system design, increasing demand for solutions that simplify deployment and support the timing-sensitive requirements of AV traffic.

Small and medium enterprises ("SMEs") rely on their networks to support mission-critical operations across environments such as education, hospitality, multi-dwelling units, and distributed business locations. These organizations face increasing network complexity driven by growing numbers of connected devices, new applications, and evolving usage patterns, while often operating with limited internal IT resources and constrained budgets. As a result, many SMEs depend on managed service providers for networking and security support. Consequently, demand continues to grow for networking and security solutions that balance reliability, security, ease of deployment, and cost effectiveness, including wireless and wired networking upgrades, cloud-managed networking capabilities, and security solutions such as firewall and SASE functionality.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-13_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-13_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-13_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-02-13_item7_mdna.md, 10-K_2026-02-13_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
