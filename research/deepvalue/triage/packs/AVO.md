# Triage pack — AVO · Mission Produce, Inc.

_Generated 2026-09-04 21:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** AVO · **Name:** Mission Produce, Inc.
- **CIK:** 0001802974
- **SIC:** 0700 — Agricultural Services
- **Fiscal year end (MM-DD):** 10-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/AVO

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Mission Produce, Inc.
- **CIK:** 1,802,974 · **SIC:** 700 (Agricultural Services) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 12.57 |
| mktcap | $1.1B |
| ev | $1.2B |
| ev_ebit | 18.3x |
| fcf | $37.2M |
| fcf_yield | 3.4% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 7.8% |
| net_debt | $82.8M |
| net_debt_ebit | 1.3x |
| cash | $33.0M |
| ltd | $115.8M |
| equity | $578.6M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $1.4B |
| revenue_prior | $1.2B |
| rev_growth | 12.7% |
| rev_growth_note | share count +25.1% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | n/a |
| ebit | $65.2M |
| net_income | $37.7M |
| cfo | $88.6M |
| capex | $51.4M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 25.1% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 88,319,807 |
| shares_py | 70,618,213 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -3.0% |
| r6m | -9.0% |
| off_52w_high | -18.1% |
| adv20 | $7.2M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.40 |
| r_ev_ebit | 0.49 |
| r_roic | 0.63 |
| r_rev_growth | 0.72 |
| r_buyback | 0.06 |
| score | 0.46 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q1I |
| shares_period | CY2026Q2I |
| shares_py_period | CY2025Q2I |
| capex_missing | False |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 284 |

**Screen rationale:** share count +25.1% yoy — growth may be acquisition/issuance-driven, not organic


## 3. Share count trend

