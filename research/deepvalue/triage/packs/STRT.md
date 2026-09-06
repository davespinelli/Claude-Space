# Triage pack — STRT · STRATTEC SECURITY CORP

_Generated 2026-09-06 11:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** STRT · **Name:** STRATTEC SECURITY CORP
- **CIK:** 0000933034
- **SIC:** 3714 — Motor Vehicle Parts & Accessories
- **Fiscal year end (MM-DD):** 06-28
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/STRT

**Fetcher warnings for this ticker:** 10-K 2026-08-28: heading split missed Item 1 - Business

## 2. Screen row (all metrics)

_Source: candidates.csv_

- **Name:** STRATTEC SECURITY CORP
- **CIK:** 933,034 · **SIC:** 3714 (Motor Vehicle Parts & Accessories) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermLineOfCredit

**Valuation**

| metric | value |
|---|---|
| price | 75.84 |
| mktcap | $302.2M |
| ev | $194.0M |
| ev_ebit | 7.3x |
| fcf | $39.0M |
| fcf_yield | 12.9% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 16.1% |
| net_debt | -$108.2M |
| net_debt_ebit | -4.1x |
| cash | $108.2M |
| ltd | $0.00 |
| equity | $238.6M |
| ltd_tag | LongTermLineOfCredit |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $579.4M |
| revenue_prior | $565.1M |
| rev_growth | 2.5% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $26.5M |
| net_income | $20.6M |
| cfo | $46.3M |
| capex | $7.3M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -4.2% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 3,985,013 |
| shares_py | 4,161,334 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 27.3% |
| r6m | -5.7% |
| off_52w_high | -16.6% |
| adv20 | $8.1M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.83 |
| r_ev_ebit | 0.90 |
| r_roic | 0.81 |
| r_rev_growth | 0.40 |
| r_buyback | 0.84 |
| score | 0.81 |

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

**Screen rationale:** top-quartile FCF yield 12.9%; cheap at 7.3x EV/EBIT; high ROIC 16.1%; buying back stock -4.2%; net cash; 12-1 momentum 27.3%


## 3. Share count trend

- Shares outstanding: **3,985,013** (CY2026Q2I) vs **4,161,334** prior year (CY2025Q2I)
- Change: **-4.2%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-04-30** — Item 1.02 (Termination of a Material Definitive Agreement): Effective as of April 30, 2026, ADAC-STRATTEC, LLC ("ADAC-STRATTEC"), a majority owned joint venture subsidiary of Strattec Security Corporation (the "Company"), entered into an Amended and Restated Credit Agreement with BMO Bank N.A. (the "New JV Credit...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 4,598 sh / $286,430 vs sells 0 sh / $0 -> net $286,430 (BUYING).
Distinct insiders buying (code P): 3. Largest buy: Pauli Matthew bought 2,000 sh @ $62.53 ($125,060) on 2026-05-12.

Form 4 filings parsed: 12; transaction rows: 17 (open-market buys 4, sales 0).

| code | rows |
|---|---|
| A | 8 |
| F | 5 |
| P | 4 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-25_2-02-results.md)

_Extraction: started at the first release heading, 'Fourth quarter fiscal 2026 sales of $151.8 million was better than exp'; skipped 12 forward-looking-statement block(s); 7 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (strt-ex99_1.htm)

Strattec Transformation Delivers Margin Improvement and Strong Cash Generation in Fiscal 2026

•
Fourth quarter fiscal 2026 sales of $151.8 million was better than expected and relatively unchanged from prior year; achieved sales of $579.4 million for fiscal year 2026

•
Reported fourth quarter gross margin of 15.6%; full year gross margin expanded to 16.5%, up from 15.0% in fiscal 2025

•
Generated fourth quarter net income attributable to Strattec of $3.9 million, or $0.95 per diluted share; adjusted diluted earnings per share were $2.06, unchanged from the prior-year period

•
Fourth quarter Adjusted EBITDA was $12.5 million, or 8.3% of net sales, compared with $13.0 million, or 8.5% of sales in the prior-year period; fiscal 2026 Adjusted EBITDA 1 was $50.5 million, a 15.3% increase over the prior year

