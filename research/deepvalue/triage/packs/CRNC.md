# Triage pack — CRNC · Cerence Inc.

_Generated 2026-09-05 02:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** CRNC · **Name:** Cerence Inc.
- **CIK:** 0001768267
- **SIC:** 7372 — Services-Prepackaged Software
- **Fiscal year end (MM-DD):** 09-30
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/CRNC

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Cerence Inc.
- **CIK:** 1,768,267 · **SIC:** 7372 (Services-Prepackaged Software) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 8.49 |
| mktcap | $384.0M |
| ev | $557.5M |
| ev_ebit | n/a |
| fcf | $46.8M |
| fcf_yield | 12.2% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -0.5% |
| net_debt | $173.5M |
| net_debt_ebit | n/a |
| cash | $0.00 |
| ltd | $173.5M |
| equity | $166.4M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $251.8M |
| revenue_prior | $331.5M |
| rev_growth | -24.0% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$2.3M |
| net_income | -$18.7M |
| cfo | $61.2M |
| capex | $14.4M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 4.4% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 45,230,257 |
| shares_py | 43,319,651 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -4.7% |
| r6m | 10.7% |
| off_52w_high | -36.2% |
| adv20 | $6.2M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.78 |
| r_ev_ebit | 0.00 |
| r_roic | 0.29 |
| r_rev_growth | 0.02 |
| r_buyback | 0.20 |
| score | 0.26 |

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
| rank | 440 |

**Screen rationale:** top-quartile FCF yield 12.2%


## 3. Share count trend

- Shares outstanding: **45,230,257** (CY2026Q2I) vs **43,319,651** prior year (CY2025Q2I)
- Change: **4.4%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-02** — Item 5.02 (officer / director change or comp arrangement): On June 28, 2026, Marcy Klevorn notified the Board of Directors (the "Board") of Cerence Inc. (the "Company") of her decision to resign from the Board, effective July 1, 2026.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 25,998 sh / $229,508 -> net $-229,508 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 12 (open-market buys 0, sales 1).

| code | rows |
|---|---|
| A | 11 |
| S | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: no Highlights/Results/quarter heading found; started at the top of the exhibit; skipped 4 forward-looking-statement block(s)._

## EX-99.1 - EX-99.1 (q3fy26cerenceaipressrele.htm)

EX-99.1
q3fy26cerenceaipressrele.htm
EX-99.1

q3fy26cerenceaipressrele

Cerence AI Reports Third Quarter Results: Revenue Up 12% YoY, Connected Services Revenue Up 20% YoY; Operating Cash Flow of $20M Supports First-Ever Share Repurchase Program Headlines • Revenue of $69.6 million and GAAP net income of $1.5 million were within guidance; Adjusted EBITDA of $13.5 million increased 50% year-over-year and exceeded the high end of guidance. Connected Services revenue increased more than 20% year-over-year. • Generated $20 million in operating cash flow and approximately $20 million in free cash flow, up more than 20% YoY. • Expanded AI platform momentum and adoption, including a new multi-brand Cerence xUI award from Stellantis and the first customer win for Cerence's Mobile Work Agent. • Board of Directors authorized the Company's first-ever share repurchase program, permitting repurchases of up to $30 million of common stock over 12 months, reflecting confidence in the business and commitment to disciplined capital allocation. BURLINGTON, Mass., August 6, 2026 – Cerence Inc. (NASDAQ: CRNC) ("Cerence AI"), a global leader pioneering conversational AI-powered user experiences, today reported its third quarter fiscal year 2026 results for the period ended June 30, 2026. The Company also announced that its Board of Directors has authorized the Company's first share repurchase program, pursuant to which the Company may purchase up to $30,000,000 of its outstanding common stock over the next 12 months. "Our third-quarter results demonstrate continued execution across the business, with solid execution, strong cash generation, and momentum across our AI portfolio," said Brian Krzanich, Chief Executive Officer of Cerence AI. "We signed an important multi-brand Cerence xUI award with Stellantis, secured the first customer for our Mobile Work Agent, and saw 20% year-over-year growth in Connected Services revenue. Together with our first-ever share repurchase authorization - which reflects the Board and management's confidence in Cerence AI's strategy, cash generation ability, and long-term value - we believe these results demonstrate our progress in strengthening the business through disciplined execution, innovation, and capital allocation." Krzanich continued, "We continue to build toward a much larger opportunity. As AI continues to be a strategic priority for automakers and increasingly extends into adjacent markets, we believe Cerence AI is uniquely positioned to serve as the interaction layer between people and intelligent systems. We believe that our portfolio of conversational, agentic, and embedded AI solutions, combined with our deep domain expertise, global reach, and long-standing customer relationships, provides a strong foundation for growth as we help customers bring the next generation of AI-powered experiences to life. We look forward to providing additional perspective on our roadmap and long-term growth strategy next quarter." Stock Repurchase Program Under the stock repurchase program, the Company intends to repurchase shares from time to time in the open market in compliance with Rule 10b-18 under the Securities Exchange Act of 1934, pursuant to Rule 10b5-1 trading plans, in privately negotiated transactions, through accelerated share repurchase Cerence Media Relations | press@cerence.com Cerence Investor Relations | cerence@pondel.com

