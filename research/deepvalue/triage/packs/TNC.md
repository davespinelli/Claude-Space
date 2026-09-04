# Triage pack — TNC · TENNANT CO

_Generated 2026-09-04 18:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** TNC · **Name:** TENNANT CO
- **CIK:** 0000097134
- **SIC:** 3580 — Refrigeration & Service Industry Machinery
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/TNC

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** TENNANT CO
- **CIK:** 97,134 · **SIC:** 3580 (Refrigeration & Service Industry Machinery) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtAndCapitalLeaseObligations

**Valuation**

| metric | value |
|---|---|
| price | 70.34 |
| mktcap | $1.2B |
| ev | $1.5B |
| ev_ebit | 21.7x |
| fcf | $43.3M |
| fcf_yield | 3.6% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 6.6% |
| net_debt | $281.5M |
| net_debt_ebit | 4.1x |
| cash | $76.9M |
| ltd | $358.4M |
| equity | $533.4M |
| ltd_tag | LongTermDebtAndCapitalLeaseObligations |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $1.2B |
| revenue_prior | $1.3B |
| rev_growth | -6.5% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $68.3M |
| net_income | $43.8M |
| cfo | $65.0M |
| capex | $21.7M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -7.7% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 17,049,303 |
| shares_py | 18,469,129 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 10.4% |
| r6m | 14.3% |
| off_52w_high | -22.5% |
| adv20 | $18.2M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.41 |
| r_ev_ebit | 0.41 |
| r_roic | 0.58 |
| r_rev_growth | 0.15 |
| r_buyback | 0.92 |
| score | 0.54 |

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
| rank | 203 |

**Screen rationale:** buying back stock -7.7%; 12-1 momentum 10.4%


## 3. Share count trend

- Shares outstanding: **17,049,303** (CY2026Q2I) vs **18,469,129** prior year (CY2025Q2I)
- Change: **-7.7%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-30** — Item 5.02 (Departure of Directors or Certain Officers; Election of): Directors; Appointment of Certain Officers; Compensatory Arrangements of Certain Officers.
- **2026-06-17** — Item 5.02 (officer / director change or comp arrangement): the appointment of Richard H. (Rusty) Zay to the position of Chief Operating Officer ("COO"), effective July 1, 2026.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 9,500 sh / $640,990 vs sells 6,875 sh / $605,103 -> net $35,887 (BUYING).
Distinct insiders buying (code P): 2. Largest buy: Mulligan Donal L bought 8,000 sh @ $67.34 ($538,720) on 2026-08-12.

Form 4 filings parsed: 12; transaction rows: 12 (open-market buys 2, sales 1).

| code | rows |
|---|---|
| A | 9 |
| P | 2 |
| S | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'Page 1 – Tennant Company Reports Second Quarter 2026 Results'; skipped 11 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99.1 - NEWS RELEASE DATED AUGUST 5, 2026 (tnc-20260805xexx991.htm)

Page 1 – Tennant Company Reports Second Quarter 2026 Results

Tennant Company Reports Second Quarter 2026 Results

Order Growth and Robotics Momentum Continued as Margin Recovery Progressed More Slowly Than Expected

Net Sales of $324 Million, a 1.7% Increase over Prior-Year Period

Adjusted EBITDA of $35 Million as Residual ERP and EMEA Cost Pressures Weighed on Margin

Full-Year Net Sales Guidance Raised to $1.270 - $1.310 Billion; Adjusted EBITDA Guidance Lowered to $155 - $170 Million

MINNEAPOLIS, MN (Aug. 5, 2026) —Tennant Company ("Tennant" or the "Company") (NYSE: TNC) today reported its financial results for the quarter ended June 30, 2026.

(In millions, except per share data) | Three Months Ended June 30, | Six Months Ended June 30,
2026 | 2025 | Incr / (Decr) | 2026 | 2025 | Incr / (Decr)
Net sales | 324.0 | 318.6 | 1.7 | % | 621.9 | 608.6 | 2.2 | %
Net income | 7.6 | 20.2 | (62.4) | % | 7.8 | 33.3 | (76.6) | %
Diluted EPS | 0.44 | 1.08 | (59.3) | % | 0.45 | 1.77 | (74.6) | %
Adjusted diluted EPS (a) | 0.83 | 1.49 | (44.3) | % | 1.41 | 2.60 | (45.8) | %
Adjusted EBITDA (a) | 35.3 | 51.0 | (30.8) | % | 64.4 | 92.0 | (30.0) | %
Adjusted EBITDA (a) margin % | 10.9 | % | 16.0 | % | (510) bps | 10.4 | % | 15.1 | % | (470) bps

