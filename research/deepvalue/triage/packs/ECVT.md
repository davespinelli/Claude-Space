# Triage pack — ECVT · Ecovyst Inc.

_Generated 2026-09-04 14:02 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** ECVT · **Name:** Ecovyst Inc.
- **CIK:** 0001708035
- **SIC:** 2800 — Chemicals & Allied Products
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/ECVT

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Ecovyst Inc.
- **CIK:** 1,708,035 · **SIC:** 2800 (Chemicals & Allied Products) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 10.21 |
| mktcap | $1.1B |
| ev | $1.5B |
| ev_ebit | 23.5x |
| fcf | $69.9M |
| fcf_yield | 6.3% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 5.2% |
| net_debt | $405.2M |
| net_debt_ebit | 6.2x |
| cash | $87.8M |
| ltd | $493.0M |
| equity | $586.9M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $723.5M |
| revenue_prior | $598.3M |
| rev_growth | 20.9% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $64.9M |
| net_income | -$71.1M |
| cfo | $140.3M |
| capex | $70.4M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -4.3% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 109,468,398 |
| shares_py | 114,417,966 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 29.4% |
| r6m | -10.0% |
| off_52w_high | -31.8% |
| adv20 | $13.2M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.55 |
| r_ev_ebit | 0.38 |
| r_roic | 0.52 |
| r_rev_growth | 0.84 |
| r_buyback | 0.87 |
| score | 0.68 |

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
| rank | 73 |

**Screen rationale:** revenue +20.9%; buying back stock -4.3%; 12-1 momentum 29.4%


## 3. Share count trend

- Shares outstanding: **109,468,398** (CY2026Q2I) vs **114,417,966** prior year (CY2025Q2I)
- Change: **-4.3%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-24** — Item 5.02 (officer / director change or comp arrangement): On August 21, 2026, the Board of Directors of Ecovyst Inc. (the "Company") appointed Laurie Bergman as Vice President, Chief Financial Officer and Treasurer of the Company, effective as of August 24, 2026 (the "Transition Date"), succeeding Michael Feehan...
- **2026-06-30** — Item 1.01 (Entry into Material Definitive Agreement): On June 30, 2026 (the "Closing Date"), Ecovyst Catalyst Technologies LLC (the "Parent Borrower"), a wholly owned subsidiary of Ecovyst Inc., Eco Services Operations Corp. ("Eco Services", and together with Parent Borrower, collectively, the "Borrowers") and...
- **2026-05-04** — Item 1.01 (Entry into a Material Definitive Agreement): On May 1, 2026, Ecovyst Inc. (the "Company"), through its wholly owned subsidiaries New Structure Subco Inc. (the "US Purchaser") and EV Industrial Chemical Subsidiary Holdings Inc. (the "Canadian Purchaser" and, together with the US Purchaser, the...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 8,450 sh / $112,638 -> net $-112,638 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 17 (open-market buys 0, sales 1).

| code | rows |
|---|---|
| A | 10 |
| F | 1 |
| M | 5 |
| S | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-05_2-02-results.md)

_Extraction: started at the first release heading, 'Ecovyst Reports Second Quarter 2026 Results and Raises 2026 Outlook'; skipped 8 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (ex991-ecvt2q26earningsrele.htm)

Ecovyst Reports Second Quarter 2026 Results and Raises 2026 Outlook

WAYNE, PA, August 5, 2026 -- Ecovyst Inc. (NYSE: ECVT) ("Ecovyst" or the "Company"), a leading provider of regenerated sulfuric acid, virgin sulfuric acid, and sulfur dioxide and related derivatives, today reported results for the second quarter ended June 30, 2026.

On December 31, 2025, the Company completed the sale of its Advanced Materials & Catalysts business, which includes the Company's investment in affiliated companies, Zeolyst International and Zeolyst C.V. Financial results of the divested Advanced Materials & Catalysts business are reported in discontinued operations in the financial statements for all periods presented.

Second Quarter 2026 Results & Highlights from Continuing Operations

• Sales grew 42% to $250.0 million, an increase of $73.9 million, from $176.1 million in the second quarter of 2025

• Net income of $10.7 million, compared to $5.0 million in the year-ago quarter, with a net income margin of 4.3% and diluted net income per share of $0.10

• Adjusted Net Income was $23.4 million, compared to $11.4 million in the year-ago quarter, with Adjusted Diluted Income per share of $0.21