arrangements, purchases, or by other means. The Company may repurchase shares under this program depending on a variety of factors, including, among other things, the impact of dilution from employee stock awards, market conditions, stock price, applicable legal and regulatory requirements, and other factors. Because the program is discretionary, the program does not obligate the Company to acquire any particular number of shares or any specific dollar amount, and there is no assurance as to the timing or amount of any repurchases. The Company intends to fund repurchases under the program primarily with existing cash and cash equivalents and, secondarily, free cash flow generated by operations. Results Summary (1) (in millions, except per share data) Cerence AI delivered third-quarter revenue and net income within its guidance ranges; adjusted EBITDA above the high end of guidance and up 50% year-over-year; and $19.6 million of free cash flow, up more than 20% year-over-year. Revenue increased 12% year-over-year, primarily driven by the timing of fixed license contract execution and growth in Connected Services revenue, which increased more than 20% year-over-year, reflecting continued adoption of the Company's connected solutions. Professional Services revenue was down year-over-year, reflecting the Company's continued focus on standardization and higher-margin implementations. Three Months Ended June 30, Nine Months Ended June 30, 2026 2025 2026 2025 GAAP revenue (2) $ 69.6 $ 62.2 $ 248.9 $ 191.1 GAAP gross margin 76.0 % 73.7 % 80.2 % 72.8 % GAAP total operating expenses (3) $ 51.0 $ 46.8 $ 170.8 $ 139.7 Non-GAAP total operating expenses (3) $ 42.7 $ 39.6 $ 143.2 $ 107.8 GAAP net income (loss) $ 1.5 $ (2.7) $ (2.0) $ (5.4) Adjusted EBITDA $ 13.5 $ 9.0 $ 65.4 $ 39.8 GAAP net cash provided by operating activities $ 20.0 $ 23.7 $ 72.0 $ 48.4 Free cash flow $ 19.6 $ 16.1 $ 68.9 $ 37.1 GAAP net income (loss) per share - diluted $ 0.03 $ (0.06) $ (0.05) $ (0.12) (1) Please refer to the "Discussion of Non-GAAP Financial Measures" and "Reconciliations of GAAP Financial Measures to Non-GAAP Financial Measures" included elsewhere in this release for more information regarding the Company's use of non-GAAP financial measures. (2) Q1FY26 revenue included $49.5 million of IP license revenue related to a previously disclosed agreement with Samsung. Q3FY26 and Q3FY25 revenue included $12.5 million and $0.0 million of revenue from fixed license contracts, respectively. (3) Q1FY26 GAAP and Non-GAAP operating expenses included $20.8 million of expenses related to the Company's previously disclosed agreement with Samsung. Cerence Key Performance Indicators To help investors gain further insight into Cerence AI's business and performance, management provides a set of key performance indicators (KPIs). The Company believes the KPIs for the quarter reflect continued Cerence Media Relations | press@cerence.com Cerence Investor Relations | cerence@pondel.com

