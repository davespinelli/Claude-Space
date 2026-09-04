# Triage pack — CPRI · Capri Holdings Ltd

_Generated 2026-09-04 22:10 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** CPRI · **Name:** Capri Holdings Ltd
- **CIK:** 0001530721
- **SIC:** 3100 — Leather & Leather Products
- **Fiscal year end (MM-DD):** 03-29
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/CPRI

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Capri Holdings Ltd
- **CIK:** 1,530,721 · **SIC:** 3100 (Leather & Leather Products) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

> **EARNINGS QUALITY FLAG — one-off items likely.**
> net income more than 3x operating income.
> Reported net income is not supported by the operating engine that is supposed to produce it (typical causes: gains on sale, legal settlements, deferred-tax valuation-allowance releases, bargain-purchase gains). Reconcile net income to operating income in the earnings release (section 7) before treating any earnings-based metric here as repeatable.

**Valuation**

| metric | value |
|---|---|
| price | 13.24 |
| mktcap | $1.5B |
| ev | $1.7B |
| ev_ebit | 74.6x |
| fcf | $14.0M |
| fcf_yield | 0.9% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 5.2% |
| net_debt | $210.0M |
| net_debt_ebit | 9.1x |
| cash | $114.0M |
| ltd | $324.0M |
| equity | $138.0M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $3.5B |
| revenue_prior | $3.6B |
| rev_growth | -4.1% |
| rev_growth_note | n/a |
| eq_flag | net income more than 3x operating income |
| ebit | $23.0M |
| net_income | $79.0M |
| cfo | $77.0M |
| capex | $63.0M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -4.5% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 113,651,618 |
| shares_py | 119,048,057 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -24.1% |
| r6m | -29.2% |
| off_52w_high | -52.1% |
| adv20 | $61.1M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.25 |
| r_ev_ebit | 0.09 |
| r_roic | 0.52 |
| r_rev_growth | 0.21 |
| r_buyback | 0.87 |
| score | 0.39 |

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
| rank | 333 |

**Screen rationale:** buying back stock -4.5%; EARNINGS QUALITY: net income more than 3x operating income — one-off items likely


## 3. Share count trend

- Shares outstanding: **113,651,618** (CY2026Q2I) vs **119,048,057** prior year (CY2025Q2I)
- Change: **-4.5%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-06-25** — Item 1.01 (ENTRY INTO A MATERIAL DEFINITIVE AGREEMENT): Date"), Capri Holdings Limited (the "Company") entered into Amendment No. 1 (the "Amendment") to its existing
- **2026-06-16** — Item 5.02 (officer / director change or comp arrangement): (b) On June 11, 2026, Stephen Reitman expressed his intention to not stand for re-election to the Board of Directors of Capri Holdings Limited (the "Company") at the 2026 Annual Meeting of Shareholders (the "2026 Annual Meeting") of the Company, and his term...
- **2026-04-09** — Item 5.02 (officer / director change or comp arrangement): On April 6, 2026, Krista McDonough, Chief Legal and Sustainability Officer of Capri Holdings Limited (the "Company"), notified the Company of her decision to voluntarily resign from her position in order to pursue another professional opportunity.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 17,981 sh / $349,166 -> net $-349,166 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 65 (open-market buys 0, sales 1).

| code | rows |
|---|---|
| A | 9 |
| F | 17 |
| M | 38 |
| S | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-05_2-02-results.md)

_Extraction: started at the first release heading, 'First Quarter Fiscal 2027 Highlights from Continuing Operations'; skipped 8 forward-looking-statement block(s); 7 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (cpri8-k6272026exhibit991.htm)

First Quarter Fiscal 2027 Highlights from Continuing Operations

• Revenue decreased 3.5% on a reported basis and 4.1% in constant currency

• Operating margin was 2.2%; adjusted operating margin was 3.6%

• Earnings per share were $0.60 ; adjusted earnings per share were $0.67