Highlights

• ERP stabilization held during the quarter, though the expected optimization benefits did not fully materialize, with residual inefficiencies in North America and continued pricing and volume pressure in EMEA weighing on results.

• Orders of $339.5 million increased 6.6% year over year, growing across most regions and building backlog to $127 million, reinforcing healthy underlying demand.

• Net sales of $324.0 million increased 1.7% year over year, reflecting price realization and favorable foreign currency effects, partially offset by an organic sales decline driven by softer volumes in EMEA and APAC.

• Adjusted EBITDA (a) of $35.3 million, or 10.9% of net sales, declined compared to the prior year as gross margin and cost leverage fell short of expectations, driven by residual ERP-related inefficiencies in North America and pricing and cost pressure in EMEA.

• Adjusted diluted EPS (a) of $0.83 declined compared to the prior year, primarily due to lower gross margin rates and higher operating costs, partially offset by the benefit of share repurchases.

• Robotics momentum continued to build, with AMR sales of approximately $31 million increasing 37% year over year, underscoring progress toward the Company's $250 million AMR revenue target by 2028.

(a) See supplemental non-GAAP financial tables below for a reconciliation of adjusted non-GAAP financial measures to GAAP.

(more)

Page 2 – Tennant Company Reports Second Quarter 2026 Results

"Our second quarter results reflect solid demand and order growth, though margin recovery progressed more slowly than we expected," said Dave Huml, Tennant President and Chief Executive Officer. "Orders grew across most of our regions, robotics revenue grew approximately 37%, and backlog continued to build, underscoring the strength of underlying demand for our products. At the same time, residual ERP-related inefficiencies in North America and margin pressure in EMEA weighed on profitability more than we anticipated. We are taking targeted actions to address these challenges. Reflecting the strength of our order book, backlog, and continued robotics momentum, we are raising our full-year net sales guidance while lowering our full-year Adjusted EBITDA guidance range to reflect both the profitability impacts experienced in the first half of the year and a more measured pace of margin recovery in the second half."

Net Sales

Consolidated net sales for the second quarter of 2026 totaled $324.0 million, a 1.7% increase compared to consolidated net sales of $318.6 million in the second quarter of 2025. The components of the consolidated net sales change were as follows:

Three Months Ended June 30, | Six Months Ended June 30,
2026 vs. 2025
Price | 3.0% | 3.6%
Volume | (3.5)% | (4.8)%
Organic decline | (0.5)% | (1.2)%
Acquisitions | 0.6% | 0.6%
Foreign currency | 1.6% | 2.8%
Total | 1.7% | 2.2%

Organic Sales

Organic sales, which exclude the effects of foreign currency and acquisitions, decreased 0.5% in the second quarter compared to the prior year. This decrease was the result of price realization being more than offset by lower volume, reflecting production and fulfillment constraints in North America and softer demand in certain EMEA and APAC markets.

Three Months Ended June 30, 2026 | Six Months Ended June 30, 2026
Americas | EMEA | APAC | Total | Americas | EMEA | APAC | Total
Organic sales growth / (decline) | 1.4% | (2.8)% | (10.6)% | (0.5)% | (0.7)% | (1.0)% | (6.8)% | (1.2)%

Americas (b) : The 1.4% increase in the second quarter was primarily driven by price realization and continued strength in Latin America, partially offset by lower volumes in North America due to production and fulfillment constraints.

EMEA (c) : The 2.8% decrease in the second quarter was primarily due to lower equipment volumes in certain European markets, including parts of Southern Europe and the Benelux region, as well as softer demand in export markets impacted by geopolitical developments in the Middle East.

APAC (d) : The 10.6% decrease in the second quarter was primarily driven by lower equipment volumes across most countries, reflecting softer market demand and distributor overstock in certain markets, partially offset by price realization and volume growth in India.

(b) Includes North America and Latin America.

(c) Includes Europe, the Middle East, and Africa.

(d) Includes China, Australia, Japan, and other Asian markets.

(more)

Page 3 – Tennant Company Reports Second Quarter 2026 Results

Operating Results

The gross profit margin of 39.5% in the second quarter of 2026 was 260 basis points lower compared to the second quarter of 2025. The margin rate decline was driven primarily by ERP-related recovery costs, supply constraints, and elevated freight and tariff-related material costs in North America. In EMEA, margin was pressured by competitive price concessions, volume deleverage, and unfavorable mix. These impacts were partially offset by price realization and cost management actions.