Because of varying valuation methodologies, subjective assumptions and the variety of award types, we exclude stock-based compensation from our operating results. We evaluate performance both with and without these measures because compensation expense related to stock-based compensation is typically non-cash and awards granted are influenced by the Company's stock price and other factors such as volatility that are beyond our control. The expense related to stock-based awards is generally not controllable in the short-term and can vary significantly based on the timing, size and nature of awards granted. As such, we do not include such charges in operating plans. Stock-based compensation will continue in future periods. Other expenses. We exclude certain other expenses that result from unplanned events outside the ordinary course of continuing operations, in order to measure operating performance and current and future liquidity both with and without these expenses. By providing this information, we believe management and the users of the financial statements are better able to understand the financial results of what we consider to be our organic, continuing operations. Included in these expenses are items such as other charges (credits), net (gains) losses from extinguishment of debt, net (gains) losses from foreign currency translation, and changes in indemnification assets corresponding with the release of pre-spin liabilities for uncertain tax positions. Non-GAAP total operating expenses. Non-GAAP total operating expenses reflect GAAP operating expenses excluding stock-based compensation, intangible asset amortization, and restructuring and other costs. Our management and Board of Directors use this financial measure to evaluate our operating performance. It is also a significant performance measure in our annual incentive compensation programs. Key Performance Indicators We believe that providing key performance indicators ("KPIs") allows investors to gain insight into the way management views the performance of the business. We further believe that providing KPIs allows investors to better understand information used by management to evaluate and measure such performance. KPIs should not be considered superior to, or a substitute for, operating results prepared in accordance with GAAP. In assessing the performance of the business during the three months ended June 30, 2026, our management has reviewed the following KPIs, each of which is described below: • Percent of worldwide auto production with Cerence Technology (TTM): The number of Cerence enabled cars shipped on a TTM basis as compared to IHS Markit car production data. • Change in number of Cerence connected cars shipped: The year-over-year change in the number of cars shipped with Cerence connected solutions. Amounts calculated on a TTM basis. • Change in Adjusted total billings YoY (TTM): The year over year change in total billings excluding Professional Services and fixed license billings and adjusted for fixed license consumption. Amounts calculated on a TTM over prior year TTM basis. ____________ See the tables at the end of this press release for non-GAAP reconciliations to the most directly comparable GAAP measures. To learn more about Cerence AI, visit www.cerence.ai, and follow the company on LinkedIn. About Cerence Inc. Cerence Inc. (NASDAQ: CRNC) is a global industry leader in creating intuitive, seamless, AI-powered experiences across automotive and transportation. Leveraging decades of innovation and expertise in voice, generative AI, and large language models, Cerence powers integrated experiences that create safer, more connected, and more enjoyable journeys for drivers and passengers alike. With more than 525 million cars Cerence Media Relations | press@cerence.com Cerence Investor Relations | cerence@pondel.com

shipped with Cerence technology, the company partners with leading automakers, transportation OEMs, and technology companies to advance the next generation of user experiences. Cerence is headquartered in Burlington, Massachusetts, with operations globally and a worldwide team dedicated to pushing the boundaries of AI innovation. For more information, visit www.cerence.ai. Cerence Media Relations | press@cerence.com Cerence Investor Relations | cerence@pondel.com

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2025-11-20_item7_mdna.md)

_Extraction: started at the Overview heading._

Overview

Cerence builds conversational and agentic AI solutions for the mobility/transportation market. Our primary target is the automobile market, but our solutions can apply to all forms of transportation including, but not limited to, two-wheel vehicles, planes, tractors, cruise ships and elevators as well as the Internet of Things industry as a whole, including televisions, smart watches, voice-powered kiosks, and more. Our solutions power natural conversational and intuitive interactions between automobiles, drivers and passengers, and the broader digital world. We possess one of the leading software platforms for building automotive virtual assistants. Our automotive customers include nearly all major automobile original equipment manufacturers ("OEMs") or their tier 1 suppliers worldwide. We deliver our solutions on a white-label basis, enabling our customers to deliver customized virtual assistants with unique, branded personalities and ultimately strengthening the bond between automobile brands and end users. Our vision is to enable a more enjoyable, safer journey for everyone.

Our principal offering is our software platform, which our customers use to build virtual assistants that can communicate, find information and take action across an expanding variety of categories. Our software platform has a hybrid architecture combining edge software components with cloud-connected components. Edge software components are installed on a vehicle's head unit and can operate without access to external networks and information. Cloud-connected components are comprised of certain speech and natural language understanding related technologies, AI-enabled personalization and context-based response frameworks, and content integration platform.

We generate revenue primarily by selling software or intellectual property ("IP") licenses and cloud-connected services. Our edge software components are typically sold under a traditional per unit perpetual software license model, in which a per unit fee is charged on a variable basis for each software instance installed on an automotive head unit. We typically license cloud-connected software components in the form of a service to the vehicle end user, which is paid for in advance. In addition, we generate professional services revenue from our work with our customers during the design, development and deployment phases of the vehicle model lifecycle and through maintenance and enhancement projects. We have existing relationships with nearly all major automotive OEMs or their tier 1 suppliers, and while our customer contracts vary, they generally represent multi-year engagements, giving us some visibility into future revenue; however, such revenue may not materialize as expected due to delays in automobile production, volatility in the political, legal and regulatory environment in which we operate including trade, tariffs and other policies implemented by the administration in the United States or actions taken by other countries in response, automotive production curtailment or delays related thereto, changing customer forecasts, macroeconomic conditions or other factors discussed elsewhere in this Annual Report.

