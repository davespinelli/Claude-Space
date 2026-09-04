# Triage pack — GOGO · Gogo Inc.

_Generated 2026-09-04 14:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** GOGO · **Name:** Gogo Inc.
- **CIK:** 0001537054
- **SIC:** 4899 — Communications Services, NEC
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/GOGO

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Gogo Inc.
- **CIK:** 1,537,054 · **SIC:** 4899 (Communications Services, NEC) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 2.65 |
| mktcap | $359.1M |
| ev | $1.1B |
| ev_ebit | 9.7x |
| fcf | $65.1M |
| fcf_yield | 18.1% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 10.3% |
| net_debt | $750.9M |
| net_debt_ebit | 6.6x |
| cash | $63.1M |
| ltd | $814.1M |
| equity | $120.7M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $910.5M |
| revenue_prior | $444.7M |
| rev_growth | 104.7% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $114.1M |
| net_income | $12.9M |
| cfo | $124.5M |
| capex | $59.4M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 1.4% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 135,507,862 |
| shares_py | 133,685,225 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -58.4% |
| r6m | -50.5% |
| off_52w_high | -75.4% |
| adv20 | $6.0M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.87 |
| r_ev_ebit | 0.78 |
| r_roic | 0.71 |
| r_rev_growth | 0.98 |
| r_buyback | 0.40 |
| score | 0.65 |

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
| rank | 101 |

**Screen rationale:** top-quartile FCF yield 18.1%; cheap at 9.7x EV/EBIT; revenue +104.7%; WARNING 6m return below -40%


## 3. Share count trend

- Shares outstanding: **135,507,862** (CY2026Q2I) vs **133,685,225** prior year (CY2025Q2I)
- Change: **1.4%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-17** — Item 5.02 (officer / director change or comp arrangement): On July 15, 2026, Hayden Olson transitioned from EVP, General Manager, SD Government of Gogo Inc. (the "Company") to EVP, Corporate Development.
- **2026-06-02** — Item 5.02 (officer / director change or comp arrangement): The board of directors of Gogo Inc. (the "Company") previously adopted, subject to stockholder approval the Amended and Restated 2024 Omnibus Equity Incentive Plan (the "A&R 2024 Plan"), which amends and restates the Company's 2024 Omnibus Equity Incentive...

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 16 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 10 |
| F | 2 |
| M | 4 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'GOGO ANNOUNCES SECOND QUARTER RESULTS'; skipped 10 forward-looking-statement block(s); 6 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (gogo-ex99_1.htm)

GOGO ANNOUNCES SECOND QUARTER RESULTS

Total Revenue of $222.8 million;

Service Revenue of $191.3 million, up 2% sequentially

Military / Government service revenue of $39.9 million, up 40% compared to Q2 2025 and 20% sequentially

Net loss of $2.0 million, Adjusted EBITDA 1 of $53.7 million, up approximately 1% sequentially

Gogo Galileo and 5G Expected to Ramp in 2H 2026

BROOMFIELD, Colo. - August 6, 2026 – Gogo Inc. (NASDAQ: GOGO) ("Gogo" or the "Company"), a leading global provider of broadband connectivity services for the business and military/government aviation markets, today announced its financial results for the quarter ended June 30, 2026.

"Our second quarter results show continued momentum in Gogo's transformation into a global provider of high-speed broadband to the business and military/government aviation markets," said Chris Moore, CEO of Gogo. "Our military and government business delivered a record quarter, with service revenue up 40% year over year, driven by ongoing demand for secure airborne connectivity, providing a durable revenue base. Our next-generation product transition is well under way, which we expect to be driven by the continued scaling of Galileo and 5G."

Zac Cotner, CFO of Gogo, commented, "Our second quarter financial results came in line with our expectations, supported by a particularly strong performance with our military and government customers. We continue to see expansion across that customer segment, which grew 20% sequentially and will continue to be both a stabilizer and growth engine for the future. Our results reflect disciplined execution across the business, which along with debt reduction, remain our highest financial priorities over the next several quarters."

Q2 2026 Financial Highlights

•
Total revenue of $222.8 million decreased 1% compared to Q2 2025 and 2% compared to Q1 2026.

Equipment Revenue

o
Equipment revenue of $31.5 million decreased 2% compared to Q2 2025 and 18% compared to Q1 2026.

o
Q2 equipment units shipped for Gogo Galileo, Gogo's new cutting-edge Low Earth Orbit ("LEO") satellite broadband service, totaled 108, up 17% compared to Q1 2026. Cumulative Gogo Galileo equipment shipments reached 518 units.