•
$108.2 million in cash and no debt; returned $7.4 million to shareholders through share repurchases in the fourth quarter and authorized a new $40 million share buyback program

MILWAUKEE, WI , August 25, 2026 — Strattec (Nasdaq: STRT), a global provider of highly engineered access solutions for the automotive and mobility industries, today reported financial results for its fourth quarter and fiscal year 2026, which ended June 28, 2026.

Jennifer Slater, President and CEO of Strattec, said, "Fiscal 2026 was a year of progress and discipline as we continued to reshape Strattec into a more resilient, higher-performing business. While our fourth quarter and full-year results were impacted by foreign exchange pressure and the effect of tariffs, we nonetheless delivered year-over-year growth in sales and gross margin expansion through disciplined pricing, cost actions and operational improvements."

She added, "We recognize that the near-term environment remains uncertain and we have much work to do to secure future OEM vehicle platforms. We are managing costs and capital prudently, while our strong cash position gives us the flexibility to continue investing in our product technologies, production automation and customer relationships. These investments will better position us to benefit when industry conditions improve. The strength of our balance sheet also allows us to

1 Refer to use of "Non-GAAP Financial Metrics and Additional Financial Information" as well as accompanying reconciliations to GAAP

3333 WEST GOOD HOPE ROAD MILWAUKEE, WI 53209 | 414.247.3333 WWW.STRATTEC.COM | NASDAQ: STRT

Strattec Transformation Delivers Margin Improvement and Strong Cash Generation in Fiscal 2026

August 25, 2026

Page 2 of 10

consider opportunities that could enhance scale and diversify our customers, products and programs over time."

FY 2026 Fourth Quarter Financial Summary

Net sales were $151.8 million, relatively unchanged from $152.0 million in the prior-year period, and reflected better than expected OEM vehicle production volumes relative to industry forecasts. A majority of the volume decline, including $3.2 million related to customer cancelled EV programs, was offset by pricing actions.

Gross profit was $23.6 million, compared with $25.4 million in the prior year while gross margin contracted 110 basis points to 15.6%. Restructuring savings of $0.8 million, a $0.9 million reduction in tariff charges and pricing were more than offset by $1.9 million of higher costs related to unfavorable foreign currency exchange rates and the prior year benefit of $1.3 million of incremental tooling gains.

Selling, administrative and engineering ("SAE") expenses increased 3%, or $0.6 million, to

$17.5 million, or 11.5% of sales, compared with $16.9 million, or 11.1% of sales, in the prior-year period. Higher SAE expenses included $1.4 million in business transformation and executive transition costs. These costs were partially offset by a $0.7 million reduction in engineering and professional fees and $0.2 million of restructuring savings.

Interest income grew $0.1 million on higher cash balances, while interest expenses declined

$0.2 million on lower borrowings. Other income increased $1.4 million primarily as a result of changes in foreign currency exchange rates.

Net income attributable to Strattec was $3.9 million, or $0.95 per diluted share, compared with

$8.3 million, or $2.01 per diluted share, in the prior-year period. On an adjusted basis, fourth quarter fiscal 2026 net income attributable to Strattec was $8.4 million and adjusted diluted earnings per share 1 was $2.06 unchanged from the prior year.

Adjusted EBITDA 1 for the quarter was $12.5 million compared with $13.0 million in the prior-year period. Adjusted EBITDA margin of 8.3%, compared with 8.5% in the fiscal 2025 fourth quarter.

Solid Balance Sheet

Cash from operations in the fourth quarter of fiscal 2026 was $9.7 million, compared with

$30.2 million in the prior-year period which benefited from a significant reduction in working capital.

At June 28, 2026, Strattec had $108.2 million in cash and cash equivalents, up from

$107.0 million at the end of the third quarter of fiscal 2026 and $84.6 million at the end of the prior fiscal year. During the quarter, the Company paid down the remaining $1.0 million in outstanding borrowings on the JV credit facility. The Company also repurchased 110,269 shares for $7.4 million for an average price of $67.10. There is $40 million remaining under the current share repurchase authorization.

Fourth Quarter and Fiscal Year 2026 Webcast and Conference Call

Strattec Transformation Delivers Margin Improvement and Strong Cash Generation in Fiscal 2026

August 25, 2026