John D. Idol, the Company's Chairman and Chief Executive Officer, said, "We are encouraged by our first quarter results, which exceeded our expectations and demonstrated the progress we are making to build a stronger and more profitable business. Our strategic initiatives across both Michael Kors and Jimmy Choo are driving deeper consumer engagement through enhanced brand storytelling and compelling product innovation."

Mr. Idol continued, "As we look at the balance of fiscal 2027 we expect Jimmy Choo to continue to grow and return to profitability. At Michael Kors certain headwinds including lower than anticipated inventory levels in the second quarter, softer trends in EMEA and updated foreign currency exchange rate assumptions are impacting our revenue outlook. As a result we now expect fiscal 2027 revenue of approximately $3.4 billion. Based on our revised revenue expectations we are taking actions to reduce operating expenses which are enabling us to maintain our fiscal 2027 earnings per share outlook of approximately $2.15, representing 40% growth over the prior year."

Mr. Idol concluded, "Looking beyond fiscal 2027 the opportunity for Michael Kors and Jimmy Choo remains significant. As our strategic initiatives continue to gain momentum, Capri Holdings is well positioned to drive sustainable growth, enhance profitability and create meaningful long-term value for our shareholders."

First Quarter Fiscal 2027 Results

Financial Results and Non-GAAP Reconciliation

The Com pany's results are reported in this press release in accordance with accounting principles generally accepted in the United States ("U.S. GAAP") and on an adjusted, non-GAAP basis. A reconciliation of GAAP to non-GAAP financial information is provided at the end of this press release.

As previously disclosed, on April 10, 2025, the Company and Prada S.p.A. ("Prada") entered into a Stock Purchase Agreement (the "Purchase Agreement") whereby Prada agreed to acquire certain subsidiaries of the Company which operate the Company's Versace business. As a result, the Company classified the results of operations and cash flows of its Versace business as discontinued operations in its consolidated financial statements for all periods presented. The related assets and liabilities associated with the discontinued operations were classified as held for sale in the consolidated balance sheets as of June 28, 2025. On December 2, 2025, the Company completed the sale of its Versace business. Unless otherwise noted, the discussion below, including analysis of financial condition and results of operations, relates only to continuing operations.

Overview of Capri Holdings First Quarter Fiscal 2027 Results

• Total revenue of $769 million decreased 3.5% compared to last year. On a constant currency basis, total revenue decreased 4.1%.

• Gross profit was $500 million and gross margin was 65.0%, compared to $502 million and 63.0% in the prior year. The 200 basis point increase in gross margin was primarily driven by higher full-price sell-throughs and lower tariff rates relative to the first quarter of fiscal 2026.

• Income from operations was $17 million and operating margin was 2.2%, compared to income from operations o f $16 million an d operating margin of 2.0% in the prior year. A djusted income from operations was $28 million a nd adjusted operating margin was 3.6%, compared to $20 million and 2.5% in the prior year.

• Net income was $69 million, or $0.60 pe r diluted share, compared to net income of $56 million , or $0.47 per diluted share, in the prior year. Adjusted net income was $76 million, or $0.67 per diluted share, compared to $60 million, or $0.50 per diluted share, in the prior year.

• Net inventory as of June 27, 2026 was $624 million, a 20% decrease compa red to the prior year.

• Cash flow provided by operating activities for the first quarter was $73 million, while capital expenditures were $25 million, resulting in free cash flow of $48 million.

• Cash and cash equivalents totaled $114 million, and total borrowings outstanding w ere $338 million, resulting in net debt of $224 million as of June 27, 2026 v ersu s $1.5 billion as of June 28, 2025 .

Michael Kors First Quarter Fiscal 2027 Results

• Michael Kors revenue of $590 million decreased 7.1% compared to last year. On a constant currency basis, Michael Kors revenue decline d 7.6%. Approximately $10 million of revenue was attributable to earlier than anticipated timing of wholesale shipments.