o
Total ATG equipment units sold in Q2 2026 totaled 297, down 27% compared to Q2 2025 and 42% compared to Q1 2026.

▪
Gogo 5G unit shipments continue to ramp, with 138 units sold in Q2 2026, up from 52 units sold in Q1 2026.

Service Revenue

o
Service revenue of $191.3 million decreased 1% compared to Q2 2025 and increased 2% compared to Q1 2026.

▪
Business aviation service revenue of $151.3 million decreased 8% compared to Q2 2025 and 2% compared to Q1 2026.

▪
Military / Government service revenue of $39.9 million increased 40% compared to Q2 2025 and 20% compared to Q1 2026.

•
Aircraft online ("AOL") as of June 30, 2026:

o
Total ATG AOL 2 of 5,731 decreased 15% versus Q2 2025 and 6% versus Q1 2026.

▪
ATG AVANCE AOL of 4,603 decreased 4% compared to June 30, 2025 and decreased 5% compared to March 31, 2026.

▪
ATG C-1 AOL of 690 increased 24% from 557 as of March 31, 2026.

o
Broadband GEO AOL of 1,306 decreased 1% compared to June 30, 2025 and was flat compared to March 31, 2026.

o
Gogo Galileo AOL of 184 increased 66% from 111 as of March 31, 2026.

•
Net Income (loss) for the quarter was ($2.0) million, compared to $12.8 million in Q2 2025 and $13.1 million in Q1 2026.

•
Adjusted EBITDA 1 of $53.7 million decreased 13% compared to Q2 2025 and increased approximately 1% compared to Q1 2026. Adjusted EBITDA includes $3.2 million of expense incurred in the quarter for ongoing litigation matters.

•
Net cash provided by (used in) operating activities was $32.3 million in Q2 2026, down from $36.7 million in Q2 2025 and up from $(7.2) million in Q1 2026.

•
Free Cash Flow 1 of $21.6 million in Q2 2026 was down from $33.5 million in Q2 2025 and up from $(19.2) million in Q1 2026.

•
Cash and cash equivalents was $63.1 million as of June 30, 2026, compared to $103.5 million as of March 31, 2026 and $102.1 million as of June 30, 2025. During Q2 2026, the Company made a $40.0 million earn-out payment related to the company's earlier purchase of Satcom Direct and a $21.1 million principal payment on the HPS term loan facility, both of which are excluded from Free Cash Flow.

Recent Developments

•
Galileo HDX has earned FAA and EASA certification via Dassault Falcon Jet for installation on Falcon 7X and 8X aircraft, expanding global, high-speed LEO connectivity paired with Gogo's robust cybersecurity protections to these leading long-range business jets.

•
Gogo secured a $7.5 million multi-year contract with NOAA's Aircraft Operations Center to provide mission-critical SATCOM, cybersecurity and cockpit datalink software for the "Hurricane Hunter" research fleet.

•
Airshare is equipping its Embraer Phenom 300 fleet with Gogo Galileo HDX and AVANCE L5 to provide high-speed, multi-device streaming and video conferencing for passengers and crew. Gogo Galileo HDX remains the only line-fit option for the Phenom 300, one of the most popular light jets on the market.

•
SD Government, a subsidiary of Gogo, Pilatus, and Pro Star Aviation achieved FAA Supplemental Type Certificates ("STC") approval to install Gogo Galileo HDX on Pilatus PC-12 turboprops, delivering high-speed LEO internet for special missions, defense, MEDEVAC and private operators globally.

•
Gulfstream received STC certification for all tail-mounted Gogo Galileo HDX installations on G650 and G650ER aircraft, both leading large-cabin jets.

•
Gogo anticipates beginning HDX and 5G demonstrations for the Pilatus PC-24, a leading light business jet. The HDX demonstrations are tentatively scheduled to start in mid-August and the 5G in late October.

Updates 2026 Financial Guidance

Gogo is updating its financial guidance previously provided in May.

•
Total revenue in the range of $870 million to $895 million, split ~84% service revenue and ~16% equipment revenue.

•
Adjusted EBITDA 1 in the range of $175 million to $185 million, which includes $5 million in strategic investments and $22 million of ongoing litigation expense, up from $8 million of litigation expense included in the prior guidance.

•
Free Cash Flow 1 in the range of $65 million to $85 million, including the aforementioned updated expense for ongoing litigation and $30 million slated for strategic investments in 2026, net of any FCC reimbursement.

