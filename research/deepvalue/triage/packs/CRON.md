# Triage pack — CRON · Cronos Group Inc.

_Generated 2026-09-04 20:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** CRON · **Name:** Cronos Group Inc.
- **CIK:** 0001656472
- **SIC:** 2833 — Medicinal Chemicals & Botanical Products
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/CRON

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Cronos Group Inc.
- **CIK:** 1,656,472 · **SIC:** 2833 (Medicinal Chemicals & Botanical Products) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 3.26 |
| mktcap | $1.2B |
| ev | $734.0M |
| ev_ebit | n/a |
| fcf | $149k |
| fcf_yield | 0.0% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -2.3% |
| net_debt | -$467.0M |
| net_debt_ebit | n/a |
| cash | $467.0M |
| ltd | $0.00 |
| equity | $1.1B |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $146.6M |
| revenue_prior | $117.6M |
| rev_growth | 24.6% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$17.4M |
| net_income | -$2.9M |
| cfo | $25.9M |
| capex | $25.7M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -3.8% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 368,412,864 |
| shares_py | 382,939,590 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 7.5% |
| r6m | 26.8% |
| off_52w_high | -8.2% |
| adv20 | $4.8M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.21 |
| r_ev_ebit | 0.00 |
| r_roic | 0.25 |
| r_rev_growth | 0.86 |
| r_buyback | 0.84 |
| score | 0.48 |

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
| rank | 262 |

**Screen rationale:** revenue +24.6%; buying back stock -3.8%; debt data missing (net cash unverified); 12-1 momentum 7.5%


## 3. Share count trend

- Shares outstanding: **368,412,864** (CY2026Q2I) vs **382,939,590** prior year (CY2025Q2I)
- Change: **-3.8%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-05-11** — Item 1.01 (Entry into a Material Definitive Agreement): On May 8, 2026, Cronos Group Inc. (the "Company"), its indirect wholly owned subsidiary, CGM B.V. (the "Purchaser"), "Ring" International Holding AG ("Ring"), and Landewyck Tobacco S.A. ("Landewyck," and together with Ring, the "Sellers") entered into an...

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 33 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 4 |
| F | 7 |
| M | 22 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'Cronos Group Reports 2026 Second Quarter Results'; skipped 45 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (pressreleaseq22026qformat.htm)

Cronos Group Reports 2026 Second Quarter Results

Organically achieved record net revenue, gross profit, and Adjusted EBITDA while reducing share count

Net revenue in Q2 2026 increased by 51% year-over-year on an organic, constant-currency basis

Delivered record net revenue in Canada, with Spinach ® maintaining #1 market share in vapes and edibles 1

Tenth consecutive quarter of record net revenue in Israel, where PEACE NATURALS ® continues to be the #1 cannabis brand 2

Generated record net revenue outside Canada and Israel, led by strong demand for PEACE NATURALS ® in Germany

Repurchased 12.3 million shares in the first half of 2026

TORONTO, August 6, 2026 - Cronos Group Inc. (NASDAQ: CRON) (TSX: CRON) ("Cronos" or the "Company"), today announced its 2026 second quarter business results.

"Cronos delivered a record second quarter by organically achieving record net revenue, record gross profit and record Adjusted EBITDA, while also reducing our share count. Cronos Israel delivered its tenth consecutive quarter of record net revenue, continuing to secure PEACE NATURALS ® as the leading cannabis brand in the country. Outside of Israel, our international business also delivered a record net revenue quarter, led by momentum in Germany. In Canada, the Spinach ® brand continued to gain significant market share, maintaining its #1 position in vapes for the second consecutive quarter and its #1 position in edibles for the eighth consecutive quarter 1 , while also making notable gains in pre-rolls and flower," said Mike Gorenstein, Chairman, President and CEO of Cronos.