• Michael Kors gross profit was $377 million and gross margin was 63.9%, compared to $388 million and 61.1% in the prior year. The 280 basis point increase in gross margin was primarily driven by higher full-price sell-throughs and lower tariff rates relative to the first quarter of fiscal 2026.

• Michael Kors operati ng income was $55 million and operating margin was 9.3%, co mpared to $63 million and 9.9% in the prior year. The 60 basis point decline in operating margin was primarily due to expense deleverage on lower revenue.

Jimmy Choo First Quarter Fiscal 2027 Results

• Jimmy Choo reven ue of $179 million increased 10.5% compared to last year. On a constant currency basis, Jimmy Choo revenue increased 9.3%.

• Jimmy Choo gross profit was $123 million and gross margin was 68.7%, compared to $114 million and 70.4% in the prior year. The 170 basis point decrease in gross margin was primarily driven by channel mix.

• Jimmy Choo ope rating income was $13 million and operating margin was 7.3%, co mpared to operating income of $4 million and operating margin of 2.5% in the pri or year. The 480 basis point increase in operating margin was primarily due to expense leverage on higher revenue.

Share Repurchase Program

During the fiscal first quarter, the Company spent $50 million to repurchase approximately 2.6 million ordinary shares in open market transactions at an average cost of approximately $19.31 per share. As of June 27, 2026 the remaining availability under the Company's share repurchase program was $871 million.

Outlook

The following guidance is provided on an adjusted, non-GAAP basis. Guidance assumes an incremental 10% tariff rate on imports into the United States through July 24, 2026 and 10% to 12.5% thereafter. F inancial results could differ materially from the current outlook due to a number of external events which are not reflected in our guidance, including changes in global macroeconomic conditions, incremental tariff rates in excess of our assumptions, greater than anticipated inflationary pressures or weakening consumer confidence, and further considerable fluctuations in foreign currency exchange rates.

Fiscal Year 2027 Outlook

For Capri Holdings, the Company now expects the following:

• Total revenue of approximately $3.4 billion impacted by approximately $50 million from lower than anticipated second quarter revenue at Michael Kors due to inventory delays, $50 million from softer trends in EMEA due to the ongoing conflict in the Middle East and $35 million from foreign currency headwinds relative to our prior expectation.

• Operating income of approximately $170 million

• Net interest and other income of approximately $100 million

• Effective tax rate in the low-teens range

• Weighted average diluted shares outstanding of approximately 110 million

• Diluted earnings per share of approximately $2.15

For Michael Kors, the Company expects the following:

• Total revenue of approximately $2.765 billion

• Operating margin in the low-double-digit range

For Jimmy Choo, the Company expects the following:

• Total revenue of approximately $635 million

• Operating margin in the low-single-digit range

Second Quarter Fiscal 2027 Outlook

For Capri Holdings, the Company expects the following:

• Total revenue of approximately $780 million impacted by approximately $50 million associated with inventory delays at Michael Kors, $15 million from softer than previously anticipated trends in EMEA, $10 million from foreign currency headwinds and $10 million related to the timing shift of wholesale shipments that benefited the first quarter.

• Operating income of approximately $10 million

• Net interest and other income of approximately $25 million

• Effective tax rate in the mid-30% range

• Weighted average diluted shares outstanding of approximately 112 million

• Diluted earnings per share of approximately $0.20

For Michael Kors, the Company expects the following:

• Total revenue of approximately $645 million

• Operating margin in the high-single-digit range

For Jimmy Choo, the Company expects the following:

• Total revenue of approximately $135 million

• Operating margin in the negative mid-single-digit range

The Company is unable to provide a reconciliation of the non-GAAP financial outlook to the corresponding GAAP measures presented in this press release and on the Company's conference call without unreasonable effort due to the challenge in quantifying v arious significant items, including, but not limited to, foreign currency fluctuations, taxes, increased tariffs, and any future restructuring and other charges and expenses.

