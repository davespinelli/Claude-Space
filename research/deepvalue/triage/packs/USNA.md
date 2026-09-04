# Triage pack — USNA · USANA HEALTH SCIENCES INC

_Generated 2026-09-04 15:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** USNA · **Name:** USANA HEALTH SCIENCES INC
- **CIK:** 0000896264
- **SIC:** 2833 — Medicinal Chemicals & Botanical Products
- **Fiscal year end (MM-DD):** 01-03
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/USNA

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** USANA HEALTH SCIENCES INC
- **CIK:** 896,264 · **SIC:** 2833 (Medicinal Chemicals & Botanical Products) · **Exchange:** NYSE

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 14.43 |
| mktcap | $266.6M |
| ev | $98.1M |
| ev_ebit | 2.6x |
| fcf | $8.5M |
| fcf_yield | 3.2% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 8.3% |
| net_debt | -$168.6M |
| net_debt_ebit | -4.5x |
| cash | $168.6M |
| ltd | $0.00 |
| equity | $526.3M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $925.3M |
| revenue_prior | $854.5M |
| rev_growth | 8.3% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $37.4M |
| net_income | $10.8M |
| cfo | $22.3M |
| capex | $13.8M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 1.1% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 18,476,534 |
| shares_py | 18,271,836 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -52.7% |
| r6m | -20.7% |
| off_52w_high | -54.7% |
| adv20 | $3.2M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.38 |
| r_ev_ebit | 0.98 |
| r_roic | 0.65 |
| r_rev_growth | 0.61 |
| r_buyback | 0.44 |
| score | 0.61 |

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
| rank | 131 |

**Screen rationale:** cheap at 2.6x EV/EBIT; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **18,476,534** (CY2026Q2I) vs **18,271,836** prior year (CY2025Q2I)
- Change: **1.1%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-02 among the 3 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 13,074 sh / $250,647 -> net $-250,647 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 27 (open-market buys 0, sales 4).

| code | rows |
|---|---|
| F | 5 |
| M | 18 |
| S | 4 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-04_2-02-results.md)

_Extraction: started at the first release heading, 'USANA Health Sciences Reports Second Quarter 2026 Results'; skipped 10 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (q22026earningsreleaseex991.htm)

USANA Health Sciences Reports Second Quarter 2026 Results

Company Continues Evolution to a Diversified, Omnichannel Health and Wellness Business

SALT LAKE CITY, August 4, 2026 (BUSINESS WIRE)—USANA Health Sciences, Inc. (NYSE: USNA) today announced financial results for its fiscal second quarter ended July 4, 2026.

Key Financial Results

Second Quarter 2026 vs. Second Quarter 2025

• Net sales of $223 million versus $236 million.

• Net loss of $(21.4) million, which includes an estimated preliminary non-cash impairment charge (3) of $29.1 million, versus net earnings of $9.7 million.

• Diluted EPS of $(1.16) as compared with $0.52.

• Adjusted diluted EPS (1) of $(0.07) as compared with $0.74.

• Adjusted EBITDA (2) of $27.8 million versus $30.5 million.

• Core Nutritional Active Customers of 384,000 versus 418,000.

• Hiya Active Monthly Subscribers of 166,000 versus 200,400.

• Company updates fiscal 2026 guidance.

Q2 2026 Consolidated Performance

Q2 2026 | Year-Over-Year | Sequentially
Net Sales | $223 million | -5% (+$6 million or +3% FX impact) | -11%
Net Loss* | $(21.4) million | N/A | N/A
Diluted EPS | $(1.16) | N/A | N/A
Adjusted Diluted EPS (1) | $(0.07) | N/A | N/A
Adjusted EBITDA (2) | $27.8 million | -9% | -2%

*Income tax expense of $9 million added to a pretax loss of $(19) million for Q2 2026.

Net Loss, EPS and EBITDA figures represent amounts attributable to USANA and excludes the noncontrolling interest of 21.2% in Hiya.

"Our consolidated second quarter results reflect mixed performance as the Core Nutritional business delivered results generally in line with our expectations, while our ventures businesses performed below expectations," said Kevin Guest, Chairman and Chief Executive Officer. "Specifically, Hiya continued to experience a challenging digital marketing environment, which pressured topline performance, subscriber growth, and margins. Additionally, Rise Wellness experienced a packaging-related disruption that impacted its commercial execution during the quarter. While we believe that these challenges for Hiya and Rise are temporary, and both companies remain well positioned to execute their growth strategies, we now expect net sales for these businesses during the full year to be below our prior expectations and are updating our outlook accordingly.