"We're executing with discipline across our strategic priorities and our results reflect it. We remain active under our share repurchase program and continue to believe the repurchases represent an attractive use of capital. Backed by an industry-leading balance sheet and positive cash flow from operations, we are well positioned to invest in our growth strategy while returning capital to shareholders and maintaining optionality to be opportunistic as attractive opportunities arise."

1 Hifyre Retail Analytics - National Retail Dollar by Brand in Canada - Q2 2026.

2 Market share and ranking information from pharmacy data collected by Cronos - Q2 2026.

Consolidated Financial Results

The tables below set forth our condensed consolidated results of operations, expressed in thousands of United States ("U.S.") dollars for the periods presented. Our condensed consolidated financial results for these periods are not necessarily indicative of the consolidated financial results that we will achieve in future periods.

(in thousands of USD) | Three months ended June 30, | Change | Six months ended June 30, | Change
2026 | 2025 | % | 2026 | 2025 | %
Net revenue | 53,007 | 33,455 | 19,552 | 58 | % | 98,217 | 65,717 | 32,500 | 49 | %
Cost of sales | 24,168 | 18,865 | 5,303 | 28 | % | 49,560 | 37,393 | 12,167 | 33 | %
Inventory write-down | 388 | 86 | 302 | 351 | % | 1,053 | 86 | 967 | 1124 | %
Gross profit | 28,451 | 14,504 | 13,947 | 96 | % | 47,604 | 28,238 | 19,366 | 69 | %
Gross margin (i) | 54 | % | 43 | % | N/A | 11 | pp | 48 | % | 43 | % | N/A | 5 | pp
Inventory step-up recorded to cost of sales | — | — | — | N/A | — | 517 | (517) | N/A
Adjusted Gross Profit (ii) | 28,451 | 14,504 | 13,947 | 96 | % | 47,604 | 28,755 | 18,849 | 66 | %
Adjusted Gross Margin (iii) | 54 | % | 43 | % | N/A | 11 | pp | 48 | % | 44 | % | N/A | 4 | pp
Net income (loss) | 35,663 | (38,482) | 74,145 | N/M | 51,374 | (30,759) | 82,133 | N/M
Adjusted EBITDA (ii) | 13,088 | 1,688 | 11,400 | 675 | % | 18,167 | 3,977 | 14,190 | 357 | %
Other Data
Cash and cash equivalents and interest-bearing deposits (iv) | 827,019 | 834,416 | (7,397) | (1) | %
Cash and cash equivalents (iv) | 467,019 | 794,416 | (327,397) | (41) | %
Short-term investments (iv) | 330,000 | 40,000 | 290,000 | 725 | %
Non-current interest-bearing deposits (iv) | 30,000 | — | 30,000 | N/A
Capital expenditures (v) | 1,782 | 3,838 | (2,056) | (54) | % | 3,753 | 19,194 | (15,441) | (80) | %

(i) Gross margin is defined as gross profit divided by net revenue.

(ii) See " Non-GAAP Measures " for more information, including a reconciliation of adjusted earnings (loss) before interest, taxes, depreciation and amortization ( " Adjusted EBITDA " ) to net income (loss) and a reconciliation of Adjusted Gross Profit to gross profit.

(iii) Adjusted Gross Margin is defined as Adjusted Gross Profit divided by net revenue. See Non-GAAP Measures for more information.

(iv) Dollar amounts are as of the last day of the period indicated.

(v) Capital expenditures represent component information of investing activities and is defined as the sum of purchase of property, plant and equipment, and purchase of intangible assets.

Second Quarter 2026

• Net revenue of $53.0 million in Q2 2026 increased by $19.6 million from Q2 2025. The increase was primarily due to higher cannabis flower sales in Israel and other countries, specifically Germany, which carry no excise taxes, and higher cannabis flower and extract sales in the Canadian market. In addition, net revenue for the current period benefited from the strengthening of the New Israeli Shekel versus the U.S. dollar.