• Adjusted EBITDA grew 27% to $53.1 million, an increase of $11.2 million from $41.9 million in the second quarter of 2025

• Cash flow from operating activities was $55.2 million for the six months ended June 30, 2026, compared to $25.3 million for the six months ended June 30, 2025. Adjusted Free Cash Flow was $12.8 million for the six months ended June 30, 2026, compared to $(2.4) million for the six months ended June 30, 2025

• Completed the strategic acquisition of the Calabrian sulfur dioxide and related derivatives business from INEOS Enterprises on June 30, 2026

"In the second quarter of 2026 Ecovyst continued to deliver on its financial and long-term strategic objectives. As anticipated, high refinery utilization and positive alkylate economics contributed to increased volume of regenerated sulfuric acid, while virgin sulfuric acid volume increased double digits, reflecting positive demand fundamentals and the contribution from the Waggaman sulfuric acid plant we acquired in May 2025. As a result, we delivered second quarter 2026 Adjusted EBITDA of $53 million, within our guidance range, and up 27% compared to the year ago quarter," said Kurt J. Bitting, Ecovyst's Chief Executive Officer.

"We remain focused on creating long-term stockholder value by delivering differentiated growth by capitalizing on favorable trends in our end-use segments and pursuing synergistic acquisitions that expand our ability to serve those attractive industries," said Bitting. "In Q2 2026, we completed our acquisition of the Calabrian sulfur dioxide and related derivatives business. This transaction broadens Ecovyst's platform of leading sulfur-based solutions, expands our presence in core applications such as mining and water treatment, and provides us with attractive growth opportunities in adjacent industry applications such as food processing and pharmaceuticals. As we begin the integration of Calabrian into Ecovyst, we expect to realize meaningful synergies that we believe will create additional value for our stockholders," said Bitting. "Based upon our favorable results for the first six months of the year, and to reflect the anticipated financial contribution of Calabrian in the second half of the year, we are raising our guidance for full-year Adjusted EBITDA to a range of $195 million to $207 million," added Bitting.

Ecovyst Second Quarter 2026 Earnings Release | Page 1

Review of Business Results

Second quarter 2026 sales were $250.0 million, up $73.9 million or 42%, compared to $176.1 million in the second quarter of 2025. The increase in sales reflects higher sales volume and pricing compared to the prior year quarter. Average selling prices were higher primarily due to the pass-through effect of higher sulfur costs of approximately $55 million and favorable contractual pricing for regenerated sulfuric acid. The increase in sales volume was driven by higher sales of regenerated sulfuric acid from strong demand and less customer downtime, along with higher sales of virgin sulfuric acid due to increased customer demand and the contribution of sales volume from the Waggaman location, compared to the prior year quarter. Second quarter 2026 Adjusted EBITDA was $53.1 million, up $11.2 million or 27%, compared to $41.9 million in the second quarter of 2025, with the increase primarily driven by higher sales volume and favorable net pricing, partially offset by higher manufacturing costs, general inflation and higher transportation costs.

Cash Flows and Balance Sheet

Cash flows from operating activities for continuing operations were $55.2 million for the six months ended June 30, 2026 , co mpared to $25.3 million for the six months ended June 30, 2025. The increase was primarily driven by higher earnings exclusive of non-cash expenses.

As of June 30, 2026, the Company had cash and cash equivalents of $87.8 million. Total gross debt was $497.1 million and availability under the Asset-Based Lending ("ABL") facility was $88.5 million, after giving effect to $2.2 million of outstanding letters of credit and with no revolving credit facility borrowings outstanding. Total cash and cash equivalents of $87.8 million plus the $88.5 million of availability under the ABL facility provided for total available liquidity of $176.3 million.

As of June 30, 2026, the net debt to net income ratio was 15.9x and the net debt leverage ratio was 2.0x. The increase in the net debt leverage ratio from 1.2x at December 31, 2025 is due to the $100 million increase in the term loan associated with the acquisition of the Calabrian business with no associated Adjusted EBITDA in the trailing twelve-month period related to the Calabrian business.

Revised 2026 Financial Outlook

For the second half of 2026 our outlook for demand for regenerated and virgin sulfuric acid remains positive. We expect strong demand for regenerated acid to support alkylate production and lower customer downtime, compared to the second half of 2025. However, and consistent with our previous guidance, we expect lower sales of virgin sulfuric acid in the third and fourth quarters, compared to 2025, primarily reflecting lower expected spot sales opportunities. We remain cautious about the potential for softer demand in some industrial applications for virgin sulfuric acid.