Page 3 of 10

Strattec will host a conference call and webcast tomorrow, Wednesday, August 26, 2026, at 8:00 am Central Time/9:00 am Eastern Time to review the financial and operating results for the period ended June 28, 2026, and provide an update on its transformation progress. A question-and-answer session will follow.

You can access the call by phoning +1 (201) 689-8470 or find the webcast and accompanying slide presentation at investors.strattec.com .

A telephonic replay will be available from approximately 11:00 am CT on the day of the call through Wednesday, September 9, 2026. To listen to the archived call, dial +1 (412) 317-6671 and enter replay PIN 13761060. The webcast replay will be available on the Investor Relations section of the Company's website at investors.strattec.com , where a transcript will be posted once available.

About Strattec

Strattec is a global automotive access company that designs and delivers safe, secure, and highly engineered access solutions for the automotive and mobility industries. Built on generations of access and security engineering expertise, Strattec partners closely with OEMs to create differentiated, system‑level access experiences for end consumers. Strattec's portfolio spans the access journey from Permission, enabling secure vehicle entry through advanced mechanical and electronic systems; to Motion, delivering effortless, reliable powered access that enhances everyday usability; and through to Hold, providing precision‑engineered latching solutions that give drivers confidence through proven strength, safety, and durability trusted by OEMs worldwide.

As access becomes increasingly intelligent, connected, and central to vehicle experience, Strattec's strategy is to expand its market share, further diversify its customers and geographic reach while becoming the most trusted access partner to drive long‑term growth across global automotive and mobility markets. For more information, visit www.strattec.com .

Page 5 of 10