"We remain confident in USANA's strategic transformation from a single-channel direct sales business into a diversified, omnichannel health and wellness company built on consumer acquisition and loyalty. We are continuing to evolve our Brand Partner incentive plan, accelerate product innovation, and modernize our technology infrastructure. We remain confident that these initiatives will lead to long-term sustainable growth.

"Hiya's talented management team continues to embrace the opportunity to leverage their brand across additional channels to reach a broader consumer base, while continuing to build on strong performance at a major national retailer, early-stage international expansion, and encouraging momentum in additional e-commerce channels. Rise Wellness' high growth protein beverage brand, Protein Pop, is just a year old, and continues to attract new retailers, expand its presence with existing retailers and create the foundation for an exciting and expanded product pipeline. We recognize this progress will not always be linear quarter to quarter, and as we manage the business with that expectation in mind, our focus remains on building long-term loyalty from the consumers and Brand Partners who depend on our brands."

Q2 2026 Segment Results

Core Nutritional

Core Nutritional
Q2 2026 | Year-Over-Year | Sequentially
Net Sales | $192 million | -4% | -6%
Active Customers | 384,000 | -8% | -5%

Asia Pacific Region
Q2 2026 | Year-Over-Year | Year-Over-Year (Constant Currency) | Sequentially
Net Sales | $157 million | -4% | -7% | -7%
Active Customers | 307,000 | -9% | N/A | -6%

Asia Pacific Sub-Regions
Q2 2026 | Year-Over-Year | Year-Over-Year (Constant Currency) | Sequentially
Greater China | Net Sales | $114 million | +1% | -3% | -7%
Active | 216,000 | -6% | N/A | -8%
Customers
North Asia | Net Sales | $14 million | -20% | -14% | -10%
Active | 32,000 | -14% | N/A | Flat
Customers
Southeast Asia Pacific | Net Sales | $29 million | -13% | -15% | -6%
Active | 59,000 | -13% | N/A | Flat
Customers

Americas and Europe Region
Q2 2026 | Year-Over-Year | Year-Over-Year (Constant Currency) | Sequentially
Net Sales | $34 million | -5% | -7% | -2%
Active Customers | 77,000 | -6% | N/A | -1%

Hiya Health
Q2 2026 | Year-Over-Year | Sequentially
Net Sales | $28 million | -17% | -12%
Active Monthly Subscribers | 166,000 | -17% | -11%

Rise Wellness

Q2 2026 | Year-Over-Year | Sequentially
Net Sales | $3 million | +40% | -75%

Balance Sheet

The Company ended the quarter with $169 million in cash and cash equivalents and zero debt. As of July 4, 2026, inventory totaled $95 million, a decrease of approximately $13 million, or 12% compared to balances at year-end 2025.

The Company did not repurcha se any shar es during the quarter and has approximately $34 million remaining under the current share repurchase authorization as of the end of the second quarter.

Fiscal Year 2026 Outlook

The Company is updating its outlook for fiscal year 2026, as follows:

Fiscal Year 2026 Outlook
Updated Estimate | Previous Range
Core Nutritional business net sales | $750 million* | $720 to $765 million
Hiya net sales | $125 million | $140 to $155 million
Rise Wellness net sales | $35 million | $65 to $80 million
Consolidated net sales | $910 million | $925 million to $1.0 billion
Net (loss) earnings | $(11) million | $20 million to $27 million
Diluted EPS | $(0.61) | $1.11 to $1.45
Adjusted diluted EPS (1) | $0.76 | $1.95 to $2.29
Adjusted EBITDA (2) | $87 million | $101 million to $109 million

*Reflects an expected favorable currency exchange rate impact of approximately $20 million, or 2% of net sales and one less week of operations compared to fiscal year 2025 which was a 53-week year.

"Our GAAP net loss and negative Adjusted diluted EPS this quarter reflect lower-than-expected commercial performance from Hiya and Rise, and we've updated our full-year outlook accordingly," said Doug Hekking, Chief Financial Officer. "Related to Hiya, we recorded an estimated preliminary non-cash goodwill impairment charge of $29 million. This non-cash charge primarily reflects recent performance and changes in near-term forecasts, as well as updated valuation assumptions under applicable accounting standards, including adjustments to market multiples and discount rates. Hiya continues to be a core element of our strategy and we remain confident and committed to leveraging the brand across channels and international markets to drive long-term growth. Additionally, an increase in the annual estimated income tax rate, which was driven by both current performance and lower near-term forecasts, disproportionately impacted the current-year quarter and contributed to the net loss.