In light of the acquisition of the Calabrian sulfur dioxide and related derivatives business on June 30, 2026, we are revising our consolidated full-year 2026 guidance to reflect our expectations for Calabrian's contributions in the third and fourth quarters of 2026.

The Company's revised 2026 guidance is as follows:

▪ Sales 1 of $1,020 million to $1,060 million (change from $890 million to $970 million)

▪ Adjusted EBITDA 2 of approximately $195 million to $207 million (change from $180 million to $195 million), including an impact from Calabrian in the second half of 2026 of $10 million to $12 million

▪ Adjusted Free Cash Flow 2 of $45 million to $55 million (change from $40 million to $55 million)

▪ Capital expenditures of $85 million to $95 million (change from $80 million to $90 million)

▪ Interest expense of $18 million to $22 million

▪ Depreciation & Amortization of $80 million to $84 million (change from $78 million to $82 million)

▪ Effective tax rate in the mid 20% range

▪ Adjusted Net Income 2 of $65 million to $85 million (change from $55 million to $75 million), with Adjusted Diluted Income per share 2 of $0.58 to $0.72 (change from $0.50 to $0.65)

Ecovyst Second Quarter 2026 Earnings Release | Page 2

1 Sales outlook for 2026 assumes higher average sulfur prices compared to 2025 and higher projected pass-through of sulfur costs of approximately $220 million (change from approximately $155 million).

2 In reliance upon the unreasonable efforts exemption provided under Item 10(e)(1)(i)(B) of Regulation S-K, the Company is not able to provide a reconciliation of its non-GAAP financial guidance to the corresponding GAAP measures without unreasonable effort because of the inherent difficulty in forecasting and quantifying certain amounts necessary for such a reconciliation such as certain non-cash, nonrecurring or other items that are included in net income and net cash provided by operating activities as well as the related tax impacts of these items and asset dispositions / acquisitions and changes in foreign currency exchange rates that are included in cash flow, due to the uncertainty and variability of the nature and amount of these future charges and costs. Because this information is uncertain, the Company is unable to address the probable significance of the unavailable information, which could be material to future results.

Stock Repurchase

In April 2022, the Company's Board of Directors approved a stock repurchase program authorizing the repurchase of up to $450 million of the Company's outstanding common stock. In October 2025, the Company's Board of Directors approved the removal of the expiration date of the stock repurchase program. As of June 30, 2026, $146.5 million was available for stock repurchases under the program.

During the second quarter of 2026, the Company did not repurchase any shares of its common stock pursuant to the stock repurchase program. For the six months ended June 30, 2026, the Company repurchased 3,226,461 shares of its common stock on the open market at an average price of $11.07 per share, for a total cost of $35.7 million.

During the second quarter of 2025, the Company repurchased 2,926,152 shares of its common stock on the open market at an average price of $7.47 per share, for a total cost of $21.9 million.

For possible future repurchases, the actual timing, number, and nature of shares repurchased will depend on a variety of factors, including stock price, trading volume, and general business and market conditions and may be conducted through negotiated transactions, open market repurchases or other means, including through Rule 10b-18 and Rule 10b5-1 trading plans or accelerated stock repurchases. The repurchase program does not obligate the Company to acquire any number of shares in any specific period, or at all, and the repurchase program may be amended, suspended or discontinued at any time at the Company's discretion.

Conference Call and Webcast Details

On Wednesday, August 5, 2026, Ecovyst management will review the second quarter 2026 results during a conference call and audio-only webcast scheduled for 11:00 a.m. Eastern Time.

Conference Call: Investors may listen to the conference call live via telephone by dialing 1 (800) 245-3047 (domestic) or

1 (203) 518-9765 (international) and use the participant code ECVTQ226.

Webcast: An audio-only live webcast of the conference call and presentation materials can be accessed at https://investor.ecovyst.com. A replay of the conference call/webcast will be made available at https://investor.ecovyst.com/events-presentations.

Investor Contact:

Gene Shiels

(484) 617-1225

gene.shiels@ecovyst.com

About Ecovyst Inc.

Ecovyst Inc. and subsidiaries is a leading provider of regenerated sulfuric acid, virgin sulfuric acid and sulfur dioxide and related derivatives, which we believe are essential to our customers' operations and processes.