STRATTEC SECURITY CORPORATION
CONDENSED CONSOLIDATED STATEMENTS OF INCOME (UNAUDITED)
(in thousands, except per share amounts)
Three Months Ended | Twelve Months Ended
June 28, 2026 | June 29, 2025 | June 28, 2026 | June 29, 2025
Net sales | 151,827 | 152,013 | 579,392 | 565,066
Cost of goods sold | 128,179 | 126,613 | 484,027 | 480,489
Gross profit | 23,648 | 25,400 | 95,365 | 84,577
Gross margin | 15.6 | % | 16.7 | % | 16.5 | % | 15.0 | %
Selling, administrative and engineering expenses | 17,480 | 16,898 | 68,842 | 61,793
Income from operations | 6,168 | 8,502 | 26,523 | 22,784
Operating margin | 4.1 | % | 5.6 | % | 4.6 | % | 4.0 | %
Interest income | 859 | 753 | 3,500 | 2,039
Interest expense | (37 | (212 | (359 | (1,007
Other income, net | 2,630 | 1,189 | 3,298 | 820
Income before provision for income taxes and non-controlling interest | 9,620 | 10,232 | 32,962 | 24,636
Income tax expense | 6,002 | 2,170 | 11,339 | 5,717
Net income | 3,618 | 8,062 | 21,623 | 18,919
Net income (loss) attributable to non-controlling interest | (264 | (205 | 1,025 | 234
Net income attributable to Strattec | 3,882 | 8,267 | 20,598 | 18,685
Earnings per share attributable to Strattec
Basic | 0.96 | 2.05 | 5.07 | 4.64
Diluted | 0.95 | 2.01 | 5.00 | 4.58
Weighted average shares outstanding:
Basic | 4,035 | 4,039 | 4,064 | 4,030
Diluted | 4,091 | 4,105 | 4,122 | 4,076

Strattec Transformation Delivers Margin Improvement and Strong Cash Generation in Fiscal 2026

August 25, 2026

Page 6 of 10

STRATTEC SECURITY CORPORATION
CONDENSED CONSOLIDATED BALANCE SHEETS (UNAUDITED)
(in thousands, except share amounts)
June 28, 2026 | June 29, 2025
ASSETS
Current Assets:
Cash and cash equivalents | 108,243 | 84,579
Receivables, net | 99,109 | 102,061
Inventories, net | 64,310 | 64,701
Pre-production costs | 6,489 | 8,657
Value-added tax recoverable | 10,069 | 19,389
Other current assets | 8,053 | 10,676
Total current assets | 296,273 | 290,063
Noncurrent Assets:
Property, plant and equipment, net | 69,845 | 77,410
Deferred income taxes | 16,080 | 19,531
Other long-term assets | 5,281 | 4,450
Total Assets | 387,479 | 391,454
LIABILITIES AND SHAREHOLDERS' EQUITY
Current Liabilities:
Accounts payable | 54,973 | 65,824
Accrued payroll and benefits | 20,773 | 22,956
Value-added tax payable | 7,429 | 11,933
Warranty reserve | 6,673 | 8,900
Other current liabilities | 12,383 | 9,737
Total current liabilities | 102,231 | 119,350
Noncurrent Liabilities:
Borrowings under credit facilities | — | 8,000
Post-employment benefits | 13,350 | 13,325
Other noncurrent liabilities | 6,401 | 4,348
Total Liabilities | 121,982 | 145,023
Shareholders' Equity:
Common stock, authorized 18,000,000 shares, $.01 par value, 7,704,994 issued shares at June 28, 2026 and 7,635,883 issued shares at June 29, 2025 | 77 | 76
Capital in excess of par value | 107,138 | 103,784
Retained earnings | 289,895 | 269,297
Accumulated other comprehensive loss | (14,143 | (16,113
Less: treasury stock, at cost (3,727,322 shares at June 28, 2026 and 3,596,549 shares at June 29, 2025) | (144,321 | (135,452
Total Strattec shareholders' equity | 238,646 | 221,592
Non-controlling interest | 26,851 | 24,839
Total Shareholders' Equity | 265,497 | 246,431
Total Liabilities and Shareholders' Equity | 387,479 | 391,454

Strattec Transformation Delivers Margin Improvement and Strong Cash Generation in Fiscal 2026

August 25, 2026

Page 7 of 10

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-08-28_item7_mdna.md)

_Extraction: started at the Overview heading._

Business Overview

Strattec is a global automotive access company that designs and delivers safe, secure, and highly engineered access solutions for the automotive and mobility industries. Built on generations of access and security engineering expertise, Strattec partners closely with OEMs to create differentiated, system‑level access experiences for end consumers. Strattec's portfolio spans the access journey from Permission, enabling secure vehicle entry through advanced mechanical and electronic systems; to Motion, delivering effortless, reliable powered access that enhances everyday usability; and through to Hold, providing precision‑engineered latching solutions that give drivers confidence through proven strength, safety, and durability trusted by OEMs worldwide. As access becomes increasingly intelligent, connected, and central to vehicle experience, Strattec's strategy is to expand its market share, further diversify its customers and geographic reach while becoming the most trusted access partner to drive long‑term growth across global automotive and mobility markets. While the Company serves major automotive OEMs globally, the majority of sales are to the three largest automobile original equipment manufacturers in North America.

Current Business Update

Our strategic priority is to execute on a business transformation to strengthen the Company's profitability and deliver sustainable sales growth. We expect to improve our business with upgraded systems and processes, modernization of our support functions and focus on productivity and efficiencies in our manufacturing operations. We believe this will result in an optimized cost structure and consistent cash generation through improved working capital velocity and efficient asset utilization. To drive organic growth, we will leverage our technical engineering expertise, market leading positions and strong customer relationships to generate innovative solutions and capture more content on current platforms, win new platforms with current customers, gain new customers both domestically and abroad and build opportunities in the broader transportation industry. The strength of our balance sheet also supports continued investments in process modernization, automation and new product innovation, as well as the flexibility needed to navigate through industry cycles.

Fiscal 2026 Financial Highlights

•
Grew net sales 3% to $579.4 million driven by pricing and volume increases

•
Expanded gross margin 150 basis points to 16.5%

•
Delivered a 10% increase in net income to $20.6 million, or $5.00 per diluted share

•
Generated $46.3 million of cash flow from operations driven by cash earnings and working capital management

•
Returned $7.4 million of capital to shareholders through the repurchase of over 2% of our outstanding common stock

Business Transformation

During fiscal 2026, we continued executing on our multi-year business transformation. We made significant progress on organizational restructuring actions, operational improvements and investments in business processes and technology. We reduced total headcount by approximately 7% during the year while maintaining support for customer programs and key growth initiatives. Operationally, we continued implementing initiatives designed to improve efficiency and cost competitiveness, including manufacturing automation, freight optimization and supply chain resiliency projects. These efforts contributed to improved gross profit margin despite foreign exchange headwinds and fluctuating customer production schedules. We also advanced several foundational process and technology initiatives intended to strengthen decision-making, improve data visibility, and increase organizational effectiveness.

Commercially, we continued efforts to strengthen customer engagement, improve quoting and program management processes, refine our product portfolio and pursue opportunities to win new business from both existing and prospective customers. The automotive industry is characterized by long product development and customer sourcing cycles. New vehicle programs are typically awarded several years before the start of production, requiring suppliers to invest significant engineering, validation, tooling and program management resources well in advance of realizing sales. Customer relationships are often developed over an extended period, and it may take five to seven years or longer to establish new OEM relationships, demonstrate technical capabilities, earn customer trust and secure meaningful production awards. As a result, we are actively working to be included on vehicle platforms scheduled for production in model years 2030 and beyond. We are also working to expand our reach to a broader customer set than we have addressed historically. Our strategic initiatives are aimed at building a more predictable business that can generate consistent cash flow across industry cycles.

We believe these transformational initiatives, combined with ongoing investments in organizational capabilities, will better position the Company to respond in a changing automotive market.

Capital Allocation

Over the past two years we have driven significant cash flow from operations which has resulted in the repayment of all existing debt and continued strengthening of our balance sheet. We are committed to a disciplined capital allocation approach, designed to maximize long-term shareholder value while maintaining financial flexibility through industry cycles. Our first priority is to maintain a strong balance sheet and sufficient liquidity to support working capital requirements and capital expenditures, and allow us to navigate potential market volatility. Given the cyclical nature of the automotive industry and ongoing macroeconomic uncertainty, we believe maintaining a strong balance sheet enhances our ability to invest through economic cycles and respond to changing customer and market conditions. Our second priority is investing in the business to support long-term growth and operational improvement. These investments include customer program launches, product development, manufacturing automation, cost reduction initiatives, information technology investments, and other strategic initiatives intended to improve our competitiveness and margins. Third, we evaluate opportunities to return excess capital to shareholders. Subject to market conditions and investment opportunities we may repurchase shares on an opportunistic basis and to offset dilution associated with equity compensation programs. We also allocate capital to pursue strategic acquisition opportunities that enhance our capabilities, expand customer relationships, increase scale, improve margins, or otherwise support our long-term strategic objectives.

Market & Macro Environment

The North American automotive market continues to experience uncertainty driven by evolving trade policies, foreign exchange fluctuations, changing vehicle affordability dynamics, shifting OEM production schedules and emerging Chinese OEMs. Industry production levels remained below historical peak levels during fiscal 2026, and third-party forecasts indicate a modest (2% to 3%) decline in North American light vehicle production in fiscal 2027, while our primary customers are expected to decline 5% to 6% over the next year. Recent production forecasts have been impacted by tariff-related uncertainty, consumer demand trends, and a reduced number of scheduled vehicle launches by certain OEMs. Several of our largest customers, including Ford, General Motors, and Stellantis, continue to operate in a highly competitive environment characterized by declining market share positions, ongoing electrification strategy adjustments, and efforts to optimize vehicle inventories and production schedules. Industry participants remain focused on balancing production with retail demand following the inventory rebuilding experienced after the COVID-19 supply disruptions.

The global trade environment also remains dynamic. During fiscal 2026, the United States implemented and modified tariffs on certain imported goods, while other countries introduced reciprocal measures and trade restrictions. In addition, the ongoing review of the United States‑Mexico‑Canada Agreement ("USMCA") and potential future changes to regional content requirements, rules of origin, and tariff treatment have contributed to uncertainty across the North American automotive supply chain. These developments have required us to evaluate sourcing strategies, localization opportunities, and supply chain resiliency initiatives.

Foreign currency movements, particularly fluctuations in the Mexican peso relative to the U.S. dollar, remain an important factor affecting our operating results. Because a significant portion of the Company's manufacturing operations are located in Mexico, peso appreciation increases labor and manufacturing costs when translated into U.S. dollars. During fiscal 2026, changes in foreign exchange rates affected both operating costs and the mark-to-market valuation of the Company's foreign currency hedging program. The Company continues to utilize forward currency contracts to reduce a portion of its exposure to Mexican peso fluctuations.

While macroeconomic uncertainty, fluctuating OEM production volumes, tariffs, and foreign exchange volatility remain challenges, we believe the actions taken during fiscal 2026 have improved profitability and enhanced cash generation. As we enter fiscal 2027, we remain focused on continuing to advance our strategic priorities, executing the business transformation, strengthening operational performance, and delivering long-term value for shareholders.

Analysis of Results of Operations

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business

_Not available: the fetcher did not split out this section for this filing. Describe the business from the MD&A overview above instead, and say so in the note._

## 10. Earnings call material

- **CALL PERIOD: 2026Q4** (call dated 2026-08-25)
- **Recency:** no earnings release to compare against.
- **File:** transcript_2026Q4_2026-08-25.md
- **Type:** EARNINGS PRESS RELEASE ONLY, not the call — no Q&A, no unscripted management commentary. Do not attribute call quotes to this.
- **Source:** https://www.sec.gov/Archives/edgar/data/933034/000093303426000003/strt-ex99_1.htm

EX-99.1

2

strt-ex99_1.htm

EX-99.1

EX-99.1

NEWS
RELEASE

FOR IMMEDIATE RELEASE
Strattec Transformation Delivers Margin Improvement and Strong Cash Generation in Fiscal 2026
•
Fourth quarter fiscal 2026 sales of $151.8 million was better than expected and relatively unchanged from prior year; achieved sales of $579.4 million for fiscal year 2026
•
Reported fourth quarter gross margin of 15.6%; full year gross margin expanded to 16.5%, up from 15.0% in fiscal 2025
•
Generated fourth quarter net income attributable to Strattec of $3.9 million, or $0.95 per diluted share; adjusted diluted earnings per share were $2.06, unchanged from the prior-year period
•
Fourth quarter Adjusted EBITDA was $12.5 million, or 8.3% of net sales, compared with $13.0 million, or 8.5% of sales in the prior-year period; fiscal 2026 Adjusted EBITDA
1
was $50.5 million, a 15.3% increase over the prior year
•
$108.2 million in cash and no debt; returned $7.4 million to shareholders through share repurchases in the fourth quarter and authorized a new $40 million share buyback program

MILWAUKEE, WI
, August 25, 2026 —
Strattec
(Nasdaq: STRT), a global provider of highly engineered access solutions for the automotive and mobility industries, today reported financial results for its fourth quarter and fiscal year 2026, which ended June 28, 2026.
Jennifer Slater, President and CEO of Strattec, said, “Fiscal 2026 was a year of progress and discipline as we continued to reshape Strattec into a more resilient, higher-performing business. While our fourth quarter and full-year results were impacted by foreign exchange pressure and the effect of tariffs, we nonetheless delivered year-over-year growth in sales and gross margin expansion through disciplined pricing, cost actions and operational improvements.”

She added, “We recognize that the near-term environment remains uncertain and we have much work to do to secure future OEM vehicle platforms. We are managing costs and capital prudently, while our strong cash position gives us the flexibility to continue investing in our product technologies, production automation and customer relationships. These investments will better position us to benefit when industry conditions improve. The strength of our balance sheet also allows us to

1
Refer to use of “Non-GAAP Financial Metrics and Additional Financial Information” as well as accompanying reconciliations to GAAP

3333 WEST GOOD HOPE ROAD
MILWAUKEE, WI 53209

414.247.3333
WWW.STRATTEC.COM

NASDAQ:
STRT

Strattec Transformation Delivers Margin Improvement and Strong Cash Generation in Fiscal 2026
August 25, 2026
Page
2
of 10

consider opportunities that could enhance scale and diversify our customers, products and programs over time.”

FY 2026 Fourth Quarter Financial Summary

_[...truncated at ~3,000 chars of this document]_

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | **MISSING** |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-08-28_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-08-28_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-25_2-02-results.md, 10-K_2026-08-28_item7_mdna.md, transcript_2026Q4_2026-08-25.md

**Missing:** 10-K Item 1 - Business (business description)

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