Business Trends

We experienced a 24.0% decrease in total revenue during fiscal year 2025. The decrease in revenues was driven by a decrease in connected services revenue due to the early termination of a legacy contract acquired by Nuance through a 2013 acquisition and the termination of services provided to a separate customer, who in turn provided services to our legacy customer. The effect of this change was to accelerate $67.8 million of deferred revenue into the first quarter of fiscal year 2024. The decrease was partially offset by an increase in license revenue primarily due to an increase in volume of licensing royalties. Our license revenue is highly dependent on vehicle production, the timing and volume of which continues to be impacted by the changing dynamics in the global automotive industry. Macroeconomic conditions

such as high interest rates and lack of credit availability have contributed to production delays and slowdowns. The decrease in our professional services revenues was primarily driven by the increased standardization of our software product offerings, which requires less professional services effort to implement, other efficiencies in our professional services processes and, in some cases, customers opting to perform these activities internally.

During fiscal year 2025, total cost of revenues decreased by 21.3% compared to fiscal year 2024, primarily driven by the declines in connected services and professional services revenues. Total operating expenses decreased by 77.5% during fiscal year 2025, primarily driven by the impairment of goodwill recognized in fiscal year 2024 and our ongoing business transformation and cost reduction efforts. Restructuring and other costs, net decreased $1.7 million, driven by the wind-down of restructuring efforts initiated in 2024.

Basis of Presentation

The accompanying consolidated financial statements have been prepared in accordance with GAAP, and the rules and regulations of the SEC. The consolidated financial statements reflect all adjustments considered necessary for a fair presentation of the consolidated results of operations and financial position for the fiscal years presented. All such adjustments are of a normal recurring nature.

The consolidated financial statements include the accounts of the Company, as well as those of its wholly owned subsidiaries. All significant intercompany transactions and balances are eliminated in consolidation.

Key Financial Metrics

In evaluating our financial condition and operating performance, we focus on revenue, operating margins, and cash flow from operations.

For the fiscal year 2025 as compared to fiscal year 2024:

• Total revenue decreased by $79.7 million, or 24.0%, from $331.5 million to $251.8 million.

• Operating margin increased by 174.0 percentage points from negative 174.9% to negative 0.9%.

• Cash from operating activities changed by $44.0 million, or 255.7%, from cash provided by operating activities of $17.2 million to cash provided by operating activities of $61.2 million.

For fiscal year 2024 as compared to fiscal year 2023:

• Total revenue increased by $37.0 million, or 12.6%, from $294.5 million to $331.5 million.

• Operating margin decreased by 165.7 percentage points from negative 9.2% to negative 174.9%.

• Cash from operating activities changed by $9.7 million, or 129.4%, from cash provided by operating activities of $7.5 million to cash provided by operating activities of $17.2 million.

Operating Results

The following table shows the Consolidated Statements of Operations for the fiscal years 2025, 2024 and 2023 (dollars in thousands):

2025 | 2024 | 2023
Revenues:
License | 140,625 | 124,746 | 145,159
Connected services | 53,358 | 133,444 | 75,071
Professional services | 57,798 | 73,314 | 74,245
Total revenues | 251,781 | 331,504 | 294,475
Cost of revenues:
License | 6,941 | 6,060 | 8,522
Connected services | 21,418 | 24,787 | 22,995
Professional services | 40,286 | 56,282 | 63,232
Amortization of intangibles | — | 103 | 414
Total cost of revenues | 68,645 | 87,232 | 95,163
Gross profit | 183,136 | 244,272 | 199,312
Operating expenses:
Research and development | 97,756 | 121,563 | 123,333
Sales and marketing | 21,815 | 21,725 | 27,504
General and administrative | 48,770 | 52,468 | 57,903
Amortization of intangible assets | 1,668 | 2,203 | 5,854
Restructuring and other costs, net | 15,418 | 17,077 | 11,917
Goodwill impairment | — | 609,172 | —
Total operating expenses | 185,427 | 824,208 | 226,511
Loss from operations | (2,291) | (579,936) | (27,199)
Interest income | 3,853 | 5,353 | 4,471
Interest expense | (10,223) | (12,553) | (14,769)
Other (expense) income, net | (160) | 2,526 | 1,108
Loss before income taxes | (8,821) | (584,610) | (36,389)
Provision for income taxes | 9,893 | 3,468 | 19,865
Net loss | (18,714) | (588,078) | (56,254)

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2025-11-20_item1_business.md)