Selling and administrative ("S&A") expense totaled $99.5 million in the second quarter of 2026, a $5.8 million increase compared to the second quarter of 2025. The increase was primarily driven by unfavorable foreign currency, higher people-related costs and technology spend, partially offset by lower bad debt expense and other administrative expenses. S&A expense as a percentage of sales was 30.7% in the second quarter of 2026, compared to 29.4% in the second quarter of 2025. Adjusted S&A (a) as a percentage of net sales increased to 29.1% in the second quarter of 2026, compared to 27.3% in the second quarter of 2025.

Research and development ("R&D") expense totaled $12.5 million in the second quarter of 2026, compared to $9.8 million in the second quarter of 2025. The increase was primarily driven by continued investment in innovation, including robotics and autonomous solutions.

Adjusted EBITDA (a) was $35.3 million in the second quarter of 2026, compared to $51.0 million in the prior-year period. The decrease in Adjusted EBITDA (a) was primarily due to gross margin declines coupled with S&A deleverage. Adjusted EBITDA margin (a) for the second quarter of 2026 was 10.9%, down 510 basis points compared to 16.0% in the prior-year period.

Net income was $7.6 million in the second quarter of 2026, compared to $20.2 million in the second quarter of 2025. Adjusted net income (a) was $14.4 million in the second quarter of 2026, a decrease of $13.4 million compared to the second quarter of 2025. The decrease was primarily driven by lower operating performance from gross margin compression coupled with S&A deleverage.

Adjusted diluted EPS (a) was $0.83 in the second quarter of 2026, compared to $1.49 in the second quarter of 2025. The decrease was driven by lower adjusted net income resulting from gross margin compression and S&A deleverage, partially offset by a reduction of approximately 1.5 million diluted weighted average shares outstanding versus the prior-year period.

Cash Flow, Liquidity and Capital Allocation

Tennant generated $5.0 million of cash flow for operating activities during the second quarter of 2026, a $17.5 million decrease compared to the prior‑year period, primarily driven by lower operating performance and increased working capital requirements, including higher accounts receivable and inventory balances and lower accounts payable. Working capital levels and cash conversion were adversely affected by operational and process inefficiencies associated with the North America ERP implementation, and management remains focused on improving working capital efficiency as stabilization and fulfillment efforts progress.

Liquidity remained strong with a balance of $76.9 million in cash and cash equivalents at the end of the second quarter, and $289.4 million of unused borrowing capacity under the Company's revolving credit facility.

The Company continues to strategically deploy cash flow to meet operational capital requirements and to return capital to shareholders in alignment with its capital allocation priorities. During the second quarter of 2026, the Company invested $5.3 million in capit al expenditures and returned $5.3 million to shareholders through dividends. The Company remains diligent in managing its debt and maintaining a strong balance sheet. The Company had a net leverage ratio (Adjusted Net Debt (a) / trailing twelve months (TTM) Adjusted EBITDA (a) ) of 2.0 times as of June 30, 2026.

(a) See supplemental non-GAAP financial tables below for a reconciliation of adjusted non-GAAP financial measures to GAAP.

(more)

Page 4 – Tennant Company Reports Second Quarter 2026 Results

2026 Guidance

Our first-half results reflect solid demand and order growth, though gross margin recovery progressed more slowly than we anticipated. Residual ERP-related inefficiencies in North America, together with pricing and volume pressure in EMEA and incremental freight and material costs tied to Middle East disruptions, weighed on margin performance during the second quarter. Order momentum remained healthy, with orders up 6.6% year over year and backlog building to $127 million, and robotics revenue grew approximately 37% year over year. Based on our first-half performance and our outlook for the second half, we are raising our full-year net sales guidance, reflecting our order and backlog position and continued robotics momentum, while lowering our full-year Adjusted EBITDA guidance range to reflect the slower pace of margin recovery, as follows.

(In millions, except per share data) | 2026 Guidance Ranges
Net sales | $1,270 - $1,310
Organic net sales growth | 3.5% - 7.0%
Diluted net income per share | $2.15 - $2.80
Adjusted diluted net income per share** | $3.80 - $4.45
Adjusted EBITDA** | $155 - $170
Adjusted EBITDA margin** | 12.2% - 13.0%
Capital expenditures | ~$25
Adjusted effective tax rate** | 24% - 29%