Ecovyst Second Quarter 2026 Earnings Release | Page 3

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-27_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

Overview

We are a leading integrated provider of virgin and regenerated sulfuric acid products and services. We believe that our business contributes to improving the sustainability of the environment.

We are a leading provider of sulfuric acid recycling to the North American refining industry for the production of alkylate, an essential gasoline component for lowering vapor pressure and increasing octane to meet stringent gasoline specifications and fuel efficiency standards. We are a leading North American producer of high quality and high strength virgin sulfuric acid for mining and industrial applications. We also provide chemical waste handling and treatment services, as well as ex-situ catalyst activation services for the refining and petrochemical industry.

In 2025, we served customers across many end uses and, as of December 31, 2025, operated out of nine strategically located manufacturing facilities.

On September 10, 2025, we entered into a definitive agreement to sell our Advanced Materials & Catalysts business, which includes the Zeolyst Joint Venture, to Technip Energies N.V. for a purchase price of $556.0 million, subject to certain adjustments including for indebtedness, cash, working capital and transaction expenses. The transaction was concluded effective December 31, 2025. The results of operations, financial condition, and cash flows for the Advanced Materials & Catalysts business are presented herein as discontinued operations. Except where noted, any tables, percentages or metrics included within this filing exclude the results of our Advanced Materials & Catalysts business. Refer to Note 4 to our consolidated financial statements for additional information

Stock Repurchase Program

On April 27, 2022, the Board of Directors approved a stock repurchase program that authorized the Company to purchase up to $450.0 million of the Company's common stock over the four-year period from the date of approval (the "Stock Repurchase Program"). In October 2025, the Board of Directors amended the Stock Repurchase Program to remove the limitation that all repurchases must be made within the four-year period from the date of original approval. For the year ended December 31, 2025, the Company repurchased 5,752,285 shares on the open market at an average price of $8.24 per share, for a total of $47.4 million excluding brokerage commissions and accrued excise tax. As of December 31, 2025, $182.2 million was available for share repurchases under the program.

During the year ended December 31, 2024, the Company repurchased 552,081 shares on the open market at an average price of $9.05 per share, for a total of $5.0 million, excluding brokerage commissions and accrued excise tax.

For possible future repurchases, the actual timing, number, and nature of shares repurchased will depend on a variety of factors, including stock price, trading volume, and general business and market conditions and may be conducted through negotiated transactions, open market repurchases or other means, including through Rule 10b-18 and 10b5-1 trading plans or accelerated share repurchases.

Key Performance Indicators

Adjusted EBITDA, Adjusted Net Income and Net Debt

Adjusted EBITDA, Adjusted Net Income and Net Debt are financial measures that are not prepared in accordance with GAAP and that we use to evaluate our operating performance, for business planning purposes and to measure our performance relative to that of our competitors. Adjusted EBITDA, Adjusted Net Income and Net Debt are presented as key performance indicators as we believe these financial measures will enhance a prospective investor's understanding of our results of operations and financial condition. EBITDA consists of net income from continuing operations b efore interest, taxes, depreciation and amortization. Adjusted EBITDA consists of EBITDA adjusted for (i) non-operating income or expense, and (ii) the impact of certain non-cash, nonrecurring or other items included in net income from continuing operations and EBITDA that we do not consider indicative of our ongoing operating performance. Adjusted Net Income consists of net income from continuing operations adjusted for (i) non-operating income or expense and (ii) the impact of certain non-cash, nonrecurring or other items included in net income from continuing operations that we do not consider indicative of our ongoing operating performance. Net Debt consists of total debt less cash and cash equivalents. We believe that these non-GAAP financial measures provide investors with useful financial metrics to assess our operating performance from period-to-period by excluding certain items that we believe are not representative of our core business.

You should not consider Adjusted EBITDA, Adjusted Net Income, or Net Debt in isolation or as alternatives to the presentation of our financial results in accordance with GAAP. The presentation of Adjusted EBITDA, Adjusted Net Income and Net Debt financial measures may differ from similar measures reported by other companies and may not be comparable to other similarly titled measures. In evaluating Adjusted EBITDA and Adjusted Net Income, you should be aware that we are likely to incur expenses similar to those eliminated in this presentation in the future and that certain of these items could be considered recurring in nature. Our presentation of Adjusted EBITDA and Adjusted Net Income should not be construed as an inference that our future results will be unaffected by unusual or nonrecurring items. Reconciliations of Adjusted EBITDA, Adjusted Net Income to GAAP net income and Net Debt to GAAP total debt are included in this "Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations" for each of the respective periods.