• Gross profit of $28.5 million in Q2 2026 increased by $13.9 million from Q2 2025. The increase was primarily due to higher average sales prices, largely driven by a mix shift to Israel and other countries, which carry no excise taxes, and higher sales volumes. Higher sales volumes led to higher net revenue and efficiencies as fixed overhead costs were spread over greater volumes.

• Net income was $35.7 million in Q2 2026, compared to a net loss of $38.5 million in Q2 2025. The improvement was primarily due to higher gross profit and other income, largely driven by foreign currency transaction gains, partially offset by higher operating expenses.

• Adjusted EBITDA of $13.1 million in Q2 2026 improved by $11.4 million from Q2 2025. The improvement was primarily driven by higher gross profit, partially offset by higher operating expenses due to higher sales and marketing, general and administrative, and research and development ("R&D") costs.

Business Updates

Brand and Product Portfolio

Spinach ® 3

The Spinach ® brand remained Canada's #2 overall cannabis brand in Q2 2026, with national market share expanding to 5.9%.

In edibles, Spinach ® remained the #1 brand in Canada, with market share consistent at 20.8%. In Q2 2026, five SOURZ by Spinach ® gummies products ranked among the top 10 edibles nationally, including the top-selling edibles SKU in Canada, the Fully Blasted Blue Raspberry Watermelon 10 Pack.

In July, Cronos expanded the SOURZ by Spinach ® product lineup to include varieties of the brand's popular flavors featuring rare cannabinoid formulations with CBG, CBN and CBC alongside THC, and also introduced the first limited-time offering within the Fully Blasted multipack format, the SOURZ by Spinach ® Fully Blasted Orange Cream gummies, available for the summer season.

Spinach ® remained the #1 vape brand in Canada for the second consecutive quarter, with total vape market share across all formats expanding to 10.6%. Within vape cartridges specifically, Spinach ® remained #1 for the third consecutive quarter, with market share expanding to 11.8%. In disposable vapes, Spinach ® ranked #2 for the full quarter, with 8.2% market share. Notably, during the quarter, the five best-selling vape SKUs nationwide across all formats were Spinach ® vape products.

In Q2 2026, Cronos launched three new PUFFERZ™ flavors in Canada, Strawberry Burst, Peach Iced Tea, and Grape Gas, expanding the brand's all-in-one vape portfolio. During the quarter, Cronos also introduced the Spinach ® Orange Vanilla Twist 1g vape cartridge, the brand's first limited-time offering vape, for the summer season.

In flower, Spinach ® remained #3 in Canada, with market share expanding to 5.4%. During the quarter, two Spinach ® flower strains, GMO Cookies and OG Kush, ranked among the top-six-selling flower products nationally.

In pre-rolls, Spinach ® rose to #7 in Canada, with market share rising to 3.1%. In Q2 2026, distribution broadened across Canadian provinces for Spinach STIX ® , the brand's first cylindrical-style pre-roll. In the second quarter, Spinach ® rose to #6 in infused pre-rolls, with market share increasing to 3.5%, and reached #6 in traditional pre-rolls, with market share increasing to 2.9%.

PEACE NATURALS ®4

Cronos Israel delivered its tenth consecutive quarter of record net revenue in Q2 2026, with net revenue growing 60% year-over-year (32% growth on a constant-currency basis), as the PEACE NATURALS ® brand continued to expand its lead in the Israeli medical cannabis market.

Cronos continued to expand its international presence in Q2 2026, with the Company's international business ex-Israel delivering record net revenue, increasing 88% year-over-year, led by strong demand for the Company's flower products, particularly in Germany. The sustained leadership of PEACE NATURALS ® products reflects the strength of Cronos' advanced genetic breeding program and industry-leading cultivation capabilities.

3 Hifyre Retail Analytics - National Retail Dollar by Brand in Canada - Q2 2026.

4 Market share and ranking information from pharmacy data collected by Cronos - Q2 2026.

Transactions