**Non-GAAP Measures: see supplemental non-GAAP financial tables below for a reconciliation of adjusted non-GAAP financial measures to GAAP.

Conference Call

Tennant will host a conference call to discuss its 2026 second quarter results on August 6, 2026, at 9 a.m. Central Time (10 a.m. Eastern Time). The conference call and accompanying slides will be available via webcast on Tennant's investor website. To listen to the call live and view the slide presentation, go to investors.tennantco.com and click on the link at the bottom of the overview page. A replay of the conference call, with slides, will be available at investors.tennantco.com.

Company Profile

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-24_item7_mdna.md)

_Extraction: started at the Overview heading._

Overview

Tennant Company is a world leader in designing, manufacturing and marketing solutions that help create a cleaner, safer, healthier world. The Company is committed to creating and commercializing breakthrough, sustainable cleaning innovations to enhance its broad suite of products, including floor maintenance and cleaning equipment, detergent-free and other sustainable cleaning technologies, aftermarket parts and consumables, equipment maintenance and repair service, and asset management solutions. Our products are used in many types of environments, including factories and warehouses, distribution centers, office buildings, public venues such as arenas and stadiums, schools and universities, hospitals and clinics, and more. Customers include contract cleaners to whom organizations outsource facilities maintenance as well as businesses that perform facilities maintenance themselves. The Company reaches these customers through the industry's largest direct sales and service organization and through a strong and well-supported network of authorized distributors worldwide.

Macroeconomic Events

As a global company, we continue to be exposed to risks and uncertainties stemming from macroeconomic and geopolitical conditions. These factors include inflationary pressures, interest rate volatility, foreign currency exchange rate volatility, changes in capital markets conditions, and shifts in international trade policy. Collectively, these conditions create a dynamic operating environment that may affect the Company's ability to drive growth, restore margins, and advance its transformation initiatives

While overall inflationary pressures have generally moderated, the Company continues to experience a more concentrated and direct impact on the cost components of its products, which remain significant to its cost structure. Changes in trade policy, particularly tariffs, pose a significant risk to our operations. Tariff increases, changes to trade agreements, or potential retaliatory actions could raise supplier costs, weaken demand, and disrupt the Company's operations. The Company has implemented, and expects to continue implementing, pricing actions, cost management initiatives, and supply chain measures to mitigate these pressures; however, such efforts may not fully offset the impact.

Global geopolitical instability continues to contribute to economic and operational uncertainty. Ongoing conflicts in Ukraine and the Middle East, rising tensions involving China and Taiwan, and the possibility of escalation in regions where the United States may be involved have increased the risk of wider economic disruption. These developments could result in supply chain volatility, logistics constraints, higher input costs, and changes in customer purchasing behavior. The timing, duration, and severity of these potential effects are uncertain and difficult to predict.

Demand trends across our major markets were mixed throughout the year. In China, after a period marked by uneven economic recovery and pricing pressure, organic growth returned late in the year. In EMEA and the broader APAC region, organic growth also improved in the latter part of the year, reversing earlier declines and

reflecting resilience in select markets and effective responses to customer needs despite ongoing macroeconomic and competitive pressures.

Enterprise Resource Planning (ERP) System Implementation

In the first week of November 2025, the Company went live with the ERP system in its largest region, North America. The transition introduced unexpected challenges that constrained operating capacity post go-live, including order‑management and fulfillment disruptions, manufacturing scheduling issues, and reduced inventory visibility, particularly within Parts & Consumables and Service. The system transition also resulted in the loss of three weeks of machine order entry and parts shipping capability, as well as contributing to slower transaction processing and prolonged customer delays.

In response, the Company deployed cross‑functional recovery teams, implemented manual and system‑based workarounds, increased on‑site support, and adjusted production scheduling. Although December showed improvement as our mitigation efforts took hold, we were unable to fully offset the impact of the November disruptions.

While primary system issues have been addressed, certain customer‑related impacts and incremental support needs continued into early 2026, and we expect some temporary inefficiencies to persist as teams acclimate to the new platform and as optimization efforts continue.

See the "Risk Factors" section in Part I, Item 1A of this Annual Report for further discussion of the possible impact of the above conflicts and macroeconomic events on our business and financial results.

Outlook

The Company expects the macroeconomic and demand environment in 2026 to generally reflect the conditions experienced during 2025. Tariff‑related cost increases and inflationary input costs are expected to remain key elements of the cost structure. The Company has implemented targeted pricing and cost‑out initiatives intended to moderate these impacts, though the timing and magnitude of benefits may vary.