"Our balance sheet continues to be a source of strength, as we ended the period with $169 million in cash and debt-free. We also generated $20 million in free cash flow this quarter, driven in large part by improved working capital management. Financial flexibility remains important and is central to how we're investing in USANA's continued evolution from a single-channel direct sales business into a diversified, omnichannel health and wellness company."

(1) Adjusted Diluted (Loss) Earnings Per Share is a non-GAAP financial measure. The Company excludes cost realignment expenses, impairment expense, gain on sale of assets, and acquisition-related costs, such as business transaction costs, integration expense and amortization expense from acquisition-related intangible assets in calculating Adjusted Diluted (Loss) Earnings Per Share. Please refer to "Non-GAAP Financial Measures" and "Reconciliation of Diluted (Loss) Earnings Per Share (GAAP) to Adjusted Diluted (Loss) Earnings Per Share (Non-GAAP)" in this press release for an explanation and reconciliation of this non-GAAP financial measure.

(2) Adjusted EBITDA is a non-GAAP financial measure. Please refer to "Non-GAAP Financial Measures" and "Reconciliation of Net (Loss) Earnings (GAAP) to Adjusted EBITDA (Non-GAAP)" in this press release for an explanation and reconciliation of this non-GAAP financial measure.

(3) Estimated preliminary non-cash impairment charge was recognized, during the second quarter of 2026, to reduce goodwill, which impacted the Hiya reporting unit.

Non-GAAP Financial Measures

This press release contains the non-GAAP financial measures Adjusted EBITDA and Adjusted Diluted EPS. Adjusted EBITDA is a non-GAAP financial measure of (loss) earnings before interest, taxes, depreciation, and amortization that also excludes certain adjustments as indicated below in the reconciliation from net (loss) earnings. Adjusted Diluted EPS is a non-GAAP financial measure of diluted (loss) earnings per share that excludes certain adjustments as indicated below in the reconciliation from diluted EPS.

Adjusted EBITDA (non-GAAP) is net (loss) earnings (its most directly comparable GAAP financial measure) adjusted for interest expense, net, (benefit from) provision for income taxes, depreciation and amortization, non-cash share-based compensation, transaction-related expenses and integration costs for the Hiya acquisition, cost realignment expenses, impairment expense, and gain on sale of assets. Adjusted EBITDA attributable to USANA (non-GAAP) is Adjusted EBITDA (non-GAAP) further adjusted to exclude the Adjusted EBITDA attributable to non-controlling interest related to Hiya.

Adjusted diluted (loss) earnings per share (non-GAAP) is diluted (loss) earnings per share (its most directly comparable GAAP financial measure) adjusted for amortization of intangible assets, transaction-related expenses and integration costs related to the Hiya acquisition, cost realignment expenses, impairment expense, and gain on sale of assets.

Management believes that Adjusted EBITDA (non-GAAP), Adjusted EBITDA attributable to USANA (non-GAAP), and Adjusted diluted (loss) earnings per share (non-GAAP), along with GAAP measures used by management, most appropriately reflect how the Company measures the business internally.

The Company prepares its financial statements using U.S. generally accepted accounting principles ("GAAP") and investors should not directly compare with or infer relationship from any of the Company's operating results presented in accordance with GAAP to Adjusted EBITDA and Adjusted diluted (loss) earnings per share. Non-GAAP financial measures have limitations in their usefulness to investors because they have no standardized meaning prescribed by GAAP and are not prepared under any comprehensive set of accounting rules or principles. In addition, other companies, including companies in our industry, may calculate similarly titled non-GAAP financial measures differently or may use other measures to evaluate their performance, all of which could reduce the usefulness of non-GAAP financial information as a tool for comparison. As a result, the non-GAAP financial information is presented for supplemental informational purposes only and should not be considered in isolation from, or as a substitute for financial information presented in accordance with GAAP.

Reconciliation of Net (Loss) Earnings (GAAP) to Adjusted EBITDA (non-GAAP)