Conference Call Information

A conference call to discuss first quarter fiscal 2027 results is scheduled for today, August 5, 2026 at 8:30 a.m. ET. A live webcast of the conference call will be available on the Company's website, www.capriholdings.com. In addition, a replay will be available shortly after the conclusion of the call and remain available until August 12, 2026. To access the telephone replay, listeners should dial 1 (844) 512-2921 or 1 (412) 317-6671 for international callers. The access code for the replay is 13758328. A replay of the webcast will also be available within two hours of the conclusion of the call.

Use of Non-GAAP Financial Measures

Constant currency effects are non-GAAP financial measures, which are provided to supplement our reported operating results to facilitate comparisons of our operating results and trends in our business, excluding the effects of foreign currency rate fluctuations. Because we are a global company, foreign currency exchange rates may have a significant effect on our reported results. The Company believes presenting metrics on a constant currency basis will help investors to understand the effect of significant year-over-year foreign currency exchange rate fluctuations and provide a framework to assess how the business is performing and expected to perform excluding these effects. We calculate constant currency measures and the related foreign currency impacts by translating the current year's reported amounts into comparable amounts using prior year's foreign exchange rates for each currency. All constant currency performance measures discussed in this press release should be considered a supplement to and not in lieu of our operating performance measures calculated in accordance with U.S. GAAP. The Company also presents free cash flow, which is a non-GAAP measure and is calculated by taking net cash provided by operating activities less capital expenditures for the period. The Company believes that free cash flow is an important liquidity measure of cash that is available after giving effect to our capital and strategic plans, and that it is useful to investors because it measures the Company's ability to generate cash. Additionally, this earnings release includes

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-05-27_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

Our Business

Capri Holdings Limited is a global fashion luxury group consisting of iconic brands Michael Kors and Jimmy Choo. Our commitment to glamorous style and craftsmanship is at the heart of each of our luxury brands. We have built our reputation on designing exceptional, innovative products that cover the full spectrum of fashion luxury categories. Our strength lies in the unique DNA and heritage of each of our brands, the diversity and passion of our people and our dedication to the clients and communities we serve.

Our Michael Kors brand was launched in 1981 by Michael Kors, a world-renowned designer, whose vision has taken the Company from its beginnings as an American luxury sportswear house to a global accessories, footwear and apparel company with a global distribution network that has presence in over 100 countries through Company-operated retail stores and e-commerce sites, leading department stores, specialty stores and select licensing partners. Michael Kors is a highly recognized fashion luxury brand in the Americas and Europe with strong brand awareness in other international markets. Michael Kors features distinctive designs, materials and craftsmanship with a Jet Set aesthetic that combines stylish elegance and a sporty attitude. Michael Kors offers three primary collections: the Michael Kors Collection line, the MICHAEL Michael Kors line and the Michael Kors Mens line. Michael Kors Collection establishes the aesthetic authority of the entire brand and is carried by select retail stores, our e-commerce sites, as well as in the finest luxury department stores in the world. MICHAEL Michael Kors has a strong focus on accessories, in addition to offering footwear and apparel. We have also been developing our men's business in recognition of the significant opportunity afforded by the Michael Kors brand's established fashion authority and the expanding men's market. Taken together, our Michael Kors collections target a broad customer base while retaining our premium luxury image.

Our Jimmy Choo brand offers a distinctive, glamorous and fashion-forward product range that since its inception in 1996 has been anchored by women's luxury footwear, complemented by accessories, including handbags, small leather goods, jewelry, scarves and belts, as well as men's luxury footwear and accessories. In addition, certain categories, including fragrance and eyewear, are produced under licensing agreements. Jimmy Choo's design team is led by Sandra Choi, who has been the Creative Director for the brand since its inception in 1996. Jimmy Choo products are unique, instinctively seductive and chic. The brand offers classic and timeless luxury products, alongside innovative collections that are intended to set and lead fashion trends. Jimmy Choo is represented through its global store network, its e-commerce sites, as well as through the most prestigious department and specialty stores worldwide.