Following the North America ERP implementation in late 2025, certain operational inefficiencies and elevated support needs are expected to persist into the second quarter of 2026. As part of broader system‑stabilization efforts, the Company conducted a comprehensive physical inventory that required a two‑week shutdown of manufacturing operations in early January, which is expected to weigh on first‑quarter sales and costs. The Company also anticipates continued operating inefficiencies during the early stages of system stabilization, resulting in higher costs and margin pressure, most notably in the first quarter. As stabilization progresses and processes mature, the Company expects to transition toward a more normalized operating rhythm by mid‑year.

While these factors may influence near‑term results, operating margins are expected to improve through 2026 as ERP stabilization advances and as the cumulative benefits of pricing actions, cost‑management measures, and supply‑chain initiatives are realized. Margin performance is expected to strengthen gradually over the course of the year, with first‑quarter margins anticipated to be generally consistent with levels experienced in the fourth quarter of 2025 and improving thereafter as operational efficiency increases. The Company also expects ongoing margin pressure from tariffs implemented in the second half of 2025. To help offset these impacts, it has taken targeted actions across its supply chain and commercial pricing processes.

Additionally, the Company continues to invest in strategic priorities that support long‑term growth and competitiveness, including the ongoing expansion of its robotics portfolio and autonomous solutions.

Historical Results

The following table compares the historical results of operations for the years ended December 31, 2025 and 2024 in dollars and as a percentage of net sales (in millions, except per share amounts and percentages):

2025 | % | 2024 | %
Net sales | 1,203.5 | 100.0 | 1,286.7 | 100.0
Cost of sales | 719.2 | 59.8 | 736.7 | 57.3
Gross profit | 484.3 | 40.2 | 550.0 | 42.7
Selling and administrative expense | 374.8 | 31.1 | 391.9 | 30.5
Research and development expense | 41.2 | 3.4 | 43.8 | 3.4
Operating income | 68.3 | 5.7 | 114.3 | 8.9
Interest expense, net | (9.0) | (0.7) | (9.1) | (0.7)
Net foreign currency transaction gain | (1.7) | (0.1) | 0.1 | —
Other expense, net | 0.3 | — | (0.5) | —
Income before income taxes | 57.9 | 4.8 | 104.8 | 8.1
Income tax expense | 14.1 | 1.2 | 21.1 | 1.6
Net income | 43.8 | 3.6 | 83.7 | 6.5
Net income per share - diluted | 2.36 | 4.38

Net Sales

Consolidated net sales in 2025 totaled $1,203.5 million, a 6.5% decrease as compared to consolidated net sales of $1,286.7 million in 2024. The components of the consolidated net sales change were as follows:

Twelve Months Ended December 31,
2025 vs. 2024
Price | 1.4%
Volume | (8.7)%
Organic decline | (7.3)%
Acquisitions | 0.1%
Foreign currency | 0.7%
Total decline | (6.5)%

The 6.5% decrease in consolidated net sales was driven by:

• Organic sales decline of 7.3% primarily due to volume declines in North America, which lapped a significant backlog-reduction benefit in the prior-year period and was affected by transitional impacts related to the new ERP implementation . These factors were partly offset by price realization in the Americas and EMEA;

• A net favorable impact from foreign currency exchange of approximately 0.7% primarily due to the strengthening of the Euro relative to the U.S. dollar; and

• Acquisition-related growth of 0.1% driven by TCS.

The following table sets forth annual net sales by geographic area and the related percentage change from the prior year (in millions, except percentages):

2025 | % | 2024 | %
Americas | 792.0 | (10.9) | 888.5 | 5.7
Europe, Middle East and Africa (EMEA) | 334.6 | 5.1 | 318.5 | 1.3
Asia Pacific (APAC) | 76.9 | (3.5) | 79.7 | (10.3)
Total | 1,203.5 | (6.5) | 1,286.7 | 3.5

Americas

Net sales in the Americas were $792.0 million in 2025, a decrease of 10.9% from 2024 driven by:

• Organic sales decline of 10.5%, primarily due to volume declines in North America, as a result of lapping a significant backlog-reduction benefit in the prior-year period, order fulfillment disruptions associated with our fourth quarter 2025 ERP transition, and softer underlying demand primarily in industrial equipment in the second half of 2025. This was partially offset by price realization; and

• A net unfavorable impact from foreign currency exchange of approximately 0.4%.