(in thousands)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-16_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We develop and manufacture high quality nutritional supplements, functional foods and personal care products that are sold throughout the world. Historically, we have distributed our products through the direct selling channel, because we believe it is conducive to our vision of improving the overall health and nutrition of individuals and families around the world. On December 23, 2024, we acquired a 78.85% controlling ownership interest in Hiya, a leading provider of high-quality children's health and wellness products. We believe that the addition of Hiya to our business promotes our vision and adds a diversified layer of growth in the direct-to-consumer channel. In 2022, we acquired Rise and have expanded Rise's product offering, distribution channel, and customer base over the last three years. Consequently, through our core nutritional business, Hiya and Rise, we now operate and sell products through an omni-channel platform, which includes direct selling, direct-to-consumer, third-party marketplace and retail channels and organize our business into two reportable segments: Core nutritional and Hiya direct-to-consumer.

Core nutritional: Core nutritional is our primary business with approximately 84% of consolidated net sales during 2025. Our core nutritional customer base is primarily comprised of two types of customers: "Brand Partners" and "Preferred Customers," referred to together as "active Customers." Our Brand Partners also sell our products to retail customers. Brand Partners share in our company vision by acting as independent distributors of our products in addition to purchasing our products for their personal use. In 2023, we launched our Affiliate program in the United States, Canada, and Mexico, which offers another sales and compensation opportunity to individuals who are interested in selling USANA products. Affiliates are discussed and reported in the report as part of our Brand Partners. Preferred Customers purchase our products strictly for personal use and are not permitted to resell or to distribute the products. We only count as active Customers those Brand Partners and Preferred Customers who have purchased from us at any time during the most recent

three-month period. As of January 3, 2026, we had approximately 387,000 active Customers worldwide in our core nutritional business.

We have core nutritional operations in multiple markets, with sales and expenses being generated and incurred in multiple currencies. Our reported U.S. dollar sales and earnings can be significantly affected by fluctuations in currency exchange rates. In general, our operating results are affected positively by a weakening of the U.S. dollar and negatively by a strengthening of the U.S. dollar. During 2025, net sales outside of the United States represented 90.3% of core nutritional net sales. In our net sales discussions that follow, we approximate the impact of currency fluctuations on net sales by translating current year sales at the average exchange rates in effect during the comparable periods of the prior year.

Hiya direct-to-consumer: Hiya operates and sells products to customers in the United States. Hiya's customers purchase Hiya products for personal use primarily through a subscription model, which is intended to provide a steady, predictable income stream for Hiya. The ongoing nature of subscriptions fosters stronger relationships with customers by making it easier for them to receive products regularly, which we believe leads to retention and loyalty. Hiya's subscription model also provides important data on customer preferences and behaviors, which enables personalized offerings, efficient marketing and data-driven innovation insights. We evaluate Hiya's customer counts and behavior through its monthly subscribers and only count as "active Monthly Subscribers" those Hiya customers who have purchased from Hiya at any time during the most recent month. As of January 3, 2026, Hiya had approximately 181,700 active Monthly Subscribers.

Other: The other category is comprised of Rise Bar Wellness, Inc. ("Rise") and Oola Global, LLC ("Oola"), which are both businesses we acquired in 2022. Rise manufactures and sells high-quality protein bars, powdered drinks, and clear protein drinks that are formulated to help customers achieve their health goals through clean and simple ingredients. Oola is a direct selling company that offers a personal development framework and nutritional products that helps individuals create a life of balance, g rowth, and purpose.

We discuss our other category, which is not a reportable segment, together with our "core nutritional" segment.

The following table summarizes operating results as a percentage of net sales for the current and prior-year periods, as indicated :

Year Ended
January 3, 2026 | December 28, 2024
Core nutritional & other | Hiya direct-to-consumer | Consolidated | Core nutritional & other | Hiya direct-to-consumer | Consolidated
Net sales | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0%
Cost of sales | 19.5% | 35.1% | 21.7% | 18.8% | 30.4% | 18.9%
Gross profit | 80.5% | 64.9% | 78.3% | 81.2% | 69.6% | 81.1%
Operating expenses:
Brand Partner incentives | 42.4% | —% | 36.3% | 42.7% | —% | 42.6%
Selling, general and administrative | 32.2% | 62.3% | 36.5% | 30.7% | 62.2% | 30.8%
Cost realignment and impairment | 1.7% | —% | 1.5% | —% | —% | —%
Total operating expenses | 76.3% | 62.3% | 74.3% | 73.4% | 62.2% | 73.4%
Earnings from operations | 4.2% | 2.6% | 4.0% | 7.8% | 7.4% | 7.7%
Amortization of acquired intangible assets | 0.2% | 13.8% | 2.1% | 0.1% | 14.9% | 0.2%

