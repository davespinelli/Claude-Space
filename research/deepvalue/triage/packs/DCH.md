# Triage pack — DCH · Dauch Corp

_Generated 2026-09-05 00:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** DCH · **Name:** Dauch Corp
- **CIK:** 0001062231
- **SIC:** 3714 — Motor Vehicle Parts & Accessories
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/DCH

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Dauch Corp
- **CIK:** 1,062,231 · **SIC:** 3714 (Motor Vehicle Parts & Accessories) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 6.67 |
| mktcap | $1.6B |
| ev | $5.8B |
| ev_ebit | 51.9x |
| fcf | $155.1M |
| fcf_yield | 9.8% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 1.5% |
| net_debt | $4.2B |
| net_debt_ebit | 37.7x |
| cash | $880.8M |
| ltd | $5.1B |
| equity | $1.5B |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $5.8B |
| revenue_prior | $6.1B |
| rev_growth | -4.7% |
| rev_growth_note | share count +100.2% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | n/a |
| ebit | $112.3M |
| net_income | -$19.7M |
| cfo | $411.6M |
| capex | $256.5M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 100.2% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 237,604,602 |
| shares_py | 118,664,153 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 0.7% |
| r6m | 14.2% |
| off_52w_high | -25.9% |
| adv20 | $18.5M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.70 |
| r_ev_ebit | 0.14 |
| r_roic | 0.36 |
| r_rev_growth | 0.20 |
| r_buyback | 0.01 |
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
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 380 |

**Screen rationale:** share count +100.2% yoy — growth may be acquisition/issuance-driven, not organic; 12-1 momentum 0.7%


## 3. Share count trend