Key Factors and Trends Affecting Operating Results and Financial Condition

Sales

Overall, our business continued to benefit from positive demand trends for our products and services in the majority of end uses we serve. Strong demand for refined products continued to support high refinery utilization rates, while more stringent gasoline standards and growing demand for premium gasoline to power higher-compression and turbo-charged engines continued to drive demand for alkylate and for our regeneration services product group. In addition, demand for virgin sulfuric acid across a wide range of industrial applications, including mining, remained favorable.

Cost of Goods Sold

Cost of goods sold consists of variable product costs, fixed manufacturing expenses, depreciation expense and freight expenses. Variable product costs include all raw materials and energy costs that are directly related to the manufacturing process. Fixed manufacturing expenses include all plant employment costs, manufacturing overhead and periodic maintenance costs.

The primary raw materials include spent sulfuric acid, sulfur, acids, bases (including sodium hydroxide, or "caustic soda") and certain metals. Spent sulfuric acid for our regeneration services product group is supplied by customers as part of their contracts.

Most of our contracts feature take-or-pay volume protection and/or quarterly price adjustments for commodity inputs, labor, the Chemical Engineering Index (U.S. chemical plant construction cost index) and natural gas. About 90% of our sales for the year ended December 31, 2025 were under contracts featuring quarterly price adjustments. The price adjustments generally reflect actual costs for producing sulfuric acid and tend to protect us from volatility in labor, fixed costs and raw material pricing. The take-or-pay volume protection allows us to cover fixed costs through intermittent, temporary production issues at customer refineries.

While natural gas is not a direct feedstock for any product, natural gas powered machinery and equipment are used to heat raw materials and create the chemical reactions necessary to produce end-products. We maintain multiple suppliers wherever possible and structure our customer contracts when possible to allow for the pass-through of raw material, labor and natural gas costs.

Seasonality

Our regeneration services product group typically experiences seasonal fluctuations as a result of higher demand for gasoline products in the summer months and lower demand in the winter months as well as fluctuations associated with customer turnarounds. These demand fluctuations generally result in higher sales and working capital requirements in the second and third quarters.

Results of Operations

Year Ended December 31, 2025 Compared to the Year Ended December 31, 2024

Highlights

The following is a summary of our financial performance for the year ended December 31, 2025 compared with the year ended December 31, 2024, which excludes the results of the Advanced Materials & Catalysts business for all periods.

Sales

Sales increased $125.2 million to $723.5 million. The increase in sales primarily reflects higher average selling prices from the pass-through effect of higher sulfur costs, favorable contractual pricing for regenerated sulfuric acid and higher sales of virgin sulfuric acid, including the contribution from the acquired Waggaman, Louisiana location, partially offset by lower regenerated sulfuric acid volume.

Gross Profit

Gross profit decreased $5.3 million to $158.1 million. The decrease in gross profit was primarily due to lower regenerated sulfuric acid volume and higher manufacturing costs, partially offset by higher average selling prices.

Operating Income

Operating income decreased $20.2 million to $64.9 million. The decrease in operating income was primarily due to the decrease in gross profit and higher other operating expenses, net.

The following is our consolidated statements of loss and a summary of financial results for the years ended December 31, 2025 and 2024.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-27_item1_business.md)

ITEM 1. BUSINESS.

Ecovyst Inc. ("Ecovyst" or the "Company"), formerly PQ Group Holdings Inc., was incorporated in Delaware on August 7, 2015. We trace our roots to the late 1800s with our first sulfuric acid plant and the beginning of our oldest customer relationship.

Our common stock is listed on the New York Stock Exchange under the stock ticker "ECVT". Unless the context otherwise indicates, the terms "Ecovyst Inc.," "we," "us," "our," or the "Company" mean Ecovyst Inc. and our subsidiaries.