Customers

Core nutritional

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Summary of 2025 Financial Results

Our discussion and analysis is focused on our 2025 and 2024 financial results, including comparisons of our year-over-year performance between these years. Discussion and analysis of our 2023 fiscal year specifically, as well as the year-over-year comparison of our 2024 financial performance to 2023, are located in Part II, Item 7. " Management's Discussion and Analysis of Financial Condition and Results of Operations " in our Annual Report on Form 10-K for the fiscal year ended December 28, 2024, filed with the SEC on March 12, 2025, which is available on our investor relations website at https://ir.usana.com or the SEC's website at www.sec.gov. That information is incorporated by reference into this report.

Net sales in 2025 increased 8.3%, or $70.8 million, to $925.3 million, compared with 2024. The net sales increase was primarily the result of adding the year-to-date incremental sales for Hiya of $130.0 million, partially offset by a decline in net sales for the core nutritional segment. Additionally, unfavorable changes in currency exchange rates decreased net sales for the year by an estimated $3.1 million.

Net earnings attributable to USANA decreased 74.4% to $10.8 million in 2025, when compared with 2024. The decrease in net earnings attributable to USANA was primarily the result of a lower operating margin and a substantial increase in the effective tax rate for 2025.

Fiscal Year 2025 compared to Fiscal Year 2024

Net Sales

The following table summarizes the changes in our net sales by segment for the fiscal years ended January 3, 2026, and December 28, 2024:

Net Sales by Region (in thousands) | Change from prior year | Percent change | Currency impact on sales | Percent change excluding currency impact
Year Ended
January 3, 2026 | December 28, 2024
Core nutritional:
Asia Pacific
Greater China | 424,541 | 45.9 | % | 457,976 | 53.6 | % | (33,435) | (7.3) | % | (180) | (7.3) | %
Southeast Asia Pacific | 131,996 | 14.3 | % | 146,795 | 17.2 | % | (14,799) | (10.1) | % | 1,950 | (11.4) | %
North Asia | 70,627 | 7.6 | % | 78,214 | 9.1 | % | (7,587) | (9.7) | % | (3,068) | (5.8) | %
Asia Pacific total | 627,164 | 67.8 | % | 682,985 | 79.9 | % | (55,821) | (8.2) | % | (1,298) | (8.0) | %
Americas and Europe | 148,288 | 16.0 | % | 162,804 | 19.1 | % | (14,516) | (8.9) | % | (1,757) | (7.8) | %
Core nutritional total | 775,452 | 83.8 | % | 845,789 | 99.0 | % | (70,337) | (8.3) | % | (3,055) | (8.0) | %
Hiya (1) | 131,971 | 14.3 | % | 1,970 | 0.2 | % | 130,001 | N/A | — | N/A
Other | 17,834 | 1.9 | % | 6,744 | 0.8 | % | 11,090 | 164.4 | % | — | 164.4 | %
Consolidated total | 925,257 | 100.0 | % | 854,503 | 100.0 | % | 70,754 | 8.3 | % | (3,055) | 8.6 | %

(1) Percentage change for Hiya is not applicable due to timing of the acquisition.

Core Nutritional Net Sales

Net sales in our core nutritional business (discussed with our other category) in 2025 were $793.3 million, down 6.9% when compared to the corresponding period of 2024. On a constant currency basis, net sales in the core nutritional segment declined 6.6%. The decrease in net sales was mainly due to a 14.8% decrease in active Customers, partially offset by a 4.4% increase in average spend per customer and one additional week of operations compared to fiscal year 2024 which was a 52-week year.

Asia Pacific: Net sales declined 8.2%, or 8.0% on a constant currency basis, in this region during the current year period. Active Customers in this region declined 10.8% year-over-year, partially offset by 3.2% higher average spend per customer throughout the region. The net sales decline reflects a challenging economic and operating environment.

The following table summarizes changes in local currency net sales, active Customer counts, and average spend per active Customer for the markets primarily contributing to the decline in net sales within the Asia Pacific region:

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-16_item1_business.md)

Item 1. Business

General