On April 8, 2025, our Board of Directors made the decision to sell Versace to Prada, and a definitive agreement was entered into on April 10, 2025. Accordingly, we determined that the held for sale and discontinued operations criteria were met and we classified the results of operations and cash flows of our Versace business as discontinued operations in our consolidated statements of operations and comprehensive income (loss) and consolidated statements of cash flows for all periods presented. On December 2, 2025, we completed the sale of our Versace business. The related assets and liabilities associated with the discontinued operations are classified as held for sale in the consolidated balance sheet as of March 29, 2025. Unless otherwise noted, management's discussion and analysis of financial condition and results of operations only relates to our continuing operations. Refer to Note 4 - "Discontinued Operations" to the accompanying consolidated financial statements for additional information.

Termination of the Agreement and Plan of Merger with Tapestry

As previously disclosed, on August 10, 2023, Capri entered into an Agreement and Plan of Merger (the "Merger Agreement") with Tapestry, a Maryland corporation, and Sunrise Merger Sub, Inc., a British Virgin Islands business company limited by shares and a direct wholly owned subsidiary of Tapestry. The Merger Agreement provided that, among other things and on the terms and subject to the conditions set forth therein, Tapestry would acquire Capri in an all-cash transaction by means of a merger of Merger Sub with and into Capri, with Capri surviving the Merger as a wholly owned subsidiary of Tapestry.

The Merger had been approved by the boards of directors of Capri and Tapestry and by the shareholders of Capri. Completion of the Merger was subject to, among other customary conditions, the expiration or termination of the applicable waiting period under the Hart-Scott-Rodino Antitrust Improvements Act of 1976, as amended. The Company received

Table of Content s

regulatory approval from all countries except for the United States. In connection with Tapestry's proposed acquisition of Capri, on April 22, 2024, the U.S. FTC filed a lawsuit in the United States District Court for the Southern District of New York (the "District Court") against Tapestry and the Company seeking to block the Merger, claiming that the Merger would violate Section 7 of the Clayton Act and that the Merger Agreement and the Merger constituted unfair methods of competition in violation of Section 5 of the Federal Trade Commission Act and should be enjoined. The preliminary injunction hearing concluded in September 2024, and on October 24, 2024, the District Court granted the FTC's motion for a preliminary injunction to enjoin the Merger pending the completion of the FTC's in-house administrative proceeding. On October 28, 2024, Tapestry and Capri jointly filed a notice of appeal to the U.S. Court of Appeals for the Second Circuit (the "Second Circuit").

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

A discussion regarding our results of operations for Fiscal 2026 compared to Fiscal 2025 is presented below. Since we have classified our results of operations of the Versace business as discontinued operations for all periods presented, we are also providing comparisons between Fiscal 2025 and Fiscal 2024. Refer to Note 4 - "Discontinued Operations" to the accompanying consolidated financial statements for additional information.

Comparison of Fiscal 2026 with Fiscal 2025

The following table details the results of our operations for Fiscal 2026 and Fiscal 2025 and expresses the relationship of certain line items to total revenue as a percentage (dollars in millions):