Europe, Middle East and Africa ("EMEA")

EMEA net sales were $334.6 million in 2025, an increase of 5.1% from 2024 driven by:

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-24_item1_business.md)

ITEM 1 – Business

General Development of Business

Founded in 1870 by George H. Tennant, Tennant Company ("the Company, we, us, or our"), headquartered in Eden Prairie, Minnesota, is a world leader in designing, manufacturing and marketing of solutions that help create a cleaner, safer and healthier world. Tennant was incorporated as a Minnesota corporation in 1909 and began as a one-man woodworking business, eventually evolving into a successful wood flooring and wood products company, an d finally into a manufacturer of floor cleaning equipment. Throughout its history, the Company has remained focused on advancing its industry by aggressively pursuing new technologies and creating a culture that celebrates innovation.

Today, the Company has 11 global manufacturing locations and operates in three geographic areas including the Americas, Europe, Middle East and Africa ("EMEA") and Asia Pacific ("APAC"). We aggregate our operating segments into one reportable segment that consists of the design, manufacture, sale and servicing of products used primarily in the maintenance of nonresidential surfaces.

Our commitment to innovation and excellence extends across every aspect of our business—from product development and customer service to manufacturing and marketing. We prioritize delivering high-performance solution s that minimize waste, lower costs, enhance safety, and advance sustainability objectives. By dedicating resources to research, development and engineering, we continuously refine existing products and introduce new ones that align with evolving market demands.

Over the past century, we have expanded our brand portfolio, diversified our product offerings, and advanced our technologies through innovation and strategic acquisitions. This disciplined approach to growth ensures that each acquisition complements our existing capabilities and adds value by enhancing our product range or improving technological expertise.

Principal Products, Markets and Distribution

The Company offers products and solutions consisting of manual and autonomous mechanized cleaning equipment for both industrial and commercial use, detergent-free and other sustainable cleaning technologies, aftermarket parts and consumables, equipment maintenance and repair services, and business solutions such as financing, rental and leasing programs, and machine-to-machine asset management solutions. The Company is committed to developing cleaning technologies which increase cleaning productivity. We have strong brand presence in the global markets we serve, offering both premium and mid-tier products for each region to meet customer needs.

The Company's products are used in many types of environments including: retail establishments, distribution centers, factories and warehouses, public venues such as arenas and stadiums, office buildings, schools and universities, hospitals and clinics, and more. The Company markets its offerings under the following brands: Tennant ® , Nobles ® , Alfa Uma Empresa Tennant™, IPC, Gaomei and Rongen brands as well as private-label brands. The Company has a portfolio of differentiated technology solutions that includes an expanding portfolio of robotic cleaning equipment, IRIS ® as an asset management solution, ec-H2O NanoClean ® as a detergent-free cleaning solution, and ReadySpace ® as a rapid-drying carpet cleaning technology. The Company's more than 40,000 customers include contract cleaners to whom organizations outsource facilities maintenance, as well as businesses that perform facilities maintenance themselves. The Company reaches these customers through the industry's largest direct sales and service organization and through a strong and well-supported network of authorized distributors worldwide.

The Company has an extensive global field service network. We sell products directly in 21 countries and through distributors in more than 100 countries.

Raw Materials and Component Parts

Steel, metal alloys and resin are the primary raw materials used to manufacture our mechanized cleaning equipment. We purchase various component parts, electronics and services used in production and product development processes from third parties.

Operations and input costs are influenced by global macroeconomic conditions, including trade policies, tariffs on certain imported materials, interest rate levels, and regional supply-demand dynamics. While supply chain conditions have generally stabilized compared to prior periods, input costs remain subject to variability driven by tariff regimes, competitive market conditions, and regulatory requirements in certain jurisdictions.

The Company seeks to mitigate these risks through regional manufacturing and sourcing strategies, diversified supplier relationships, longer-term supply arrangements, and ongoing engineering and platform design initiatives intended to increase sourcing flexibility and supply chain resilience.

Intellectual Property

The Company owns a broad range of intellectual property rights in both the United States and a number of foreign countries. Our patents, proprietary technologies and trade secrets, customer relationships, licenses, trademarks, trade names and brand names in the aggregate constitute a valuable asset, but we do not regard our business as being materially dependent upon any single item or category of intellectual property. We take appropriate measures to protect our intellectual property to the extent such intellectual property can be protected.

Research and Development

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-24_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-24_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-24_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-02-24_item7_mdna.md, 10-K_2026-02-24_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