- Shares outstanding: **237,604,602** (CY2026Q2I) vs **118,664,153** prior year (CY2025Q2I)
- Change: **100.2%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`
- **Flag:** share count +100.2% yoy — growth may be acquisition/issuance-driven, not organic

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-05-04** — Item 5.02 (officer / director change or comp arrangement): On February 4, 2026, the board of directors of Dauch Corporation ("Dauch") approved the Amended and Restated Dauch Corporation 2018 Omnibus Incentive Plan (the "Plan"), subject to the approval of stockholders.
- **2026-05-01** — Item 5.02 (officer / director change or comp arrangement): On February 4, 2026, the board of directors of Dauch Corporation ("Dauch") approved the Amended and Restated Dauch Corporation 2018 Omnibus Incentive Plan (the "Plan"), subject to the approval of stockholders.
- **2026-04-17** — Item 5.02 (officer / director change or comp arrangement): On April 13, 2026, the Board of Directors of Dauch Corporation (the "Company")

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 13 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 13 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-07_2-02-results.md)

_Extraction: started at the first release heading, 'Dauch Reports Second Quarter 2026 Financial Results'; skipped 9 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (dch-q2_2026xex991xir.htm)

Dauch Reports Second Quarter 2026 Financial Results

Delivers Strong Performance and Operating Cash Flow

DETROIT, August 7, 2026 -- Dauch Corporation ("Dauch") (NYSE: DCH; LSE: DCH) today reported its financial results for the second quarter 2026.

Second Quarter 2026 Results

• Sales of $2.96 billion

• Net income attributable to Dauch of $1.0 million

• Adjusted EBITDA of $389.6 million, or 13.2% of sales

• Diluted earnings per share of $0.00; Adjusted earnings per share of $0.32

• Net cash provided by operating activities of $107.5 million; Adjusted free cash flow of $148.4 million

"The company's strong second-quarter results highlight the continued positive acceleration for the new Dauch Corporation," said Chairman and Chief Executive Officer David C. Dauch. "We are focused on unlocking the full strategic potential of the transformational acquisition we completed earlier in the year."

The acquisition of Dowlais Group plc (subsequently renamed Dowlais Group Limited) ("Dowlais") was the primary driver of year-over-year changes in financial results.

The company's sales in the second quarter of 2026 were $2.96 billion as compared to $1.54 billion in the second quarter of 2025.

The company's net income attributable to Dauch in the second quarter of 2026 was $1.0 million, a nominal amount per share and a nominal margin on sales, as compared to net income of $39.3 million, or $0.32 per share and 2.6% of sales, in the second quarter of 2025.

Adjusted earnings per share in the second quarter of 2026 was $0.32 compared to Adjusted earnings per share of $0.34 in the second quarter of 2025.

In the second quarter of 2026, Adjusted EBITDA was $389.6 million, or 13.2% of sales, as compared to $202.1 million, or 13.2% of sales, in the second quarter of 2025.

The company's net cash provided by operating activities for the second quarter of 2026 was $107.5 million as compared to $91.9 million for the second quarter of 2025.

The company's Adjusted free cash flow for the second quarter of 2026 was $148.4 million as compared to $48.7 million for the second quarter of 2025.

Dauch's Updated 2026 Financial Outlook

Dauch's full year 2026 financial targets which include a partial year contribution from Dowlais (as of February 3, 2026 close) are as follows:

• Sales in the range of $10.6 - $10.8 billion vs. $10.3 - $10.8 billion previously.

• Adjusted EBITDA in the range of $1.36 - $1.425 billion vs. $1.30 - $1.425 billion previously.

• Adjusted EBITDA includes synergy benefits of $60 - $75 million (vs $50 - $75 million previously), equating to a run rate of greater than $100 million by the end of year one.

• Equity income from our China JV (which is included in Adjusted EBITDA) in the range of $70 - $80 million vs $65 - $75 million previously.

• Adjusted free cash flow in the range of $260 - $325 million vs. $235 - $325 million previously.

• Capital expenditures in the range of 4.5% to 5% of sales.

• Restructuring cash payments of $115 - $150 million.

• Synergy implementation cash payments of $95 - $110 million.

These targets are based on the following assumptions for 2026:

• Production outlook:

North America | Europe | China | Global
~15.1 million | ~16.9 million | ~31.6 million | ~91.1 million

• Production estimates of key programs that we support and the current operating environment.

• No changes to USMCA and mitigation of a majority of incremental tariff costs.

Second Quarter 2026 Conference Call Information

A conference call to review Dauch's second quarter results is scheduled for today at 10:00 a.m. ET. Interested participants may listen to the live conference call by logging onto Dauch's investor web site at www.dauch.com or calling (877) 883-0383 from the United States or (412) 902-6506 from outside the United States with access code 953-5491. A replay will be available one hour after the call is completed until August 14, 2026 by dialing (855) 669-9658 from the United States or (412) 317-0088 from outside the United States. When prompted, callers should enter replay access code 984-1988.

Non-GAAP Financial Information

In addition to the results reported in accordance with accounting principles generally accepted in the United States of America (GAAP) included within this press release, Dauch has provided certain information, which includes non-GAAP financial measures such as Adjusted EBITDA, Adjusted earnings per share and Adjusted free cash flow. Such information is reconciled to its most directly comparable GAAP measure in accordance with Securities and Exchange Commission rules and is included in the attached supplemental data.

Certain of the forward-looking financial measures included in this earnings release are provided on a non-GAAP basis. A reconciliation of non-GAAP forward-looking financial measures to the most directly comparable forward-looking financial measures calculated and presented in accordance with GAAP has been provided. The amounts in these reconciliations are based on our current estimates and actual results may differ materially from these forward-looking estimates for many reasons, including potential event driven transactional and other non-core operating items and their related effects in any future period, the magnitude of which may be significant.

Management believes that these non-GAAP financial measures are useful to management, investors, and banking institutions in their analysis of Dauch's business and operating performance. Management also uses this information for operational planning and decision-making purposes.

Non-GAAP financial measures are not and should not be considered a substitute for any GAAP measure. Additionally, non-GAAP financial measures as presented by Dauch may not be comparable to similarly titled measures reported by other companies.

Definition of Non-GAAP Financial Measures

Dauch defines Adjusted earnings per share to be diluted earnings (loss) per share excluding the impact of restructuring and acquisition-related costs, debt refinancing and redemption costs, gains or losses on the derivative associated with our Business Combination with Dowlais, net interest on debt held in escrow, gains or losses on equity securities, impairment charges, unrealized foreign exchange gains and losses on acquired U.S. Private Placement Notes, mark-to-market on nondesignated foreign exchange derivatives assumed as part of the Business Combination with Dowlais, gains and losses on the disposal of property, plant and equipment, amortization of the acquisition intangible asset attributable to our investment in SDS, net of tax, amortization of intangible assets from acquisitions, and non-recurring items, including the tax effect thereon.

Dauch defines EBITDA to be earnings before interest expense, income taxes, depreciation and amortization. As revised, Adjusted EBITDA is defined as EBITDA excluding the impact of restructuring and acquisition-related costs, debt refinancing and redemption costs, gains or losses on the derivative associated with our Business Combination with Dowlais, interest income on debt held in escrow, gains or losses on equity securities, impairment charges, unrealized foreign exchange gains and losses on acquired U.S. Private Placement Notes, mark-to-market on nondesignated foreign exchange derivatives assumed as part of the Business Combination with Dowlais, gains and losses on the disposal of property, plant and equipment, amortization of the acquisition intangible asset attributable to our investment in SDS, net of tax, and non-recurring items.

Dauch defines free cash flow to be net cash provided by operating activities less capital expenditures net of proceeds from the sale of property, plant and equipment. Adjusted free cash flow is defined as free cash flow excluding the impact of cash payments for restructuring and acquisition-related costs, including net interest on debt held in escrow.

Company Description

Dauch Corporation is a premier Driveline and Metal Forming supplier serving the global automotive industry with a powertrain-agnostic product portfolio that supports electric, hybrid, and internal combustion vehicles. The company is headquartered in Detroit, MI, with operations that span 24 countries and more than 175 locations. Formed through the acquisition of Dowlais and its subsidiaries - GKN Automotive and GKN Powder Metallurgy, Dauch unites deep engineering roots with global manufacturing capabilities and an entrepreneurial spirit to move mobility forward. Visit www.dauch.com to learn more.

Media Contact

Christopher M. Son

Vice President, Marketing & Communications

(313) 758-4814

chris.son@aam.com

Or visit the Dauch website at www.dauch.com .

DAUCH CORPORATION

CONDENSED CONSOLIDATED STATEMENTS OF OPERATIONS

(Unaudited)

Three Months Ended | Six Months Ended
June 30, | June 30,
2026 | 2025 | 2026 | 2025
(in millions, except per share data)
Net sales | 2,955.6 | 1,536.2 | 5,334.5 | 2,947.5
Cost of goods sold | 2,617.4 | 1,335.5 | 4,770.9 | 2,572.9
Gross profit | 338.2 | 200.7 | 563.6 | 374.6
Selling, general and administrative expenses | 166.9 | 100.8 | 304.2 | 191.7
Amortization of intangible assets | 21.8 | 20.4 | 44.7 | 41.0
Impairment charge | — | 8.0 | — | 8.0
Restructuring and acquisition-related costs | 49.8 | 16.5 | 148.7 | 36.2
Operating income | 99.7 | 55.0 | 66.0 | 97.7
Interest expense | (89.8) | (43.1) | (179.4) | (86.0)
Interest income | 7.2 | 5.6 | 19.3 | 11.2
Other income (expense):
Debt refinancing and redemption costs | (0.9) | — | (3.9) | (3.3)
Gain on Business Combination Derivative | — | 46.3 | 12.9 | 68.2
Income from equity-method affiliates | 17.4 | 0.5 | 27.7 | 0.5
Other income (expense), net | (16.0) | 3.1 | (44.6) | 0.2
Income (loss) before income taxes | 17.6 | 67.4 | (102.0) | 88.5
Income tax expense (benefit) | 16.1 | 28.1 | (3.5) | 42.1
Net income (loss) | 1.5 | 39.3 | (98.5) | 46.4
Net income attributable to noncontrolling interests | (0.5) | — | (0.8) | —
Net income (loss) attributable to Dauch | 1.0 | 39.3 | (99.3) | 46.4
Diluted earnings (loss) per share | — | 0.32 | (0.46) | 0.38

DAUCH CORPORATION

CONDENSED CONSOLIDATED BALANCE SHEETS

June 30, 2026 | December 31, 2025
(Unaudited)
ASSETS | (in millions)
Current assets
Cash and cash equivalents | 880.8 | 708.9
Restricted cash | — | 1,496.6
Accounts receivable, net | 1,517.0 | 733.0
Inventories, net | 1,000.3 | 466.4
Prepaid expenses and other | 329.9 | 230.1
Total current assets | 3,728.0 | 3,635.0
Property, plant and equipment, net | 4,108.0 | 1,591.5
Deferred income taxes | 360.9 | 235.9
Goodwill | 684.7 | 174.4
Other intangible assets, net | 348.6 | 375.2
GM postretirement cost sharing asset | 118.8 | 116.0
Operating lease right-of-use assets | 169.9 | 122.3
Investments in equity-method affiliates | 889.9 | 12.1
Other assets and deferred charges | 641.2 | 407.8
Total assets | 11,050.0 | 6,670.2
LIABILITIES AND STOCKHOLDERS' EQUITY
Current liabilities
Current portion of long-term debt | — | 10.4
Accounts payable | 1,698.1 | 718.3
Accrued compensation and benefits | 513.6 | 254.9
Deferred revenue | 23.4 | 38.5
Current portion of operating lease liabilities | 37.6 | 24.7
Accrued expenses and other | 394.1 | 187.2
Total current liabilities | 2,666.8 | 1,234.0
Long-term debt, net | 5,025.9 | 4,039.1
Deferred revenue | 40.4 | 33.9
Deferred income taxes | 266.0 | 9.1
Long-term portion of operating lease liabilities | 135.3 | 100.1
Postretirement benefits and other long-term liabilities | 1,400.1 | 614.0
Total liabilities | 9,534.5 | 6,030.2
Total Dauch stockholders' equity | 1,509.7 | 640.0
Noncontrolling interest in subsidiaries | 5.8 | —
Total stockholders' equity | 1,515.5 | 640.0
Total liabilities and stockholders' equity | 11,050.0 | 6,670.2

DAUCH CORPORATION

CONDENSED CONSOLIDATED STATEMENTS OF CASH FLOWS

(Unaudited)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-13_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

COMPANY OVERVIEW

Effective January 26, 2026, American Axle & Manufacturing Holdings, Inc. changed its name to Dauch Corporation. As used in this report, except as otherwise indicated in information incorporated by reference, references to "our Company," "we," "our," "us" or "Dauch" mean Dauch Corporation and its subsidiaries and predecessors, collectively.

Dauch Corporation is a premier Driveline and Metal Forming supplier serving the global automotive industry with a powertrain-agnostic product portfolio that supports electric, hybrid, and internal combustion vehicles. The company is headquartered in Detroit, Michigan, with operations that span 24 countries and more than 175 locations. Formed through the acquisition of Dowlais Group plc and its subsidiaries - GKN Automotive and GKN Powder Metallurgy, Dauch unites deep engineering roots with global manufacturing capabilities and an entrepreneurial spirit to move mobility forward.

We are a primary supplier of driveline components to General Motors Company (GM) for its full-size rear-wheel drive (RWD) light trucks, sport utility vehicles (SUV), and crossover vehicles manufactured in North America, supplying a significant portion of GM's rear axle and four-wheel drive and all-wheel drive (4WD/AWD) axle requirements for these vehicle platforms. We also supply GM with various products from our Metal Forming segment. Sales to GM were approximately 44% of our consolidated net sales in 2025, 42% in 2024, and 39% in 2023.

We are also a supplier to Ford Motor Company (Ford) for driveline system products on certain vehicle programs including the Bronco Sport, Maverick, Escape and Lincoln Nautilus, and we also sell various products to Ford from our Metal Forming segment. Sales to Ford were approximately 15% of our consolidated net sales in 2025, 13% in 2024, and 12% in 2023.

We also supply driveline system products to Stellantis N.V. (Stellantis) for programs including the heavy-duty Ram full-size pickup truck and its derivatives. In addition, we sell various products to Stellantis from our Metal Forming segment. Sales to Stellantis were approximately 13% of our consolidated net sales in both 2025 and 2024, and 16% in 2023.

No other customer represented 10% or more of consolidated net sales during these periods.

Acquisition of Dowlais Group plc

On February 3, 2026, we completed our previously announced acquisition of Dowlais Group plc (Dowlais) whereby we acquired the entire issued share capital of Dowlais (the Business Combination). Pursuant to the Business Combination, Dowlais shareholders received for each Dowlais ordinary share: 0.0881 shares of new Company common stock and 43 pence per share in cash (approximately $0.59 per share as of the closing date), resulting in the issuance of approximately 117 million shares (and an increase in authorized shares from 150 million to 375 million shares) and a total purchase price of approximately $1.7 billion. Following the close of the transaction, the combined company is headquartered in Detroit, Michigan and led by the Company's Chairman and CEO.

Disposition of AAM India Manufacturing Corporation Pvt., Ltd.

During 2025, we completed the sale of our commercial vehicle axle business and related assets in India (AAM India Manufacturing Corporation Pvt., Ltd.) to Bharat Forge Limited (BFL) for approximately $65 million, net of closing adjustments (the India Sale Agreement). For the years ended December 31, 2025 and 2024, we recorded impairment charges of $8 million and $12 million, respectively, to reduce the carrying value of this business to fair value less costs to sell.

Uncertainty Associated with Tariffs and Trade Relations

In 2025, the U.S. government implemented tariffs and increased certain existing tariffs on various products including assembled vehicles and automotive parts and components imported into the U.S., and there is considerable uncertainty around the extent, timing and duration of these tariffs. This has resulted in retaliatory tariffs against the U.S. by the governments of various countries, resulting in significant instability and uncertainty in U.S. trade relations with certain countries. Additionally, the expected 2026 review of the United States-Mexico-Canada Agreement (USMCA) could further contribute to this instability and uncertainty in trade relations.

For the year ended December 31, 2025, the net impact on earnings related to the aforementioned tariffs was approximately $10 million and we expect a continuing impact from tariffs in future periods. We are implementing mitigation actions and pursuing recoveries from our customers for the cost increases resulting from the tariffs but have not reached final agreement with all customers and therefore the total amount and timing of such recoveries is unknown. Further, certain of these recoveries may include government issued credits and there is uncertainty about whether we will be able to effectively monetize such credits.

Commercial Matters

In April 2024, one of our largest customers notified the Company that production purchase orders related to a previously announced contract to supply e-Beam axles for a future vehicle program were terminated. We believe that the termination of these purchase orders reflects, in part, the significant uncertainty currently underlying the electric vehicle environment, including volatility in estimated volumes and the timing of production.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

RESULTS OF OPERATIONS

NET SALES

Year Ended December 31,
(in millions) | 2025 | 2024 | Change | Percent Change
Net sales | 5,836.7 | 6,124.9 | (288.2) | (4.7) | %

The change in net sales in 2025, as compared to 2024, primarily reflects lower production volumes on certain vehicle programs that we support and a reduction of approximately $57 million as a result of the sale of AAM India Manufacturing Corporation Pvt., Ltd., which was completed on July 1, 2025. These decreases were partially offset by an increase of approximately $47 million associated with the effect of metal market pass-throughs to our customers and the impact of foreign exchange related to translation adjustments.

COST OF GOODS SOLD

Year Ended December 31,
(in millions) | 2025 | 2024 | Change | Percent Change
Cost of goods sold | 5,132.2 | 5,383.5 | (251.3) | (4.7) | %

The decrease in cost of goods sold in the year ended December 31, 2025, as compared to the year ended December 31, 2024, primarily reflects lower production volumes on certain vehicle programs that we support, as well as a reduction of approximately $53 million as a result of the sale of AAM India Manufacturing Corporation Pvt., Ltd., and the impact of improved operating performance. These decreases were partially offset by an increase of approximately $36 million associated with the effect of metal market pass-throughs to our customers and the impact of foreign exchange related to translation adjustments. For the year ended December 31, 2025, material costs were approximately 54% of total cost of goods sold, as compared to approximately 57% for the year ended December 31, 2024.

GROSS PROFIT

Year Ended December 31,
(in millions) | 2025 | 2024 | Change | Percent Change
Gross profit | 704.5 | 741.4 | (36.9) | (5.0) | %

Gross margin was 12.1% in both 2025 and 2024. Gross profit and gross margin were impacted by the factors discussed in Net Sales and Cost of Goods Sold above.

SELLING, GENERAL AND ADMINISTRATIVE EXPENSES (SG&A)

Year Ended December 31,
(in millions) | 2025 | 2024 | Change | Percent Change
Selling, general and administrative expenses | 389.0 | 387.1 | 1.9 | 0.5 | %

SG&A as a percentage of net sales was 6.7% in 2025 as compared to 6.3% in 2024. R&D expense, net of engineering, design and development (ED&D) recoveries, was approximately $147.0 million in 2025, as compared to $159.0 million in 2024. The change in SG&A in 2025, as compared to 2024, was primarily attributable to increased incentive compensation expense, which was substantially offset by the decrease in R&D expense.

AMORTIZATION OF INTANGIBLE ASSETS Amortization expense related to intangible assets was $81.8 million for the year ended December 31, 2025 as compared to $82.9 million for the year ended December 31, 2024.

IMPAIRMENT CHARGES In connection with the India Sale Agreement, we recorded impairment charges of $8.0 million and $12.0 million in the years ended December 31, 2025 and December 31, 2024, respectively, to reduce the carrying value of this business to fair value less cost to sell. See Note 2 - Acquisitions and Dispositions for additional detail regarding the India Sale Agreement.

RESTRUCTURING AND ACQUISITION-RELATED COSTS Restructuring and acquisition-related costs were $113.4 million for the year ended December 31, 2025, as compared to $18.0 million for the year ended December 31, 2024. The change in restructuring and acquisition-related costs was primarily related to acquisition-related costs incurred in connection with the Business Combination, as well as increased restructuring costs as we focused on optimizing our cost structure in 2025 ahead of the closing date of the Business Combination.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-13_item1_business.md)

Item 1. Business

Effective January 26, 2026, American Axle & Manufacturing Holdings, Inc. changed its name to Dauch Corporation. As used in this report, except as otherwise indicated in information incorporated by reference, references to "our Company," "we," "our," "us" or "Dauch" mean Dauch Corporation and its subsidiaries and predecessors, collectively.

General Development of Business

The Company, a Delaware corporation, is a successor to American Axle & Manufacturing of Michigan, Inc., a Michigan corporation, pursuant to a migratory merger between these entities in 1999. In 2017, we acquired Metaldyne Performance Group, Inc. (MPG), with MPG becoming a wholly-owned subsidiary of the Company.

On February 3, 2026, we completed our previously announced acquisition of Dowlais Group plc (Dowlais) whereby we acquired the entire issued share capital of Dowlais (the Business Combination). Pursuant to the Business Combination, Dowlais shareholders received for each Dowlais ordinary share: 0.0881 shares of new Company common stock and 43 pence per share in cash (approximately $0.59 per share as of the closing date), resulting in the issuance of approximately 117 million shares (and an increase in authorized shares from 150 million to 375 million shares) and a total purchase price of approximately $1.7 billion. Following the close of the transaction, the combined company is headquartered in Detroit, Michigan and led by the Company's Chairman and CEO.

Narrative Description of Business

Company Overview

Dauch Corporation is a premier Driveline and Metal Forming supplier serving the global automotive industry with a powertrain-agnostic product portfolio that supports electric, hybrid, and internal combustion vehicles. The company is headquartered in Detroit, Michigan, with operations that span 24 countries and more than 175 locations. Formed through the acquisition of Dowlais Group plc and its subsidiaries - GKN Automotive and GKN Powder Metallurgy, Dauch unites deep engineering roots with global manufacturing capabilities and an entrepreneurial spirit to move mobility forward.

Major Customers

We are a primary supplier of driveline components to General Motors Company (GM) for its full-size rear-wheel drive (RWD) light trucks, sport utility vehicles (SUV), and crossover vehicles manufactured in North America, supplying a significant portion of GM's rear axle and four-wheel drive and all-wheel drive (4WD/AWD) axle requirements for these vehicle platforms. We also supply GM with various products from our Metal Forming segment. Sales to GM were approximately 44% of our consolidated net sales in 2025, 42% in 2024, and 39% in 2023.

We are also a supplier to Ford Motor Company (Ford) for driveline system products on certain vehicle programs including the Bronco Sport, Maverick, Escape and Lincoln Nautilus, and we also sell various products to Ford from our Metal Forming segment. Sales to Ford were approximately 15% of our consolidated net sales in 2025, 13% in 2024, and 12% in 2023.

We also supply driveline system products to Stellantis N.V. (Stellantis) for programs including the heavy-duty Ram full-size pickup truck and its derivatives. In addition, we sell various products to Stellantis from our Metal Forming segment. Sales to Stellantis were approximately 13% of our consolidated net sales in 2025, 13% in 2024, and 16% in 2023.

No other customer represented 10% or more of consolidated net sales during these periods.

Business Strategy

We have aligned our business strategy to build value for our key stakeholders. We accomplish our strategic objectives by capitalizing on our competitive strengths and continuing to diversify our customer, product and geographic sales mix, while providing exceptional value to our customers. We are focused on securing and enhancing our core business of manufacturing products that support internal combustion engine (ICE) vehicle programs by delivering operational excellence and quality products to our customers, while growing our hybrid and electric vehicle business, as end-user acceptance of these vehicle types is expected to grow in the future.

Competitive Strengths

We achieve our strategic objectives by emphasizing a commitment to:

Sustaining our operational excellence and focus on cost management.

• We deliver operational excellence by leveraging our global standards, policies and best practices across all disciplines through the use of our operating system, which includes, among other elements, our S 4 (S-to-the-fourth) safety system, Q 4 (Q-to-the-fourth) quality system and E 4 (E-to-the-fourth) energy and environmental sustainability system. We use our operating system to focus on customer satisfaction, lean production and efficient cost management, which allows us to improve quality, eliminate waste, and reduce lead time and total costs globally.

• We maintain a cost competitive, operationally flexible global manufacturing, engineering and sourcing footprint to compete in global growth markets, support global product development initiatives and maintain regional cost competitiveness.

• Our business is vertically integrated to reduce cost and mitigate risk. Our Metal Forming segment, in addition to supplying component parts to many external customers, is a key supplier to our Driveline segment, helping to ensure continuity of supply for certain parts to our largest manufacturing facilities.

• During 2025, we launched seven programs across our business units for our customers including Ford, Stellantis, Skywell and Dongfeng Motor Group. In 2026, we expect to launch new and replacement programs for a variety of customers across our business units with GM, Audi, Volkswagen, FAW Group and Phoebus.

Maintaining our high quality standards, which are the foundation of our product durability and reliability.

• Our Q 4 internal quality assurance system drives continuous improvement to meet and exceed the growing expectations of our OEM customers.

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

**Present:** meta.json, form4_summary.md, 8-K_2026-08-07_2-02-results.md, 10-K_2026-02-13_item7_mdna.md, 10-K_2026-02-13_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