USANA Health Sciences, Inc. develops and manufactures high-quality nutritional supplements, functional foods and personal care products that are sold throughout the world. In 2025, we generated $925 million in net sales and finished the year with approximately 387,000 active Customers in our core nutritional business. We were founded in 1992 by Myron W. Wentz, Ph.D. and since that time, we have developed and manufactured high quality, science-based nutritional, personal care and skincare products with a primary focus on promoting long-term health and wellness. We are committed to continuous product innovation and sound scientific research. We have operations in 25 geographic markets worldwide. Historically, we have distributed our products through the direct selling channel, because we believe it is conducive to our vision of improving the overall health and nutrition of individuals and families around the world. Mainland China ("China") is our largest market and single largest source of revenue, representing approximately 41.3% of net sales and approximately 49.9% of core nutritional active Customers. As a U.S.-based multi-national corporation with an expanding international presence, our operating results are sensitive to currency fluctuations, as well as economic and political conditions in markets throughout the world. Additionally, we are subject to the various laws and regulations in the United States, China, and the other markets in which we operate with respect to the products that we manufacture, and sell, and our method of distribution. We are a U.S. public company listed on the New York Stock Exchange ("NYSE") and subject to the rules of the SEC.

In December 2024, we acquired a 78.85% ownership interest in Hiya Health Products, LLC ("Hiya"), a leading direct-to-consumer provider of high-quality children's health and wellness products (the "Hiya Acquisition"). We believe that the addition of Hiya to our business promotes our vision and adds a diversified layer of growth in the direct-to-consumer channel. In 2022, we acquired Rise and have expanded Rise's product offering, distribution channel, and customer base over the last three years. Consequently, through our core nutritional business, Hiya and Rise, we now operate and sell products through an omni-channel platform, which includes direct selling, direct-to-consumer, third-party marketplace (i.e., Amazon), and retail channels.

This " Item 1. Business " provides detailed information about our worldwide business, including who we are, what we do and where we are headed. Unless otherwise specified, current information reported in this Annual Report on Form 10-K for the fiscal year ended January 3, 2026 (this "report" or "Annual Report") is as of or for the fiscal year ended January 3, 2026. We also discuss the development of our company and the geographic areas where we do business. For the year ended January 3, 2026, there were no material changes to our corporate structure or our method of conducting business.

Our Business

We organize our business into two reportable segments: Core nutritional and Hiya direct-to-consumer.

Core nutritional: The customer base for our core nutritional segment is primarily comprised of two types of customers" "Brand Partners" and "Preferred Customers" referred to collectively as "active Customers." Our Brand Partners also sell our products to retail customers. Brand Partners share in our company vision by acting as independent distributors of our products, in addition to purchasing our products for their personal use. We also utilize an Affiliate sales program in the United States, Canada, Mexico, and India and are evaluating introducing the program in other markets. This program offers another sales and compensation opportunity to individuals who are interested in selling USANA products. Affiliates are discussed and reported in this report as part of our Brand Partners. Preferred Customers purchase our products strictly for personal use and are not permitted to resell or to distribute the products. We only count as active Customers those Brand Partners and Preferred Customers who have purchased from us at any time during the most recent three-month period.

Hiya direct-to-consumer: Hiya operates and sells products to customers in the United States and, in 2026, is expanding into Canada and the United Kingdom. Additionally, Hiya will be expanding in the retail channel beginning in the second quarter of 2026. Hiya's customers purchase Hiya products for personal use primarily through a subscription model, which is intended to provide a steady, predictable income stream for the Company. The ongoing nature of subscriptions fosters stronger relationships with customers by making it easier for them to receive products regularly, which we believe leads to retention and loyalty. Hiya's subscription model also provides important data on customer preferences and behaviors, which enables personalized offerings, efficient marketing and data-driven innovation insights. We evaluate Hiya's customer counts and behavior through its monthly subscribers and only count as "active Monthly

Subscribers" those Hiya customers who have purchased from Hiya at any time during the most recent month. As of January 3, 2026, Hiya had approximately 181,700 active Monthly Subscribers.

Other: The customer base for our "other" category is comprised of customers of Rise and Oola Global, LLC ("Oola"), which are both businesses we acquired in 2022. Rise manufactures and sells high-quality protein bars, powdered protein drinks, and ready-to-drink ("RTD") liquid protein drinks that are formulated to help customers achieve their health goals through clean and simple ingredients. Oola is a direct selling company that offers a personal development framework and nutritional products that helps individuals create a life of balance, growth, and purpose.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-16_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-16_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-16_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-04_2-02-results.md, 10-K_2026-03-16_item7_mdna.md, 10-K_2026-03-16_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