The Company is prepared to close its pending acquisition of CanAdelaar B.V. upon receipt of regulatory clearance in the Netherlands and satisfaction or waiver of the remaining closing conditions. The Company expects the acquisition to close in the second half of 2026. We have not been informed of any specific issues with our regulatory clearance submission, and based on the information available to us, the timing appears to reflect the ordinary course of the Dutch regulatory review process for a transaction of this nature.

Anti-Dumping Matters in Israel: Update

In June 2026, the Trade Levies Commissioner of the Israel Ministry of Economy and Industry announced that it had opened a new investigation into alleged dumping of medical cannabis imports from Canada. This announcement followed the 2024 investigation by the Commissioner, which did not result in the imposition of an anti-dumping duty. On July 28, 2026, the Commissioner terminated the investigation on procedural grounds. The termination was not based on a substantive determination of the merits and did not preclude another complaint or a new investigation.

On July 30, 2026, a new complaint concerning imports of medical cannabis from Canada was filed on behalf of the Israeli domestic industry. On August 2, 2026, the Commissioner notified the Government of Canada that the new complaint contained sufficient prima facie evidence of dumping, material injury to the domestic industry and a causal link between the alleged dumping and injury. On August 5, 2026, the Commissioner notified the Company of the initiation of a new investigation. The Company disputes the allegations underlying these matters and cannot predict the timing or outcome of the new investigation or any related proceedings or whether any provisional or final anti-dumping duty or other import restriction will ultimately be imposed.

Conference Call

The Company will host a conference call and live audio webcast on Thursday, August 6, 2026, at 8:30 a.m. ET to discuss 2026 second quarter business results. An audio replay of the call will be archived on the Company's website for replay. Instructions for the live audio webcast are provided on the Company's website at https://ir.thecronosgroup.com/events-presentations.

About Cronos

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-26_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

Business Overview

Cronos is an innovative global cannabinoid company committed to building disruptive intellectual property by advancing cannabis research, technology and product development. With a passion to responsibly elevate the consumer experience, Cronos is building an iconic brand portfolio. Cronos' diverse international brand portfolio includes Spinach ® , PEACE NATURALS ® , LIT™ and Lord Jones ® .

Unless otherwise noted or the context indicates otherwise, references in this Annual Report to the "Company," "Cronos," "we," "us," and "our" refer to Cronos Group Inc., its direct and indirect wholly owned subsidiaries and, if applicable, its joint ventures and investments accounted for by the equity method; the term "cannabis" means the plant of any species or subspecies of genus Cannabis and any part of that plant, including all derivatives, extracts, cannabinoids, isomers, acids, salts, and salts of isomers; the term "U.S. hemp" has the meaning given to the term "hemp" in the U.S. Agricultural Improvement Act of 2018, including hemp-derived cannabidiol ("CBD").

Strategy

Cronos seeks to create value for shareholders by focusing on four core strategic priorities:

• growing a portfolio of iconic brands that responsibly elevate the consumer experience;

• developing a diversified global sales and distribution network;

• establishing an efficient global supply chain; and

• creating and monetizing disruptive intellectual property.

Recent Developments

CanAdelaar Acquisition

On December 9, 2025, we entered into a definitive share sale and purchase agreement to acquire all of the issued and outstanding shares of CanAdelaar B.V. ("CanAdelaar"), one of ten licensed cannabis producers in the Dutch Controlled Cannabis Supply Chain Experiment. Closing of the proposed acquisition is subject to certain closing conditions, including obtaining required regulatory clearances in the Netherlands, receipt of confirmations relating to CanAdelaar's licenses and Bibob review (a background check conducted by Dutch authorities), the accuracy of representations and warranties, and the absence of certain regulatory orders.

Cronos GrowCo Expansion