•
Net capital expenditures of $20 million. This assumes $45 million in reimbursement from the FCC Reimbursement Program.

1 See "Non-GAAP Financial Measures" below.

2 See "Key Business Metrics" below.

Conference Call

The Company will host its second quarter conference call on August 6, 2026 at 8:30 a.m. ET. A live webcast of the conference call, as well as a replay, will be available online on the Investor Relations section of the Company's investor website at https://ir.gogoair.com .

Q2 Earnings Call Webcast Link: https://edge.media-server.com/mmc/p/czisjqz9

Participants can use the below link to retrieve your unique conference ID to use to access the conference call.

https://register-conf.media-server.com/register/BIc1371241a7b64561b1ebf76042a13f3b

Non-GAAP Financial Measures

We report certain non-GAAP financial measurements, including Adjusted EBITDA and Free Cash Flow in the discussion above. Management uses Adjusted EBITDA and Free Cash Flow for business planning purposes, including managing our business against internally projected results of operations and measuring our performance and liquidity. These supplemental performance measures also provide another basis for comparing period-to-period results by excluding potential differences caused by non-operational and unusual or non-recurring items. These supplemental performance measurements may vary from and may not be comparable to similarly titled measures used by other companies. Adjusted EBITDA and Free Cash Flow are not recognized measurements under accounting principles generally accepted in the United States, or GAAP. When analyzing our performance with Adjusted EBITDA or liquidity with Free Cash Flow, as applicable, investors should (i) evaluate each adjustment in our reconciliation to the corresponding GAAP measure, and the explanatory footnotes regarding those adjustments, (ii) use Adjusted EBITDA in addition to, and not as an alternative to, net income (loss) attributable to common stock as a measure of operating results, and (iii) use Free Cash Flow in addition to, and not as an alternative to, consolidated net cash provided by (used in) operating activities when evaluating our liquidity. No reconciliation of the forecasted amounts of Adjusted EBITDA for fiscal 2026 is included in this release because we are unable to quantify certain amounts that would be required to be included in the corresponding GAAP measure without unreasonable efforts, due to high variability and complexity with respect to estimating certain forward-looking amounts, and we are therefore unable to estimate the probable significance of such amounts. We believe such reconciliation would imply a degree of precision that would be confusing or misleading to investors.

Key Business Metrics

Our management regularly reviews financial and business metrics, including the key business metrics in this press release under "Supplemental Information - Key Business Metrics," to evaluate the performance of our business and our success in executing our business plan, make decisions regarding resource allocation and corporate strategies, and evaluate forward-looking projections. Certain of these business metrics may be added, removed or updated from time to time as our business evolves.

(in thousands, except per share amounts)