Effective on December 31, 2025, we completed the sale of our Advanced Materials & Catalysts segment, which includes our investment in affiliated companies, Zeolyst International and Zeolyst C.V. (collectively, the "Zeolyst Joint Venture") to Technip Energies N.V. for a purchase price of $556.0 million, subject to certain adjustments set forth in the agreement. We used $465.0 million of the net cash proceeds to partially repay the Senior Secured Term Loan Facility due June 2031. The results of operations, financial condition and cash flows for the Advanced Materials & Catalysts business are presented herein as discontinued operations. Refer to Note 4 to our consolidated financial statements for additional information.

Our Company

We are a leading integrated provider of virgin and regenerated sulfuric acid products and services. We believe that our business contributes to improving the sustainability of the environment.

We are a leader in our business, holding what we estimate to be a number one or number two supply share position for products and services that generated more than 95% of our 2025 sales. We believe that our footprint and efficient network of strategically located manufacturing and regeneration facilities provide us with a strong competitive advantage in serving our customers.

Our products and services typically represent a small portion of our customers' overall end-product costs, yet are critical to their processes. With our long history of customer partnerships and our reputation for providing reliable, quality products and services, we believe we deliver significant value to our customers, as demonstrated by our profit margins.

We are diversified by business application and end use. In 2025, the majority of our sales were for applications that have historically had relatively predictable, consistent demand patterns associated with consumption and industrial processes.

As a result of our competitive strengths, we have generally maintained stable earnings and margins over time and through changing macro economic cycles.

In 2025, we served customers across many end uses and, as of December 31, 2025, operated out of nine strategically located manufacturing facilities.

Our Strategy

We intend to capitalize on our strong business fundamentals and long-term customer partnerships to grow sales, maintain high margins, deploy capital efficiently and generate consistent free cash flow in order to create stockholder value. We believe that our long history of operational excellence and proven reliability, longstanding customer relationships, a network of strategically located manufacturing facilities and consistent business execution developed from our industry experience positions us well to execute our business strategy.

Our Industry

The products and services that we provide to our customers are often high value-add, even when they represent a small portion of our customers' overall end product costs, and we believe we can continue to be successful by providing customers with quality products and reliable service. We believe many of the end uses that we serve are generally more resilient to economic cycles, minimizing extreme fluctuations in demand. We believe our customers value our geographic proximity to their operations and our plant network provides redundancy in capacity to serve their needs.

We believe the combination of attractive operating margins and generally predictable maintenance capital expenditure requirements improves our ability to generate attractive cash flows.

Our Product End Uses

The table below summarizes our key end use applications and products, as well as the significant growth drivers in those applications.

Key End Uses | Significant Growth Drivers | Key Products
Regeneration and Treatment Services | • Increase gasoline octane in order to improve fuel efficiency while lowering vapor pressure and sulfur to regulated levels | • Regenerated sulfuric acid
• High industry utilization | • Hazardous waste treatment services
• Growing demand for applications in hazardous and non-hazardous waste
Industrial, Mining & Automotive | • Demand for metals and minerals for low carbon technologies and infrastructure | • Virgin sulfuric acid for mining
• Demand for a wide range of products including construction materials, auto, consumer goods, petrochemicals and chemicals | • Virgin sulfuric acid derivatives for industrial production
• Recovery in global oil drilling/U.S. copper production | • Virgin sulfuric acid derivatives for nylon production
Other | • Growing demand for ex-situ catalyst activation to support traditional and sustainable fuels production | • Catalyst activation
• Improve lubricant characteristics to improve fuel efficiencies | • Aluminum sulfate solution
• Municipal and industrial water treatment | • Ammonium bisulfite solution

The table below summarizes sales for the years ended December 31, 2025, 2024 and 2023, respectively:

December 31, 2025 | December 31, 2024 | December 31, 2023
Key End Uses | Sales | % of Sales | Sales | % of Sales | Sales | % of Sales
(in millions, except percentages)
Regeneration and Treatment Services | 361.2 | 49.9 | % | 357.4 | 59.7 | % | 354.6 | 60.6 | %
Industrial, Mining & Automotive | 327.9 | 45.3 | % | 206.9 | 34.6 | % | 200.4 | 34.3 | %
Other | 34.4 | 4.8 | % | 34.0 | 5.7 | % | 29.8 | 5.1 | %
Total | 723.5 | 598.3 | 584.8

Competitive Business Strengths

Favorable Secular Growth Trends Across the Portfolio

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

**Present:** meta.json, form4_summary.md, 8-K_2026-08-05_2-02-results.md, 10-K_2026-02-27_item7_mdna.md, 10-K_2026-02-27_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