The expansion of the facility at Cronos Growing Company Inc. ("Cronos GrowCo") is complete and sales from the expansion commenced in Fall 2025. Under the terms of our amended and restated supply agreement with Cronos GrowCo (the "Cronos GrowCo Supply Agreement"), Cronos has the option to purchase up to 70% of the total production from the expanded facility. Cronos GrowCo sells the remaining portion of its supply through the wholesale channel in Canada and across markets internationally. The Company believes this additional supply will fuel growth internationally and within the domestic Canadian market and the wholesale market in

2026. As with any cultivation expansion, it typically takes time to fully optimize the new facility.

U.S. Federal Cannabis Rescheduling

In December 2025, President Trump issued an executive order (the "Executive Order") directing the U.S. Attorney General to expedite the completion of the administrative process to reschedule marijuana from Schedule I to Schedule III under the U.S. Controlled Substances Act (the "CSA"). The Executive Order followed the U.S. Department of Health and Human Services' August 2023 recommendation to reschedule marijuana and the DEA's May 2024 notice of proposed rulemaking agreeing with that recommendation. Prior to the Executive Order, the rescheduling process had experienced procedural delays, including a hearing before a DEA administrative law judge and subsequent developments that slowed progress on the rulemaking.

The Executive Order does not itself change the legal status of marijuana under U.S. federal law. Any rescheduling would require the completion of the DEA's administrative rulemaking process and could be subject to further procedural steps and legal challenges.

The Company continues to monitor developments related to U.S. federal cannabis policy, including the DEA's rulemaking process and related legislative and regulatory activity, and will evaluate any potential implications for its business as additional information becomes available.

Sale of Cronos Fermentation Facility

In September 2025, we entered into a purchase and sale agreement to sell our fermentation and manufacturing facility in Winnipeg, Manitoba (the "Cronos Fermentation Facility") for a purchase price of CAD $4.0 million, subject to customary adjustments. The sale, which closed on November 15, 2025, included the land, buildings and related chattels associated with the facility.

Termination of Ginkgo Collaboration Agreement

On December 15, 2025, Cronos and Ginkgo Bioworks Holdings, Inc. ("Ginkgo") mutually terminated their collaboration and license agreement (the "Ginkgo Collaboration Agreement"). As a result of the termination, all rights and licenses granted to Cronos under the Ginkgo Collaboration Agreement, including licenses to Ginkgo intellectual property and collaboration strains, terminated as of that date, and neither party has any continuing obligations thereunder.

Ginkgo paid Cronos nominal consideration for the termination of the licenses to the Ginkgo intellectual property and the collaboration strains. No payments or equity issuances were required by Cronos in connection with the termination, and Cronos has no further rights or obligations with respect to any patent families previously associated with the collaboration. In connection with the termination, Cronos exited fermentation-based cannabinoid manufacturing and no longer operates facilities leveraging intellectual property under the Ginkgo Collaboration Agreement.

Spinach ®

A key addition to our gummy portfolio in 2025 was 10mg THC Fully Blasted SOURZ by Spinach® gummies featuring rare cannabinoids, including Mango Lime with CBC, Peach Passionfruit with CBN and CBD and Strawberry Watermelon with CBG.

In the fourth quarter of 2025, SOURZ by Spinach® Fully Blasted gummies launched in new multipack formats. The SOURZ by Spinach® Fully Blasted Multipacks with liquid diamond-infused gummies are now available in five popular flavors.

In the first quarter of 2025, the brand introduced two new Spinach® 1g vapes, Cherry Crush and Cocoa Mintz, alongside new 1.2g cartridges, Mango Kiwi Haze CBC, Peach Passionfruit Kush CBN and Strawberry Watermelon OG CBG. These additions extend our popular SOURZ by Spinach® flavor profiles into the vape category.

In the third quarter of 2025, the brand launched the limited-edition Spinach® Sweet Green Apple 1g vape, to complement its corresponding SOURZ by Spinach® Carmel Green Apple seasonal offering.

PEACE NATURALS ®