For the Three Months Ended June 30, | For the Six Months Ended June 30,
2026 | 2025 | 2026 | 2025
Revenue:
Service revenue | 191,272 | 193,965 | 379,004 | 392,577
Equipment revenue | 31,539 | 32,073 | 70,126 | 63,768
Total revenue | 222,811 | 226,038 | 449,130 | 456,345
Operating expenses:
Cost of service revenue (exclusive of amounts shown below) | 98,110 | 91,383 | 196,424 | 185,430
Cost of equipment revenue (exclusive of amounts shown below) | 31,100 | 27,681 | 66,088 | 57,007
Engineering, design and development | 9,667 | 12,522 | 16,159 | 26,397
Sales and marketing | 13,286 | 14,741 | 26,777 | 28,951
General and administrative | 23,989 | 28,633 | 50,197 | 58,152
Depreciation and amortization | 17,009 | 15,117 | 32,148 | 29,260
Total operating expenses | 193,161 | 190,077 | 387,793 | 385,197
Operating income | 29,650 | 35,961 | 61,337 | 71,148
Other expense (income):
Interest income | (685 | (1,182 | (1,839 | (1,772
Interest expense | 17,593 | 16,411 | 34,439 | 32,969
Change in fair value of Earnout Liability | 7,200 | 3,900 | 2,257 | 3,900
Loss on extinguishment of debt | 394 | — | 394 | —
Other expense (income), net | (1,622 | (149 | (1,717 | 85
Total other expense | 22,880 | 18,980 | 33,534 | 35,182
Income before income taxes | 6,770 | 16,981 | 27,803 | 35,966
Income tax provision | 8,779 | 4,174 | 16,727 | 11,117
Net income (loss) | (2,009 | 12,807 | 11,076 | 24,849
Net income (loss) attributable to common stock per share:
Basic | (0.01 | 0.10 | 0.08 | 0.19
Diluted | (0.01 | 0.09 | 0.08 | 0.18
Weighted average number of shares:
Basic | 136,250 | 133,647 | 135,961 | 132,925
Diluted | 136,250 | 136,897 | 136,890 | 135,971

Gogo Inc. and Subsidiaries

Unaudited Condensed Consolidated Balance Sheets

(in thousands)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-27_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Company Overview

The Company is the only multi-orbit, multi-band in-flight connectivity provider offering connectivity technology purpose-built for business and military/government aviation. We have a holistic approach of providing broadband connectivity services to our customers from small to large aircraft and heavy jets through our ATG technology and integrated LEO and GEO satellite solutions provided by multiple satellite constellations owned by our satellite network partners. We aim to deliver to our customers consistent, global tip-to-tail connectivity with a suite of software, hardware, and advanced infrastructure supported by a 24/7/365 in-person customer support team to fit their every need.

Our Company's chief operating decision maker ("CODM"), who is the Chief Executive Officer, makes resource and operating decisions by evaluating the performance and business results on a consolidated basis. As we do not have multiple segments, we do not present segment information in this Annual Report on Form 10-K.

Factors and Trends Affecting Our Results of Operations

We believe that our operating and business performance is driven by various factors that affect the business and military/government aviation industries, including trends affecting the travel industry and trends affecting the customer bases that we target, as well as factors that affect wireless Internet service providers and general macroeconomic factors. Key factors that may affect our future performance include:

•
our ability to implement on a timely basis and costs associated with the ongoing implementation of our technology roadmap, including installation of and/or upgrades to the ATG Broadband technologies we currently offer, Gogo 5G, Gogo Galileo, LTE and any other next generation or other new technology that we develop or acquire;

•
our ability to manage issues and related costs that may arise in connection with the implementation of our technology roadmap, including technological issues and related remediation efforts and technological shifts, failures or delays on the part of antenna, chipset, and other equipment developers and providers or satellite network providers, some of which are single-source;

•
our ability to license additional spectrum and make other improvements to our ATG network and operations as technology and user expectations change;

•
the number of aircraft in service in our markets, including consolidations or changes in fleet size by one or more of our large-fleet customers;

•
the economic environment and other trends that affect both business and leisure aviation travel;

•
disruptions to supply chains in the aviation industry and installations of our equipment driven by, among other things, labor shortages;

•
the extent of our customers' adoption of our products and services, which is affected by, among other things, willingness to pay for the services that we provide, the quality and reliability of our products and services, changes in technology and competition from current competitors and new market entrants;

•
our ability to engage suppliers of equipment components and network services on a timely basis and on commercially reasonable terms;

•
our ability to fully utilize portions of our deferred income tax assets;

•
changes in laws, regulations, policies and interpretations affecting our business, the business of our customers and suppliers globally, including changes that impact the design of our equipment and our ability to obtain required

certifications for our equipment and services, and telecommunications services globally, including those affecting our ability to maintain our licenses for ATG spectrum in the United States, obtain sufficient rights to use additional ATG spectrum and/or other sources of broadband connectivity to deliver our services, including Gogo Galileo and Gogo 5G, and expand our service offerings and manage our network; and

•
the enactment of, and proposals for, trade protection measures by the United States as well as other countries (including United States "reciprocal" tariffs that began in April 2025), including increases or changes in tariffs and trade barriers, changes in government policies and international trade arrangements, geopolitical volatility, and global macroeconomic conditions, or uncertainty regarding the impact of proposed or future trade protection measures, may affect our results of operations in some markets.

Key Business Metrics

Our management regularly reviews financial and operating metrics, including the following key operating metrics, to evaluate the performance of our business and our success in executing our business plan, make decisions regarding resource allocation and corporate strategies, and evaluate forward-looking projections. Certain of these business metrics may be added, removed or updated from time to time as our business evolves.

For the Years Ended December 31,
2025 | 2024 | 2023
ATG aircraft online (at period end)
AVANCE | 4,956 | 4,608 | 3,976
Gogo Biz | 1,446 | 2,451 | 3,229
Total ATG | 6,402 | 7,059 | 7,205
GEO aircraft online | 1,321 | 1,249 | 10
Gogo Galileo aircraft online | 74 | — | —
Average monthly connectivity service revenue per ATG aircraft online | 3,421 | 3,481 | 3,380
ATG units sold | 1,631 | 911 | 894

•
AVANCE aircraft online. We define AVANCE aircraft online as the total number of business aircraft equipped with our AVANCE L5 or L3 system for which we provide ATG services in the last month of the period presented.

•
Gogo Biz aircraft online. We define Gogo Biz aircraft online as the total number of business aircraft not equipped with our AVANCE L5 or L3 system for which we provide ATG services in the last month of the period presented. This number excludes commercial aircraft operated by Intelsat's airline customers receiving ATG service.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The following table sets forth, for the periods presented, certain data from our consolidated statements of operations. The information contained in the table below should be read in conjunction with our consolidated financial statements and related notes. The acquisition of Satcom Direct was completed in the fourth quarter of 2024, and as a result, its results of operations are not reflected in our financial statements prior to such date.

Consolidated Statements of Operations

(in thousands)

For the Years Ended December 31,
2025 | 2024 | 2023
Revenue:
Service revenue | 774,393 | 364,270 | 318,015
Equipment revenue | 136,098 | 80,439 | 79,562
Total revenue | 910,491 | 444,709 | 397,577
Operating expenses:
Cost of service revenue (exclusive of items shown below) | 372,728 | 99,042 | 69,568
Cost of equipment revenue (exclusive of items shown below) | 134,676 | 67,561 | 63,383
Engineering, design and development | 56,143 | 44,772 | 36,683
Sales and marketing | 55,841 | 38,020 | 29,797
General and administrative | 116,741 | 125,071 | 57,280
Depreciation and amortization | 60,279 | 18,972 | 16,701
Total operating expenses | 796,408 | 393,438 | 273,412
Operating income | 114,083 | 51,271 | 124,165
Other expense (income):
Interest income | (4,676 | (8,336 | (7,403
Interest expense | 68,217 | 38,431 | 33,056
Change in fair value of earnout liability | 11,800 | — | —
Loss on extinguishment of debt | — | — | 2,224
Other (income) expense, net | 11,930 | 3,042 | (1,315
Total other expense | 87,271 | 33,137 | 26,562
Income before income taxes | 26,812 | 18,134 | 97,603
Income tax provision (benefit) | 13,889 | 4,388 | (48,075
Net income | 12,923 | 13,746 | 145,678

Comparison of Years Ended December 31, 2025 and 2024

Below is a discussion of changes in the results in operations for the years ended 2025 and 2024.

Revenue

Revenue and percent change for the years ended December 31, 2025 and 2024 were as follows (in thousands, except for percent change) :

For the Years Ended
December 31, | % Change
2025 | 2024 | 2025 over 2024
Service revenue | 774,393 | 364,270 | 112.6 | %
Equipment revenue | 136,098 | 80,439 | 69.2 | %
Total revenue | 910,491 | 444,709 | 104.7 | %

Total revenue increased to $910.5 million for the year ended December 31, 2025, as compared with $444.7 million for the prior year.

Service revenue increased to $774.4 million for the year ended December 31, 2025, as compared with $364.3 million for the prior year, due to the current year including service revenue earned as a result of the acquisition of Satcom Direct.

Equipment revenue increased to $136.1 million for the year ended December 31, 2025, as compared with $80.4 million for the prior year, due to an increase in equipment revenue earned as a result of the acquisition of Satcom Direct of $26.2 million and an increase of $21.4 million due to Gogo Galileo shipments.

We expect service revenue to decline in the near term as a result of the expected decline in ATG services sold and increase in the future as additional aircraft come online for Gogo 5G and Gogo Galileo. We expect equipment revenue to increase in the future driven by growth in sales of Gogo 5G and Gogo Galileo units.

Cost of Revenue

Cost of service revenue and percent change for the years ended December 31, 2025 and 2024 were as follows (in thousands, except for percent change) :

For the Years Ended
December 31, | % Change
2025 | 2024 | 2025 over 2024
Cost of service revenue | 372,728 | 99,042 | 276.3 | %
Cost of equipment revenue | 134,676 | 67,561 | 99.3 | %

Cost of service revenue increased 276.3% to $372.7 million for the year ended December 31, 2025, as compared with $99.0 million for the prior year, due to the current year including cost of service revenue as a result of the acquisition of Satcom Direct.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-27_item1_business.md)

Item 1. Business

Company Overview

Gogo Inc. ("Gogo", the "Company", "we" or "us") is the only multi-orbit, multi-band in-flight connectivity provider offering connectivity technology purpose-built for business and military/government aviation. We have a holistic approach of providing broadband connectivity services to our customers from small to large aircraft and heavy jets through our air-to-ground ("ATG") technology and integrated low earth orbit ("LEO") and geostationary earth orbit ("GEO") satellite solutions provided by multiple satellite constellations owned by our satellite network partners. We aim to deliver to our customers consistent, global tip-to-tail connectivity with a suite of software, hardware, and advanced infrastructure supported by a 24/7/365 in-person customer support team to fit their every need.

By leveraging our multi-orbit, multi-band in-flight connectivity solutions, our global footprint, including a mature sales force and technical support, we can provide our customers with essential market access, speed, bandwidth, greater reliability, redundancy, and responsiveness that they need around the world. Our connectivity solutions are used by business and military/government aviation customers in over 100 countries, many of which view our products and services as critical to their daily operations and integral to their communications and business infrastructure. We also serve our growing military/government customer base by providing cost-effective, turnkey in-flight connectivity that integrates innovative, commercially proven technologies and software to deliver mission-tailored capabilities.

We believe that, with our innovative solutions and tailored customer service, we are well-positioned to compete in the evolving in-flight connectivity market, which is undergoing significant change driven by several catalysts. The most significant technological advancement that is driving change in our industry today is the introduction of LEO satellite technology, which provides, among other things, a global service offering, higher capacity, and lower latency than currently available alternatives. Further, we believe that demand for in-flight connectivity will continue to increase because of changes in the demographics of our customer base, the proliferation of social applications, and lifestyle changes that remain in a post-COVID world, such as videoconferencing and live streaming.

Acquisition of Satcom Direct, LLC (the "Transaction")

On December 3, 2024 (the "Closing"), we purchased all of the issued and outstanding equity interests of Satcom Direct, LLC, a Delaware limited liability company (f/k/a Satcom Direct, Inc., a Florida corporation) and certain of its affiliates and subsidiaries (collectively, "Satcom Direct"), in exchange for (i) an aggregate cash purchase price of approximately $375,000,000, subject to customary post-closing adjustments, (ii) 5,000,000 restricted shares of the Company's common stock, par value $0.0001 per share (the "Common Stock") (valued at approximately $40,500,000 based on the Company's closing stock price of $8.10 on December 2, 2024), and (iii) up to an additional $225,000,000 in potential earnout payments of cash and/or Common Stock tied to realizing certain financial performance milestones over four years following the Closing.

Our Strategy and our Solutions

Our business strategy is to be a global satellite network integrator and facilitator by developing innovative technological and business solutions addressing the specific needs of our business and military/government customers – making connectivity accessible, available, and secure worldwide. Our technological expertise and deep understanding of the in-flight connectivity market, built over decades of leadership in our industry, places us in a prime position for continued growth over the coming decade.

The following are the primary solutions that enable us to pursue our strategy:

•
Gogo Galileo : We commercially launched the first global LEO broadband satellite service purpose-built for business aviation ("Gogo Galileo") in the first quarter of 2025. Gogo Galileo uses an electronically steered antenna ("ESA"), specifically designed with Hughes Network Systems, LLC ("Hughes") to address a broad range of business aviation and military/government aircraft, operating on a LEO satellite network operated by Network Access Associates, Ltd. ("Eutelsat OneWeb"). We believe that Gogo Galileo, in combination with or as an alternative to our ATG and GEO services, will allow us to penetrate the North American market and provide an upgrade path and an additional product for our existing ATG and GEO customer base. In addition, we believe that Gogo Galileo will allow us to penetrate the business aviation and military/government markets outside of North America, where there has been a lower adoption rate of in-flight connectivity. The launch of Gogo Galileo augments our combined product and service offerings for ATG broadband, GEO broadband, and narrowband satellite services, as described below.

•
ATG Broadband Service : Gogo is the leading provider of in-flight connectivity in the ATG broadband market in North America. Gogo started in analogue ATG technology in the late 1990s, then, as analogue cellular backhaul disappeared, migrated to narrowband satellite connectivity in the early 2000s, and then back to ATG with our digital broadband networks beginning in 2010. We continue to augment our ATG broadband connectivity services through the addition of our fourth ATG broadband network (Gogo 5G), which we launched in the fourth quarter of 2025. We are also actively

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-27_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-27_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-27_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-02-27_item7_mdna.md, 10-K_2026-02-27_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