Item 1. Business.

Overview

Cerence builds conversational and agentic AI solutions that make interaction with technology feel effortless. With decades of expertise in voice, AI, and edge-to-cloud engineering, we're trusted by many of the world's leading automakers, transportation OEMs, consumer brands, and technology companies to build voice powered-interfaces that shape the user experiences of today and tomorrow. While the majority of our business is in the automotive market, our solutions can be leveraged across other areas of transportation - two-wheeled vehicles, trucks, and more - as well as outside of automotive - televisions, smart watches, voice-powered kiosks, and more.

Our automotive customers include nearly all major automobile original equipment manufacturers (OEMs) worldwide, including BMW, Mercedes-Benz, the Volkswagen Group (Volkswagen, Audi, Porsche, and other brands), Stellantis, Renault, Toyota, Ford, General Motors, BYD, Great Wall Motor, and NIO. We also partner with leading tier-one suppliers including HARMAN, EcarX, Bosch, Continental, Denso Ten, Aptiv, and others. We deliver our solutions on a white-label basis, enabling our customers to deliver highly customized virtual assistants with unique, branded personalities that strengthen the bond between their brands and end users.

Fast-moving technological advancements and increasing user engagement and comfort with large language models are driving automakers to examine how they can quickly and cost-effectively bring expanded AI features into their cars. To meet the increasing demand for automotive cognitive assistance and to offer differentiated in-car experiences, OEMs and suppliers are building proprietary virtual assistants into their vehicles. We believe that this trend will continue and that consumer adoption of in-car AI will continue to grow.

Cerence is a market leader for building integrated, branded and differentiated virtual assistants for automobiles, offering an extensive solutions portfolio that includes conversational & generative AI as well as audio & communications AI. Our conversational and generative AI solutions include a full-stack generative AI-based voice assistant, including voice activation, natural voice input and output, and hybrid conversational services for automotive and general-purpose tasks. Our audio and communications AI solutions include best-in-class audio applications, enhancing in-car experiences by reducing environmental noise and enabling seamless interaction with vehicles, inside and out. Our solutions are comprised of both edge computing and cloud-connected software components and a software framework linking these components together under a common programming interface. We deploy these solutions in deep partnership with OEMs and suppliers to optimize our software for the requirements, configurations and acoustic characteristics of specific vehicle models.

We generate revenue primarily by selling software licenses and cloud-connected services. In addition, we generate professional services revenue from our work with OEMs and suppliers during the design, development, and deployment phases of the vehicle model lifecycle and through maintenance and enhancement projects. Over our more than 25 years in the automotive industry, we have developed longstanding industry relationships. We have existing relationships with nearly all major OEMs or their tier 1 suppliers, and while our customer contracts vary, they generally represent multi-year engagements, giving us visibility into future revenue. We have master agreements or similar commercial arrangements in place with many of our customers, supporting customer retention over the long term.

As of September 30, 2025, we had estimated five-year remaining performance obligations of approximately $165.2 million. As of September 30, 2025, we had variable five-year backlog of approximately $1,004.0 million, which includes estimated future revenue from variable forecasted royalties related to our embedded, connected, and professional services businesses. Our estimate of forecasted royalties is based on our royalty rates for embedded and connected technologies from expected car shipments under our existing contracts over the term of the programs. Expected shipments are based on historical shipping experience, customer projections, and other information that management believes, taken collectively, provide a reasonable basis for estimating future shipments as of the date of this Form 10-K. Both our embedded and connected technologies are largely priced and sold on a per-vehicle or device basis, where we receive a single fee for either or both the embedded license and the connected service term. However, our five-year remaining performance obligations and variable five-year backlog may not be indicative of our actual future revenue. The revenue we actually recognize is uncertain and subject to numerous factors, including the number and timing of vehicles our customers ship, potential terminations or changes in scope of customer contracts, and currency fluctuations, as well as the other risks discussed below in Item IA, "Risk Factors." As of September 30, 2025, we estimate our five-year backlog to be approximately $1,169.2 million, including $165.2 million of five-year remaining performance obligations and $1,004.0 million of five-year variable backlog. As of September 30, 2024, the estimated five-year backlog was approximately

$952.7 million, including $172.7 million of five-year remaining performance obligations and $780.0 million of five-year variable backlog.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2025-11-20_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2025-11-20_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2025-11-20_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2025-11-20_item7_mdna.md, 10-K_2025-11-20_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