In 2025, new launches for the PEACE NATURALS® brand included strain‑specific oils and limited‑edition premium flower series, further strengthening the brand's portfolio and patient appeal. In the third quarter of 2025, Cronos Israel introduced new PEACE NATURALS® strains ANML, OGC, and Do Si Do under a new premium limited-edition product series, and launched a limited-edition combo pack featuring Wedding CK and Blue Thai.

Internationally, PEACE NATURALS® expanded its global footprint significantly. In the second quarter of 2025, the brand entered the medical cannabis markets in Australia and Malta, followed by launching in Switzerland in the third quarter. By mid‑2025, the brand's medical presence spanned seven key markets: Canada, Israel, Germany, the United Kingdom (the "UK"), Australia, Switzerland, and Malta.

LIT™

The LIT™ brand continued to gain momentum by launching in the German and UK medical markets in 2025. The goal of this value-driven brand is to capitalize on market trends, combining local insights with product development to build loyalty in emerging medical markets. Germany and the UK's growth environments helped LIT™ gain visibility and traction as demand for affordable, high‑quality flower products increased across clinics and distributors.

Lord Jones ®

In the first quarter of 2025, the brand launched a Lord Jones ® Chocolate Fusions™ fudge brownie bite in Canada, which features a 1:1:1 ratio of CBN, CBD and THC.

The brand also expanded its presence in concentrates in Canada with the introduction of Lord Jones® Live Resin Caviar in the second quarter of 2025, reinforcing its positioning as a high‑quality, innovation‑driven brand.

2024 Compared to 2023

Results of Operations and Cash Flows

For a discussion of our 2024 results of operations and cash flows compared to 2023, see Part II, Item 7 "Management's Discussion and Analysis of Financial Condition and Results of Operations," in our Annual Report on Form 10-K for the year ended December 31, 2024.

Foreign currency exchange rates

All currency amounts in this Annual Report are stated in U.S. dollars, which is our reporting currency, unless otherwise noted. All references to "dollars" or "$" are to U.S. dollars. The assets and liabilities of our foreign operations are translated into dollars at the exchange rate in effect as of December 31, 2025 and December 31, 2024, as reported on Bloomberg. Transactions affecting the shareholders' equity (deficit) are translated at historical foreign exchange rates. The consolidated statements of net income (loss) and comprehensive income (loss) and consolidated statements of cash flows of our foreign operations are translated into dollars by applying the average foreign exchange rate in effect for the years ended December 31, 2025, December 31, 2024, and December 31, 2023, as reported on Bloomberg.

The exchange rates used to translate from Canadian dollars ("C$") to dollars are shown below:

(Exchange rates are shown as C$ per $) | Year ended December 31,
2025 | 2024 | 2023
Average rate | 1.3975 | 1.3700 | 1.3494
Spot rate | 1.3698 | 1.4351 | 1.3243

The exchange rates used to translate from New Israeli Shekels ("ILS") to dollars are shown below:

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-26_item1_business.md)

ITEM 1. BUSINESS

General

Cronos is incorporated under the laws of the Province of British Columbia with principal executive offices located at 4491 Concession Rd 12, Stayner, Ontario L0M 1S0. The Company's telephone number is +1-416-504-0004, the website is https://thecronosgroup.com/ and the investor relations section of the website is https://ir.thecronosgroup.com/. All references to Cronos' website are inactive references, are for informational purposes only and are not intended to incorporate any information from or referenced on its website into this Annual Report.

Cronos common shares are currently listed on the Toronto Stock Exchange ("TSX") and on the NASDAQ Global Market ("Nasdaq") under the trading symbol "CRON."

Description of the Business

Overview

Cronos is an innovative global cannabinoid company committed to building disruptive intellectual property by advancing cannabis research, technology and product development. With a passion to responsibly elevate the consumer experience, Cronos is building an iconic brand portfolio. Cronos' diverse international brand portfolio includes Spinach ® , PEACE NATURALS ® , LIT™, and Lord Jones ® .