Fiscal Years Ended | $ Change | % Change | % of Total Revenue for Fiscal Year Ended
March 28, 2026 | March 29, 2025 | March 28, 2026 | March 29, 2025
Statements of Operations Data:
Total revenue | 3,474 | 3,621 | (147) | (4.1) | %
Cost of goods sold | 1,311 | 1,370 | (59) | (4.3) | % | 37.7 | % | 37.8 | %
Gross profit | 2,163 | 2,251 | (88) | (3.9) | % | 62.3 | % | 62.2 | %
Selling, general and administrative expenses | 1,964 | 1,998 | (34) | (1.7) | % | 56.5 | % | 55.2 | %
Depreciation and amortization | 121 | 132 | (11) | (8.3) | % | 3.5 | % | 3.6 | %
Impairment of assets | 40 | 142 | (102) | (71.8) | % | 1.2 | % | 3.9 | %
Restructuring and other expense | 15 | 5 | 10 | NM | 0.4 | % | 0.1 | %
Total operating expenses | 2,140 | 2,277 | (137) | (6.0) | % | 61.6 | % | 62.9 | %
Income (loss) from continuing operations | 23 | (26) | 49 | NM | 0.7 | % | (0.7) | %
Other (income) expense, net | (5) | 8 | (13) | NM | (0.1) | % | 0.2 | %
Interest income, net | (77) | (37) | (40) | NM | (2.2) | % | (1.0) | %
Foreign currency (gain) loss | (2) | 5 | (7) | NM | (0.1) | % | 0.1 | %
Income (loss) from continuing operations before income taxes | 107 | (2) | 109 | NM | 3.1 | % | (0.1) | %
Provision for income taxes | 27 | 524 | (497) | (94.8) | % | 0.8 | % | 14.5 | %
Net income (loss) from continuing operations | 80 | (526) | 606 | NM
Net income (loss) from discontinued operations, net of tax | 58 | (653) | 711 | NM
Net income (loss) | 138 | (1,179) | 1,317 | NM
Less: Net income attributable to noncontrolling interest from continuing operations | 1 | 3 | (2) | (66.7) | %
Net income (loss) attributable to Capri | 137 | (1,182) | 1,319 | NM

NM Not meaningful

Total Revenue

Fiscal Years Ended | % Change
(dollars in millions) | March 28, 2026 | March 29, 2025 | $ Change | As Reported | Constant Currency
Michael Kors | 2,874 | 3,016 | (142) | (4.7) | % | (6.5) | %
Jimmy Choo | 600 | 605 | (5) | (0.8) | % | (4.3) | %
Total revenue | 3,474 | 3,621 | (147) | (4.1) | % | (6.2) | %

Total revenue decreased $147 million, or 4.1%, to $3.474 billion for Fiscal 2026, compared to $3.621 billion for Fiscal 2025, which included net favorable foreign currency effects of $76 million primarily as a result of the weakening of the United

Table of Content s

States dollar compared to the Euro and British Pound. On a constant currency basis, our total revenue decreased $223 million, or 6.2%.

• Michael Kors revenues decreased $142 million, or 4.7%, to $2.874 billion during Fiscal 2026, compared to $3.016 billion for Fiscal 2025, which included favorable foreign currency effects of $55 million. On a constant currency basis, revenue decreased $197 million, or 6.5%, primarily driven by our quality of sale initiatives, as we reduced promotional activity and reduced discounted third party sales and off-price shipments.

• Jimmy Choo revenues decreased $5 million, or 0.8%, to $600 million during Fiscal 2026, compared to $605 million for Fiscal 2025, which included favorable foreign currency effects of $21 million. On a constant currency basis, revenue decreased $26 million, or 4.3%, primarily attributable to a continued slowdown in demand for certain categories of fashion luxury goods.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-05-27_item1_business.md)

Item 1. Business

Our Company

Capri Holdings Limited ("Capri") is a global fashion luxury group consisting of iconic brands Michael Kors and Jimmy Choo. Our commitment to glamorous style and craftsmanship is at the heart of each of our luxury brands. We have built our reputation on designing exceptional, innovative products that cover the full spectrum of fashion luxury categories. Our strength lies in the unique DNA and heritage of each of our brands, the diversity and passion of our people and our dedication to the clients and communities we serve.

Our Brands

Michael Kors