- Shares outstanding: **88,319,807** (CY2026Q2I) vs **70,618,213** prior year (CY2025Q2I)
- Change: **25.1%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`
- **Flag:** share count +25.1% yoy — growth may be acquisition/issuance-driven, not organic

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-05-29** — Item 5.02 (officer / director change or comp arrangement): The information set forth in Item 2.01 of this Current Report on Form 8-K is incorporated into this Item 5.02 by reference.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 3,554,301 sh / $44,751,747 vs sells 206,176 sh / $2,769,238 -> net $41,982,509 (BUYING).
Distinct insiders buying (code P): 3. Largest buy: Globalharvest Holdings Venture Ltd bought 687,222 sh @ $13.42 ($9,222,519) on 2026-07-08.

Form 4 filings parsed: 12; transaction rows: 20 (open-market buys 16, sales 4).

| code | rows |
|---|---|
| P | 16 |
| S | 4 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-06-08_2-02-results.md)

_Extraction: started at the first release heading, 'OXNARD, Calif.—June 8, 2026—(GLOBE NEWSWIRE) Mission Produce, Inc. (NA'; skipped 8 forward-looking-statement block(s); 7 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (exh991avoq22026earningsrel.htm)

OXNARD, Calif.—June 8, 2026—(GLOBE NEWSWIRE) Mission Produce, Inc. (NASDAQ: AVO) ("Mission" or "the Company") a world leader in sourcing, producing, and distributing fresh Hass avocados, today reported its financial results for the fiscal second quarter ended April 30, 2026.

Fiscal Second Quarter 2026 Financial Overview:

• Total revenue of $290.9 million and achieved volume growth of 15% compared to the same period last year

• Net loss attributable to Mission Produce of $7.2 million, or $(0.10) per diluted share, compared to income of $3.1 million, or $0.04 per diluted share for the same period last year

• Adjusted net income was $0.8 million or $0.01 per diluted share, which excludes the impact of transaction advisory costs of $6.4 million on a pretax basis or $0.07 on a per share after-tax basis, as compared to $8.7 million, or $0.12 per diluted share, for the same period last year

• Adjusted EBITDA was $7.1 million, reflecting lower per-unit margins primarily driven by historically low prices and a temporary mismatch in supply and demand for core fruit sizes

CEO Message

John Pawlowski, President and CEO of Mission, stated, "This quarter was shaped by high volumes, low prices, strong execution by our sales and operations teams, and unfortunately, margin compression concentrated in April. Despite the low-price environment, we maintained manageable margins through most of the quarter until the Mexican supply of core fruit sizes fell out of line with customer demand in the final weeks. Delays in the California and Peru harvests increased sourcing costs to fill the gaps and pressured margins. Importantly, supply conditions have improved, pricing and margins are recovering, and we expect to deliver solid performance in the back half of the year.

"Importantly, second quarter's temporary low-price market helped lay the foundation for more durable category growth longer term. U.S. avocado consumption and household penetration reached record highs, with per-capita consumption up double-digits from last year and more than 1.6 million new households entering the category. As we've seen in the past, dynamics like these create a larger and more durable demand base, and as a category leader, Mission is positioned to capitalize on these trends going forward.

"Finally, we have recently entered a new chapter for Mission. In just the last two months we completed our CEO succession, consummated the acquisition of Calavo, drove meaningful share gains in our core business, and sharpened our capital allocation priorities that we expect will drive disciplined growth, margin expansion, and returns. We see meaningful opportunity to improve asset utilization, strengthen mix, and convert our category leadership into higher earnings power over time. We are aligned on our agenda and focused on executing it with discipline. We look forward to sharing more about our next chapter at our Investor Day coming up very shortly in the Fall."

Fiscal Second Quarter 2026 Consolidated Financial Review

Total revenue for the second quarter of fiscal 2026 decreased 24% to $290.9 million compared to the same period last year. The decrease was primarily driven by a 36% decrease in per-unit avocado sales prices, partially offset by a 15% increase in avocado volume sold. Volume and price movements in the Marketing and Distribution segment were driven by a robust Mexican avocado supply due to higher yields in the current year.

EXHIBIT 99.1

Gross profit was $20.5 million in the second quarter of fiscal 2026, compared to $28.4 million in the prior year, while gross margin decreased 50 basis points compared to the same period last year, to 7.0% of revenue. Gross profit in the Marketing & Distribution segment was lower primarily due to historically low prices and a mismatch in supply and demand for core fruit sizes in April, which further pressured per-unit margins. Gross profit was also lower in our International Farming segment due to reduced volume of blueberry packing and storage services resulting from lower harvest volumes combined with higher per-unit mango production costs.

Selling, general and administrative expense ("SG&A") (which does not include transaction advisory costs) for the second quarter were flat compared to the same period last year. Transaction advisory costs were $6.4 million for the second quarter this year and were comprised of third-party legal, diligence, and other costs associated with the Calavo acquisition, which was completed on May 28, 2026.

Net loss attributable to Mission Produce for the second quarter of fiscal 2026 was $(7.2) million, or $(0.10) per diluted share. This compares to income of $3.1 million, or $0.04 per diluted share, for the same period last year.

Adjusted net income for the second quarter of fiscal 2026 was $0.8 million, or $0.01 per diluted share, which excludes the impact of transaction advisory costs. This compares to $8.7 million, or $0.12 per diluted share for the same period last year.

Adjusted EBITDA was $7.1 million for the second quarter of fiscal 2026, as compared to $19.1 million in the prior year period. The decline was driven primarily by lower gross profit resulting from the margin dynamics described above.

Fiscal Second Quarter Business Segment Performance

Marketing & Distribution

Total segment sales in the Marketing & Distribution segment were $277.2 million, compared to $362.5 million for the same period last year, driven by the avocado volume and price dynamics described above.

Segment operating loss, which included the impact of transaction advisory costs, was $3.8 million in the three months ended April 30, 2026, compared to income of $7.6 million for the same period last year. Segment adjusted EBITDA was $7.2 million, compared to $16.8 million in the same period last year. These results were driven by lower per-unit gross margin, as described above.

International Farming

The vast majority of fruit sales from the International Farming segment are made to the Marketing & Distribution segment, with the remainder of revenue largely derived from direct sales of fruit to third parties, as well as services provided to third-parties and the Blueberries segment. Affiliated sales are concentrated in the second half of the fiscal year in alignment with the Peruvian avocado harvest season, which typically runs from April through September of each year. As a result, operating income and segment adjusted EBITDA for the International Farming segment is generally concentrated in the third and fourth quarters of the fiscal year. In addition, the Company operates approximately 700 acres of mangos in Peru. The timing of the mango harvest is generally concentrated in the fiscal second quarter.

Total segment sales in the International Farming segment were $7.7 million, compared to $8.1 million for the same period last year.

Segment operating loss was $3.9 million in the three months ended April 30, 2026, compared to $1.3 million in the same period last year. Segment adjusted EBITDA loss was $1.3 million, compared to positive $1.5 million in the same period last year. These results were driven by higher per-unit mango production costs and lower volume of blueberry packaging and storage services.

Blueberries

Sales in the Blueberries segment have traditionally been concentrated in the first and fourth quarters of the fiscal year in alignment with the Peruvian blueberry harvest season.

Total segment sales in the Blueberries segment were $11.0 million for the second quarter, compared to $15.7 million for the same period last year, primarily due to a decrease in volume sold, partially offset by increases in average per-unit sales price.

Segment operating income was $0.7 million for the second quarter compared to $0.6 million in the same period last year. Segment adjusted EBITDA was $1.2 million, compared to $0.8 million in same period last year. These results were driven by an increase in average per-unit sales price, partially offset by lower per-acre yields resulting in higher per-unit fruit production costs.

Balance Sheet and Cash Flow

Cash and cash equivalents were $33.0 million as of April 30, 2026, compared to $64.8 million as of October 31, 2025.

The Company's operating cash flows are seasonal in nature and can be temporarily influenced by working capital shifts resulting from varying payment terms to growers in different source regions. In addition, the Company is building inventory in its International

EXHIBIT 99.1

Farming segment during the first half of the year for ultimate harvest and sale that will occur during the second half of the fiscal year. While these increases in working capital can cause operating cash flows to be unfavorable in individual quarters, it is not indicative of operating cash performance expected to be realized for the full year.

Net cash used by operating activities was $21.0 million for the six months ended April 30, 2026, as compared to a use of $13.0 million in the same period last year. Lower income in the current year was partially offset by lower increases in working capital. Working capital growth in the current year is driven by higher trade receivables associated with seasonality and timing of sales in the Marketing & Distribution and Blueberries segments, while inventory growth is driven by higher volume in the Marketing & Distribution segment and cultivation of growing crop inventory in our International Farming and Blueberries segments.

Capital expenditures were $22.9 million for the six months ended April 30, 2026 compared to $28.0 million for the same period last year. Capital expenditures were comprised primarily of avocado orchard development, pre-production orchard maintenance and land improvements, packhouse construction in Guatemala and pre-production land development and blueberry plant cultivation in Peru. The current year also includes construction costs associated with increasing capacity in the Company's Mexican packing operations.

Stock Repurchase Authorization

On June 3, 2026, the Board of Directors approved a stock repurchase program, which permits the Company to repurchase up to $100 million of shares of the Company's common stock over the next 36 months, effective June 3, 2026 (the "2026 Program"). The 2026 Program replaces the Company's previous common stock repurchase program adopted in September 2023, which would have expired in September 2026 with approximately $11.2 million remaining. No shares were repurchased following approval through June 8, 2026.

Under the new share repurchase program, repurchases can be made from time to time using a variety of methods, which may include open market purchases, privately negotiated transactions or otherwise, all in accordance with the rules of the Securities and Exchange Commission and other applicable legal requirements. The specific timing, price and size of purchases will depend on prevailing stock prices, general economic and market conditions, and other considerations. The share repurchase program does not obligate the Company to acquire any particular amount of Company common stock, and the repurchase program may be suspended or discontinued at any time at the Company's discretion.

The new share repurchase program reflects the Company's commitment to disciplined capital allocation and shareholder value creation. It provides flexibility to repurchase shares opportunistically when the market valuation of the Company does not reflect its intrinsic value. The program also reflects management's confidence in Mission's long-term growth prospects.

Acquisition of Calavo Growers, Inc.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2025-12-18_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

Overview

We are a world leader in sourcing, producing and distributing Hass avocados, serving retail, wholesale and foodservice customers. We source, produce, pack and distribute avocados and a small amount of other fruits to our customers and provide value-added services including ripening, bagging, custom packaging and logistical management. In addition, we provide our customers with merchandising and promotional support, insights on market trends and training designed to increase their retail avocado sales.

Reportable segments

We have three operating segments which are also reportable segments:

• Marketing & Distribution . Our Marketing & Distribution reportable segment sources fruit from growers and then distributes the fruit through our global distribution network.

• International Farming . International Farming owns and operates orchards from which the vast majority of fruit produced is sold to our Marketing & Distribution segment. The segment's farming activities range from cultivating early-stage plantings to harvesting from mature trees. It also earns service revenues for packing and processing fruit for both our Blueberries segment, as well as for third-party producers of other crops. Operations are principally located in Peru and Guatemala.

• Blueberries. The Blueberries segment consists of farming activities that include cultivating early-stage blueberry plantings and harvesting mature bushes. Substantially all blueberries produced are sold to a single distributor under an exclusive marketing agreement.

Macroeconomic environment

During fiscal 2025, the United States enacted a series of global trade policies including reciprocal and retaliatory tariffs, and subsequent revisions and exemptions thereof, on imported goods. As a result, tariffs have applied at different dates and rates throughout the year, depending on country of origin. We are continuing to monitor changes to global trade policies, including the impact of proposed and enacted tariffs as future changes could have direct or indirect impacts to our business. For additional information, see the risk factor " Changes to U.S. trade policy, tariff and import/export regulations may adversely affect our operating results " in Section 1A. of this report.

Supply chain optimization

The Company closed its Canadian distribution centers within its Marketing & Distribution segment during the first quarter of 2025. In connection with the closure, we recognized approximately $2.7 million in charges for fiscal 2025. Charges consisted of accelerated depreciation expense of property, plant and equipment, accelerated amortization expense of operating lease right-of-use assets, loss on disposal of property, plant and equipment, and severance costs which were partially offset by gains on settlement of asset retirement obligations. Volume from these facilities has been absorbed by our other distribution centers and third-party service providers.

Results of Operations

The operating results of our businesses are significantly impacted by the price and volume of fruit we farm, source and distribute. In addition, our results have been, and will continue to be, affected by quarterly and annual fluctuations due to a number of factors, including but not limited to: tariffs; pests and disease; weather patterns; changes in demand by consumers; food safety advisories; the timing of the receipt, reduction or cancellation of significant customer orders; the gain or loss of significant customers; the availability, quality and price of raw materials; the utilization of capacity at our various locations; and general economic conditions.

Our financial reporting currency is the U.S. dollar. The functional currency of our most significant subsidiaries is the U.S. dollar and the majority of our sales are denominated in U.S. dollars. A significant portion of our purchases of avocados are denominated in the Mexican Peso and a significant portion of our growing and harvesting costs are denominated in Peruvian Soles. Fluctuations in the exchange rates between the U.S. dollar and these local currencies usually do not have a significant impact on our gross margin because the impact typically affects our pricing by comparable amounts. Our margin exposure to exchange rate fluctuations is short-term in nature, as our sales price commitments are generally limited to less than one month and orders can primarily be serviced with procured inventory. Over longer periods of time, we believe that the impact exchange rate fluctuations will have on our cost of goods sold will largely be passed on to our customers in the form of higher or lower prices.

Years ended October 31,
2025 | 2024 | 2023
(In millions, except percentages) | Dollar | % | Dollar | % | Dollar | %
Net sales | 1,391.2 | 100.0 | % | 1,234.7 | 100.0 | % | 953.9 | 100.0 | %
Cost of sales | 1,230.5 | 88.4 | % | 1,082.2 | 87.6 | % | 870.6 | 91.3 | %
Gross profit | 160.7 | 11.6 | % | 152.5 | 12.4 | % | 83.3 | 8.7 | %
Selling, general and administrative expenses | 95.5 | 6.9 | % | 86.8 | 7.0 | % | 76.4 | 8.0 | %
Operating income | 65.2 | 4.7 | % | 65.7 | 5.3 | % | 6.9 | 0.7 | %
Interest expense | (9.4) | (0.7) | % | (12.6) | (1.0) | % | (11.6) | (1.2) | %
Equity method income | 5.4 | 0.4 | % | 3.7 | 0.3 | % | 4.0 | 0.4 | %
Other income (expense), net | 0.7 | 0.1 | % | 3.6 | 0.3 | % | (0.2) | — | %
Income (loss) before income taxes | 61.9 | 4.4 | % | 60.4 | 4.9 | % | (0.9) | (0.1) | %
Provision for income taxes | 21.4 | 1.5 | % | 18.6 | 1.5 | % | 2.2 | 0.2 | %
Net income (loss) | 40.5 | 2.9 | % | 41.8 | 3.4 | % | (3.1) | (0.3) | %
Less: Net income (loss) attributable to noncontrolling interest | 2.8 | 0.2 | % | 5.1 | 0.4 | % | (0.3) | — | %
Net income (loss) attributable to Mission Produce | 37.7 | 2.7 | % | 36.7 | 3.0 | % | (2.8) | (0.3) | %

Net sales

Our net sales are generated predominantly from the shipment of fresh avocados to retail, wholesale and foodservice customers worldwide. Our net sales are affected by numerous factors, including the balance between the supply of and demand for our produce and competition from other fresh produce companies. Our net sales are also dependent on our ability to supply a consistent volume and quality of fresh produce to the markets we serve.

Years ended October 31,
(In millions) | 2025 | 2024 | 2023
Net sales:
Marketing & Distribution | 1,274.3 | 1,152.6 | 889.9
International Farming | 23.8 | 6.4 | 11.6
Blueberries | 93.1 | 75.7 | 52.4
Total net sales | 1,391.2 | 1,234.7 | 953.9

Net sales increased $156.5 million or 13% in fiscal year 2025 compared to the previous year, primarily driven by a 7% increase in avocado volume sold our Marketing & Distribution segment. Increased sales in our International Farming segment were driven by higher volumes of avocados sold directly to customers in the current year. Volume and price movements resulted from higher Peruvian avocado production driven by more favorable weather conditions in the current year.

Net sales increased $280.8 million or 29% in fiscal year 2024 compared to the previous year, primarily driven by our Marketing & Distribution segment, where average per-unit avocado sales prices increased 30% and avocado volume sold was relatively flat. Blueberry revenue increased $23.3 million or 44%, due primarily to a 37% increase in average per-unit sales price, which was favorably impacted by industry supply constraints during the Peru harvest season.

Gross profit

Cost of sales is composed primarily of avocado procurement costs from independent growers and packers, logistics costs, packaging costs, labor, costs associated with cultivation (the cost of growing crops), harvesting and depreciation. Avocado procurement costs from third-party suppliers can vary significantly between and within fiscal years and correlate closely with market prices for avocados. While we have long-standing relationships with our growers and packers, we predominantly purchase fruit on a daily basis at market rates. As such, the cost to procure products from independent growers can have a significant impact on our costs.

Logistics costs include land and sea transportation and expenses related to port facilities and distribution centers. Land transportation costs consist primarily of third-party trucking services to support North American distribution, while sea transportation cost consists primarily of third-party shipping of refrigerated containers from supply markets in South and Central America to demand markets in North America, Europe and Asia. Fuel prices as well as variations in containerboard prices, which affect the cost of boxes and other packaging materials, impact our product cost and our profit margins. Variations in production yields and other input costs also affect our cost of sales.

In general, changes in our volume of products sold can have a disproportionate effect on our gross profit. Within any particular year, a significant portion of our cost of products are fixed. Accordingly, higher volumes produced on company-owned farms directly reduce the average cost per pound of fruit grown on company owned orchards, while lower volumes directly increase the average cost per pound of fruit grown on company owned orchards. Likewise, higher volumes processed through packing and distribution facilities directly reduce the average overhead cost per unit of fruit handled, while lower volumes directly increase the average overhead cost per unit of fruit handled.

Gross profit percentage will fluctuate based upon per-unit sales price levels in relation to per-unit costs. Margin is primarily managed on a per-unit basis in our Marketing & Distribution segment, which can lead to movement in gross profit percentage when sales prices fluctuate.

Years ended October 31,
2025 | 2024 | 2023
Gross profit (in millions) | 160.7 | 152.5 | 83.3
Gross profit as a percentage of net sales | 11.6 | % | 12.4 | % | 8.7 | %

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2025-12-18_item1_business.md)

Item 1. Business

Overview

Mission Produce, Inc. together with its consolidated subsidiaries ("Mission Produce" or the "Company," "Registrant," or "Issuer," and generally referred to as "we" or "us"), is a global leader in the avocado industry. The Company's expertise lies in the farming, packaging, marketing and distribution of avocados to food retailers, distributors and produce wholesalers worldwide. The Company procures avocados principally from California, Mexico and Peru. Through our various operating facilities, we grow, sort, pack, bag and ripen avocados and a small amount of other fruits for distribution to domestic and international markets. We report our results of operations in three operating segments which are also reportable segments:

• Marketing & Distribution sources fruit from growers and then distributes the fruit through our global distribution network;

• International Farming owns and operates orchards from which the vast majority of fruit produced is sold to our Marketing & Distribution segment. The segment's farming activities range from cultivating early-stage plantings to harvesting from mature trees. It also earns service revenues for packing and processing fruit for both our Blueberries segment, as well as for third-party producers of other crops. Operations are principally located in Peru and Guatemala.

• Blueberries consists of farming activities that include cultivating early-stage blueberry plantings and harvesting mature bushes. Substantially all blueberries produced are sold to a single distributor under an exclusive marketing agreement.

Products and services

We primarily source, produce, pack and distribute avocados. The avocados we sell are primarily of the Hass variety. We sort and pack avocados and match their specifications to respective customer requirements. We sell both pre-ripe and ripened avocados, and with our network of ripening facilities, we can adjust the level of ripeness to the needs of our customers. Our custom ripening programs provide customers with the option of ordering avocados at five different stages of ripeness – hard, preconditioned, breaking, firm-ripe and ripe – which are delivered on specifically tailored schedules according to stage of ripeness. In 2021, we also began marketing mangos on a limited scale. Mangos are complementary to avocados as they typically have opposite seasons, allowing us to leverage and maintain absorption of our distribution network.

We also provide value-added services including ripening, bagging, custom packaging, logistical management, and quality assurance. In addition, we provide our customers with merchandising and promotional support, insights on market trends and hands-on training to assist with their retail sales of our avocados. For example, we operate category management, merchandising and packaging programs, such as our "Avo Intel," "Minis—small but mighty," "Emeralds in the Rough," "Ready," "Size Minded," "Jumbos—more to eat, more to love" and shelf-life extension programs, to promote the sale of avocados that might otherwise be underutilized, to identify ready-to-eat and various size avocados for consumers and to increase shelf life.

In our Blueberries segment, we act as growers. Our exclusive supply agreement with an exclusive distributor allows us to utilize our existing infrastructure and workforce in Peru during complementary periods between avocado harvest and processing seasons.

Customers

We primarily market avocados to retail, wholesale and foodservice customers. We focus on delivering quality avocados on time and within customer specifications. We forecast avocado sourcing costs for the season for our own production, which enables us to enter into fixed price contracts with customers for a season without bearing pricing risk from spot market purchases. We do not have long-term supply contracts with our customers and focus instead on building strong, long-term relationships based on product quality and specifications, on-time delivery and customer support and service.

Supply chain and distribution network

Our global distribution network includes strategically located forward distribution centers across North America, China, Europe, and the U.K. equipped to offer value-added services such as ripening, bagging, custom packaging and logistical management. Our network of distribution facilities puts us in close proximity to our customers, allowing us to provide fruit based on customer timing, specification, and volume needs. Within the United States, we can deliver avocados within approximately eight hours or less.

Before being forwarded to distribution centers, avocados are sorted and packed at one of our four state-of-the-art packing facilities in Mexico, Peru, and California, or by co-packers in various locations. Our packing facilities are located in close proximity to

growers, allowing us to control the logistics of the supply chain from tree to packing, to distribution. Transportation logistics are managed across truck, ocean, air and rail platforms, depending on origin and end markets.

Competition

We compete based on a variety of factors, including the appearance, taste, size, shelf life and overall quality of our fruit, price and distribution terms, the timeliness of our deliveries to customers and the availability of our products. The avocado and fresh produce business is highly competitive, and the effect of competition is intensified because our products are perishable. Marketing competitors include other distributors, producers, and other smaller packers and marketers. Farming competitors include other farming businesses of all sizes, from large-scale businesses and cooperatives, to individual farms.

Resources

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2025-12-18_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2025-12-18_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2025-12-18_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-06-08_2-02-results.md, 10-K_2025-12-18_item7_mdna.md, 10-K_2025-12-18_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