Strategy

Cronos seeks to create value for shareholders by focusing on four core strategic priorities:

• growing a portfolio of iconic brands that responsibly elevate the consumer experience;

• developing a diversified global sales and distribution network;

• establishing an efficient global supply chain; and

• creating and monetizing disruptive intellectual property.

Business Segment

Cronos reports through one consolidated segment, which includes operations in both Canada and Israel. In Canada, Cronos operates one wholly owned license holder under the Cannabis Act (Canada) (the "Cannabis Act"), Peace Naturals Project Inc. ("Peace Naturals"), which has production facilities in Stayner, Ontario (the "Peace Naturals Campus"). Cronos also consolidates the results of operations of Cronos GrowCo in its consolidated financial statements and maintains a 50% equity interest in Cronos GrowCo. Cronos GrowCo's production facilities are licensed under the Cannabis Act and represent the Company's principal source of cannabis.

In Israel, Cronos operates under the Good Agricultural Practices ("IMC-GAP"), Good Manufacturing Practices ("IMC-GMP") and Good Distribution Practices ("IMC-GDP") certifications required for the cultivation, production, distribution and marketing of medical cannabis products in Israel.

Operations and Investments

Peace Naturals Campus & Cronos GrowCo

The production facilities at the Peace Naturals Campus and the production facilities of Cronos GrowCo are licensed by Health Canada under the Cannabis Act to engage in the cultivation, processing, distribution and sale of dried flower, cannabis seeds, cannabis plants, cannabis extracts, cannabis topicals and cannabis edibles, among other prescribed activities.

Israel

In Israel, the Company operates under the IMC-GAP, IMC-GMP and IMC-GDP certifications required for the cultivation, production, distribution and marketing of medical cannabis products in Israel.

Operations Outside of Canada and Israel

Cronos distributes PEACE NATURALS ® and LIT™ branded products and white-labeled cannabis products to select international markets.

Cronos anticipates that it will continue entering new markets and expanding in its current geographic markets. By leveraging operational, manufacturing and regulatory expertise, quality standards and procedures and intellectual property, the Company is well-positioned to effectively expand in its existing markets and access new markets. Subject to applicable regulatory approvals, strategic international business opportunities pursued by Cronos could include:

• production, distribution, sales and marketing in jurisdictions that have passed legislation to legalize the production, distribution and possession of cannabis products at all relevant levels of government; and

• the export of cannabis products to markets that permit the import of such products.

Cronos seeks to conduct business only in jurisdictions where Cronos has determined it is legal to do so and where such operations remain compliant with its TSX and Nasdaq listing obligations. Determining whether a business activity is legal in a jurisdiction may require judgment since laws, rules, regulations and licenses may not be clear and legal interpretation and advice of counsel may vary. If a business activity in which Cronos engages in any jurisdiction is determined to be illegal, the Company could be subject to fines, penalties, reputational harm, delisting from securities exchanges and material civil, criminal and regulatory litigation and proceedings or be enjoined from doing business in the applicable jurisdiction. See " Risk Factors—Risks Relating to Regulation and Compliance—We operate in highly regulated sectors where the regulatory environment is rapidly developing, and we may not always succeed in complying fully with applicable regulatory requirements in all jurisdictions where we carry on business. "

Joint Ventures/Strategic Investments

Cronos has established two strategic joint ventures in Canada and Israel. Additionally, the Company held approximately 8.3% of the issued capital of Vitura following the issuance by Vitura of an additional 74,814,757 shares on February 12, 2025, which is accounted for as equity securities with a readily determinable fair value, and approximately 13.7% of the issued capital of NatuEra S.à.r.l. ("Natuera"), which is accounted for as equity securities without a readily determinable fair value, as of December 31, 2025.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-26_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-26_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-26_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-02-26_item7_mdna.md, 10-K_2026-02-26_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