Our Michael Kors brand was launched in 1981 by Michael Kors, a world-renowned designer, whose vision has taken the Company from its beginnings as an American luxury sportswear house to a global accessories, footwear and apparel company with a global distribution network that has presence in over 100 countries through Company-operated retail stores and e-commerce sites, leading department stores, specialty stores and select licensing partners. Michael Kors is a highly recognized fashion luxury brand in the Americas and Europe with strong brand awareness in other international markets. Michael Kors features distinctive designs, materials and craftsmanship with a Jet Set aesthetic that combines stylish elegance and a sporty attitude. Michael Kors offers three primary collections: the Michael Kors Collection line, the MICHAEL Michael Kors line and the Michael Kors Mens line. Michael Kors Collection establishes the aesthetic authority of the entire brand and is carried by select retail stores, our e-commerce sites, as well as in the finest luxury department stores in the world. MICHAEL Michael Kors has a strong focus on accessories, in addition to offering footwear and apparel. We have also been developing our men's business in recognition of the significant opportunity afforded by the Michael Kors brand's established fashion authority and the expanding men's market. Taken together, our Michael Kors collections target a broad customer base while retaining our premium luxury image.

Jimmy Choo

Our Jimmy Choo brand offers a distinctive, glamorous and fashion-forward product range that since its inception in 1996 has been anchored by women's luxury footwear, complemented by accessories, including handbags, small leather goods, jewelry, scarves and belts, as well as men's luxury footwear and accessories. In addition, certain categories, including fragrance and eyewear, are produced under licensing agreements. Jimmy Choo products are unique, instinctively seductive and chic. The brand offers classic and timeless luxury products, alongside innovative collections that are intended to set and lead fashion trends. Jimmy Choo is represented through its global store network, its e-commerce sites, as well as through the most prestigious department and specialty stores worldwide.

Table of Content s

Our Segments

We operate in two reportable segments as follows:

• Michael Kors — accounted for approximately 83% of our total revenue in Fiscal 2026 and includes worldwide sales of Michael Kors products through 673 retail stores (including concessions) and e-commerce sites, through wholesale doors, as well as through product and geographic licensing arrangements.

• Jimmy Choo — accounted for approximately 17% of our total revenue in Fiscal 2026 and includes worldwide sales of Jimmy Choo products through 211 retail stores (including concessions) and e-commerce sites, through wholesale doors, as well as through product and geographic licensing arrangements.

In addition to these reportable segments, we have certain corporate costs that are not directly attributable to our brands and, therefore, are not allocated to our segments. Such costs primarily include certain administrative, corporate occupancy, shared service and information technology systems expenses, including enterprise resource planning ("ERP") system implementation costs and Capri transformation program costs. In addition, certain other costs are not allocated to segments, including Tapestry related transaction income (expense), impairment charges and restructuring and other expense. The segment structure is consistent with how the Company's chief operating decision maker ("CODM") plans and allocates resources, manages the business and assesses performance. All intercompany revenues are eliminated in consolidation and are not reviewed when evaluating segment performance. For additional financial information regarding our segments and corporate unallocated expenses, refer to Note 21 - "Segment Information" to the accompanying consolidated financial statements.

Industry

We operate in the global personal luxury goods industry. Since 1996, the global personal luxury goods industry has increased at a mid-single-digit compound annual growth rate. Following several years of strong expansion, the industry has entered a period of recalibration amid persistent macroeconomic pressures, inflation-driven declines in purchasing power, and softer consumer confidence. In 2025, the personal luxury goods market is estimated to have declined modestly to approximately €358 billion. This represented the second consecutive year of market contraction and marked the first sustained decline in the global personal luxury goods customer base. Bain* estimates that approximately 80 million consumers exited the category over the last three years as discretionary demand softened. Over the long term, Bain forecasts the personal luxury goods market will grow at a 4% to 6% compound annual growth rate, reaching approximately €525 to €640 billion by 2035, driven by an expanding addressable consumer base, global wealth creation and increased participation from younger consumers.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-05-27_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-05-27_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-05-27_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-05_2-02-results.md, 10-K_2026-05-27_item7_mdna.md, 10-K_2026-05-27_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
