# Triage pack — TBCH · Turtle Beach Corp

_Generated 2026-09-04 14:02 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** TBCH · **Name:** Turtle Beach Corp
- **CIK:** 0001493761
- **SIC:** 3669 — Communications Equipment, NEC
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/TBCH

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Turtle Beach Corp
- **CIK:** 1,493,761 · **SIC:** 3669 (Communications Equipment, NEC) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 12.52 |
| mktcap | $224.2M |
| ev | $281.1M |
| ev_ebit | 10.2x |
| fcf | $34.0M |
| fcf_yield | 15.2% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 15.8% |
| net_debt | $56.9M |
| net_debt_ebit | 2.1x |
| cash | $19.6M |
| ltd | $76.4M |
| equity | $80.7M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $319.9M |
| revenue_prior | $372.8M |
| rev_growth | -14.2% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $27.5M |
| net_income | $15.7M |
| cfo | $35.5M |
| capex | $1.4M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -9.6% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 17,909,711 |
| shares_py | 19,806,636 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -8.9% |
| r6m | -2.0% |
| off_52w_high | -26.7% |
| adv20 | $5.7M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.83 |
| r_ev_ebit | 0.76 |
| r_roic | 0.82 |
| r_rev_growth | 0.07 |
| r_buyback | 0.94 |
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
| rank | 72 |

**Screen rationale:** top-quartile FCF yield 15.2%; cheap at 10.2x EV/EBIT; high ROIC 15.8%; buying back stock -9.6%


## 3. Share count trend

- Shares outstanding: **17,909,711** (CY2026Q2I) vs **19,806,636** prior year (CY2025Q2I)
- Change: **-9.6%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-03** — Item 5.02 (officer / director change or comp arrangement): On July 28, 2026, Turtle Beach Corporation (the "Company") adopted the Turtle Beach Corporation Executive Severance Policy (the "Severance Policy"), pursuant to which the Company's Chief Executive Officer and certain other executives of the Company are...
- **2026-05-20** — Item 5.02 (officer / director change or comp arrangement): On May 16, 2026, Mark Weinswig informed the Company of his intent to resign as Chief Financial Officer of the Company, effective as of June 15, 2026.
- **2026-05-04** — Item 1.01 (Entry into a Material Definitive Agreement): On April 30, 2026, Turtle Beach Corporation (the "Company") entered into a new financing agreement (the "Term Loan Financing Agreement") by and among the Company, Voyetra Turtle Beach, Inc., a Delaware corporation, as borrower ("VTB"), each subsidiary of the...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 294,516 sh / $3,741,256 -> net $-3,741,256 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 50 (open-market buys 0, sales 6).

| code | rows |
|---|---|
| A | 9 |
| F | 5 |
| M | 30 |
| S | 6 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'SAN DIEGO, CA – August 6, 2026 – Turtle Beach Corporation (Nasdaq: TBC'; skipped 12 forward-looking-statement block(s); 8 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (tbch-ex99_1.htm)

SAN DIEGO, CA – August 6, 2026 – Turtle Beach Corporation (Nasdaq: TBCH), a leading gaming accessories brand, today reported financial results for the second quarter ended June 30, 2026 and reaffirmed full year 2026 guidance for net revenue and adjusted EBITDA.

Second Quarter Highlights

•
Net revenue was $56.4 million, compared to $56.8 million in the prior year

•
Gross margin improved to 38.8%, a year-over-year improvement of 660 basis points due to tariff refunds received in the second quarter 2026

•
Net loss of $7.3 million, compared to net loss of $2.9 million in the prior year

•
Adjusted EBITDA of $1.3 million compared to a loss of $3.0 million in the prior year

•
Generated cash flow from operations of $6.5 million, compared to cash outflow of $3.1 million in the prior year

•
Refinanced credit facilities to enhance financial flexibility and accelerate the Company's capital return program

•
Repurchased $25.0 million of common stock through share buyback program

•
Reaffirmed full year 2026 net revenue and adjusted EBITDA guidance of $335 million - $355 million and $44 million - $48 million, respectively

"We continued to execute on our robust new product roadmap during the second quarter, delivering innovative products across multiple categories, including the launch of our flagship Stealth Pro II headset," said Cris Keirn, Chief Executive Officer of Turtle Beach Corporation. "This launch represented a key milestone in our brand transformation and helped drive accelerating momentum across the business as the quarter progressed. Channel inventories continued to contract through the first half of the quarter, consistent with trends in the first quarter, before stabilizing later in the period. As retailers begin rebuilding inventory levels in anticipation of stronger consumer demand in the second half of the year, we expect a meaningful rebound in our business."

"Our confidence in our full-year 2026 outlook is supported not only by our execution but also by the favorable industry backdrop developing in the second half of the year. With the confirmed November launch of Grand Theft Auto VI and a strong lineup of other highly anticipated titles, we believe Turtle Beach is well positioned to capitalize on renewed consumer demand.

"Creating long-term value for our shareholders remains a core priority. During the second quarter, we repurchased $25.0 million of our common stock as part of our disciplined approach to capital allocation and our ongoing commitment to enhancing shareholder returns. As we enter a period of anticipated growth, we will continue to invest strategically in the business while remaining opportunistic in returning capital to shareholders."

Share Repurchases

During the second quarter, the Company repurchased 2.0 million shares at an average purchase price of $12.53 per share for $25.0 million. The current share repurchase program, authorized in May 2025, has approximately $31.0 million of remaining capacity. Since commencing buybacks in 2024, Turtle Beach has repurchased approximately $74 million of common stock.

Debt Refinancing

During the second quarter, the Company announced the restructuring of the Company's existing debt facilities. The new credit structure consists of a revolving asset-based lending ("ABL") facility of up to $80 million provided by Bank of America, N.A., and an $85 million term loan facility provided by Blue Torch Capital LP. Together, these facilities replaced the Company's prior $150 million credit agreement and provide the Company with increased operational and capital allocation flexibility.

Balance Sheet and Cash Flow Summary

On June 30, 2026, the Company had net debt of $64.4 million, comprised of $83.9 million of borrowings less $19.6 million of cash. During the second quarter ended June 30, 2026, the Company generated $6.5 million in cash flow from operations.

Financial Outlook

The Company is reiterating guidance for the full year 2026. Net revenues are expected to be between $335 million and $355 million, representing 5% to 11% year-over-year growth.

Adjusted EBITDA is expected to be between $44 million and $48 million, representing 10% to 20% year-over-year growth.

The Company remains encouraged by the gaming industry pipeline in 2026 and beyond. The confirmed launch of Grand Theft Auto VI in November 2026 is expected to be a significant industry event, and major game releases of this scale have historically driven increased gaming engagement and accessory demand. While the Company is not providing specific guidance beyond 2026 at this time, it believes the combination of its product innovation, brand strength, and favorable industry dynamics positions it for growth opportunities as these catalysts materialize.

Earnings Conference Call and Webcast Details

Turtle Beach will host a conference call and audio webcast today, August 6 at 4:30 p.m. Eastern Time (1:30 p.m. Pacific Time), during which management will discuss second quarter results and provide commentary on business performance and its current outlook for 2026. A question-and-answer session will follow the prepared remarks.

The conference call may be accessed by telephone by dialing 1-877-407-0792 or 1-201-689-8263.

A live audio webcast of the earnings conference call may be accessed on Turtle Beach's website at corp.turtlebeach.com , along with a copy of the earnings press release and an updated investor presentation. A telephone replay of the call will be available through August 20, 2026, and can be accessed by dialing

1-844-512-2921 or 1-412-317-6671 and entering passcode 13761399. A replay of the webcast will also be available on the investor relations website for a limited time.

About Turtle Beach Corporation

Turtle Beach Corporation (the "Company") ( corp.turtlebeach.com ) is one of the world's leading gaming accessory providers. The Company's namesake Turtle Beach brand ( www.turtlebeach.com ) is known for designing best-selling gaming headsets, top-rated game controllers, award-winning PC gaming peripherals, and groundbreaking gaming simulation accessories. Turtle Beach's top-rated, fan-favorite Victrix brand is well-respected and favored by pro gamers in esports and the fighting game community. Innovation, first-to-market features, a broad range of products for all types of gamers, and top-rated customer support have made Turtle Beach a fan-favorite brand and the market leader in console gaming audio for over a decade. Turtle Beach's shares are traded on the Nasdaq Exchange under the symbol: TBCH.

Non-GAAP Financial Measures

In addition to its reported results, the Company has included in this earnings release certain financial metrics, including Adjusted EBITDA, that the Securities and Exchange Commission define as "non-GAAP financial measures." Management believes that such non-GAAP financial measures, when read in conjunction with the Company's reported results, can provide useful supplemental information for investors analyzing period-to-period comparisons of the Company's results. Non-GAAP financial measures are not an alternative to the Company's GAAP financial results and may not be calculated in the same manner as similar measures presented by other companies. "Adjusted EBITDA" is defined by the Company as net income (loss) before interest, taxes, depreciation and amortization, stock-based compensation (non-cash), and certain non-recurring special items that we believe are not representative of core operations, as further described in Table 4. These non-GAAP financial measures are presented because management uses non-GAAP financial measures to evaluate the Company's operating performance, to perform financial planning, and to determine incentive compensation. Therefore, the Company believes that the presentation of non-GAAP financial measures provides useful supplementary information to, and facilitates additional analysis by, investors. The non-GAAP financial measures included herein exclude items that management does not believe reflect the Company's core operating performance because such items are inherently unusual, non-operating, unpredictable, non-recurring, or non-cash. See a reconciliation of GAAP results to Adjusted EBITDA included as Table 4 below for the three and six months ended June 30, 2026, and June 30, 2025 .

By providing full year 2026 Adjusted EBITDA guidance, the Company provided its expectation of a forward-looking non-GAAP financial measure. Information reconciling full year 2026 Adjusted EBITDA to its most directly comparable GAAP financial measure, net income (loss), is unavailable to the Company without unreasonable effort due to the variability, complexity, and lack of visibility with respect to certain reconciling items between Adjusted EBITDA and net income (loss), including other income (expense), provision for income taxes and stock-based compensation. These items cannot be reasonably and accurately predicted without the investment of undue time, cost and other resources and, accordingly, a reconciliation of the Company's Adjusted EBITDA outlook to its net income (loss) outlook for such periods is not provided. These reconciling items could be material to the Company's actual results for such periods.

Turtle Beach Corporation

858.914.5093

kim.denapoli@turtlebeach.com

Turtle Beach Corporation

Condensed Consolidated Statements of Operations

(in thousands, except per-share data)

(unaudited)

Table 1.

Three Months Ended | Six Months Ended
June 30, | June 30, | June 30, | June 30,
2026 | 2025 | 2026 | 2025
Net revenue | 56,365 | 56,777 | 98,537 | 120,678
Cost of revenue | 34,502 | 38,515 | 65,380 | 79,049
Gross profit | 21,863 | 18,262 | 33,157 | 41,629
Operating expenses:
Selling and marketing | 14,700 | 12,731 | 26,960 | 25,184
Research and development | 4,813 | 4,471 | 9,387 | 8,464
General and administrative | 5,401 | 7,354 | 13,922 | 15,570
Insurance recovery | — | (5,965 | — | (9,404
Acquisition-related cost | — | — | — | 608
Total operating expenses | 24,914 | 18,591 | 50,269 | 40,422
Operating (loss) income | (3,051 | (329 | (17,112 | 1,207
Interest expense, net | 3,666 | 2,049 | 5,035 | 4,055
Other expense (income), net | 73 | 799 | (28 | 1,102
Loss before income tax | (6,790 | (3,177 | (22,119 | (3,950
Income tax expense (benefit) | 521 | (246 | 398 | (355
Net loss | (7,311 | (2,931 | (22,517 | (3,595
Net loss per share
Basic | (0.38 | (0.14 | (1.16 | (0.17
Diluted | (0.38 | (0.14 | (1.16 | (0.17
Weighted average number of shares:
Basic | 19,182 | 20,667 | 19,339 | 20,587
Diluted | 19,182 | 20,667 | 19,339 | 20,587

Turtle Beach Corporation

Condensed Consolidated Balance Sheets

(in thousands, except par value and share amounts)

Table 2.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-12_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We are a premier audio and gaming technology company with expertise and experience in developing, commercializing, and marketing innovative products across a range of large addressable markets under our brand, Turtle Beach. The Turtle Beach® brand is a market share leader in console gaming headsets for over 16 years running with a vast portfolio of headsets designed to be multiplatform compatible with the latest Xbox, PlayStation, and Nintendo consoles, as well as for PCs and mobile and tablet devices. Our PC product portfolio includes PC gaming headsets, keyboards, mice, microphones and other PC gaming peripherals and in 2021 it expanded its brand beyond gaming headsets and launched its gaming controller product line, as well as, flight simulation and racing simulation accessories. In 2024, we acquired PDP, another leading gaming accessory brand with a robust slate of products, including gaming controllers for all major platforms and licensing deals with popular gaming and entertainment properties. We are headquartered in San Diego, California, and incorporated in the state of Nevada in 2010.

Business Trends

Console Headset Market

In 2025, we were the leading gaming headset manufacturer in the U.S. and other major console markets. We have achieved these global market shares by delivering high-quality products that often include first-to-market innovations, robust features, superior sound, unmatched comfort, and top customer support – all key factors that consumers seek when shopping for a gaming headset.

The global market for console and PC gaming headsets is estimated to be approximately $2.9 billion, according to external market data and internal estimates, reflecting continued growth driven by increasing online multiplayer engagement, content creation, and improvements in technology. PlayStation and Xbox consoles remain among the most significant platforms supporting gaming headset usage, as console-focused headsets continue to integrate features such as wireless connectivity and surround sound optimized for these systems. Consistent with a historical pattern of major new console cycles of roughly seven to eight years, Microsoft and Sony launched their latest consoles, Xbox Series X|S and PlayStation 5, ahead of the 2020 holiday season, and these platforms have sustained an active installed base through 2025. In late 2024, Sony introduced the PS5 Pro system. The next Microsoft and Sony consoles are anticipated to launch within the next 2-3 years.

Nintendo's platform also plays a significant role in the growth of the console headset market. The large installed base of Nintendo Switch systems, combined with the successful launch of the Nintendo Switch 2 in June 2025, increases participation in online, chat-enabled gameplay, thereby expanding the overall addressable market for console gaming headsets.

Controllers

The controllers market is estimated at approximately $3.0 billion, according to external market data and internal estimates, and shares the same retail footprint and consumer base as Turtle Beach gaming headsets, creating natural cross-sell opportunities and strong category alignment. We entered the controllers market in 2021 and have since expanded our portfolio across console and PC platforms, with key products including Stealth Ultra and Stealth Pivot premium controllers, which target the higher value controller segment. The 2024 acquisition of PDP, a leading gaming accessories company with a strong foundation in the controller category, significantly strengthened our scale and competitiveness in controllers. PDP's established expertise and product portfolio, spanning high-value and enthusiast-driven segments, expanded our offerings with products such as the Riffmaster Wireless Guitar Controller and Victrix Pro BFG, Pro FS Arcade Fight Stick, and Pro KO Leverless Fight Stick, positioning us across both premium and value tiers and across multiple controller subcategories.

Industry activity across console platforms, continues to support category growth. Ongoing hardware refresh cycles and the large global installed base, continues to drive engagement across core gaming genres such as multiplayer, esports, fighting games, and rhythm‑based gaming. These trends, along with market forecasts projecting sustained controller demand tied to wireless adoption, haptic feedback innovations, and cross‑platform compatibility, indicate that the controllers category remains an attractive growth opportunity.

With an expanded product portfolio and enhanced innovation pipeline following the PDP acquisition, we believe we are well positioned to capture additional share in the global controllers market as consumer interest and platform ecosystems continue to evolve.

PC Accessories Market

The market for PC gaming mice, keyboards, and microphones is estimated to be approximately $3.9 billion, according to external market data and internal estimates. PC gaming continues to be a main gaming platform in the U.S. and internationally, similarly driven by popular AAA game launches, PC-specific esports leagues, teams, and players, content creators, and influencers, and with the introduction of cross-platform play – where PC gamers can play online against other gamers playing the same game on an Xbox, PlayStation, or Nintendo Switch. While most games are available on multiple platforms, gaming on PC offers advantages including improved graphics, increased speed and precision of mouse/keyboard controls, and the ability for deeper customization. Gaming mice and keyboards are engineered to provide gamers with high-end performance and a superior gaming experience through features such as fast key and button response times, improved materials and build quality, comfortable ergonomic designs, programmable keys and buttons, and software suites to customize and control devices and settings.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Management Overview

In 2025, we continued integrating and building upon our acquisition of PDP, a leading gaming accessory brand recognized for its diverse product lineup. The acquisition expanded our presence in the multi-platform controllers category and added a strong set of licensing partnerships, further strengthening our competitive position. The increased scale and diversification resulting from the PDP acquisition have enhanced our market position and broadened our portfolio. These strategic gains provide a stronger foundation for long-term performance as we continue to deliver industry-leading gaming accessories and an expanded suite of offerings.

Revenue for 2025 reflects the contribution from the PDP acquisition and performance in our headset and controller categories, offset by decline in demand for gaming accessories. Our portfolio continued to perform well, highlighted by ongoing demand for products such as the Stealth 700 Gen 3 wireless headset, a premium, multi-platform device featuring our proprietary cross-play technology, which proved to be a top choice among gamers. This performance underscores our commitment to delivering cutting-edge accessories and our leadership in key gaming accessory markets.

Disciplined execution of our strategic priorities, together with targeted cost-management initiatives, contributed to a more resilient operating environment during the year. Although operating expenses increased modestly, these actions helped increase gross profit and maintain operating leverage amid softer revenue. We believe our brands are well-positioned to sustain market leadership due to our expanded product portfolio, strengthened retail partnerships, and strong portfolio of innovative console gaming headsets and controllers.

The following table sets forth the Company's consolidated statements of operations for the periods presented (in thousands):

Year Ended
December 31,
2025 | 2024
Net revenue | 319,914 | 372,766
Cost of revenue | 200,631 | 243,784
Gross profit | 119,283 | 128,982
Operating expenses:
Selling and marketing | 52,485 | 52,429
Research and development | 16,886 | 17,304
General and administrative | 30,374 | 28,388
Insurance recovery | (9,404 | —
Acquisition-related costs | 1,424 | 10,832
Total operating expenses | 91,765 | 108,953
Operating income | 27,518 | 20,029
Interest expense, net | 9,771 | 8,068
Other expense, net | 945 | 1,289
Income before income tax | 16,802 | 10,672
Income tax expense (benefit) | 1,071 | (5,511
Net income | 15,731 | 16,183

The following table sets forth the Company's consolidated statements of operations data as a percentage of revenue for the periods presented:

Year Ended
December 31,
2025 | 2024
Net revenue | 100.0 | % | 100.0 | %
Cost of revenue | 62.7 | 65.4
Gross profit | 37.3 | 34.6
Operating expenses:
Selling and marketing | 16.4 | 14.1
Research and development | 5.3 | 4.6
General and administrative | 9.5 | 7.6
Insurance recovery | (2.9 | —
Acquisition-related costs | 0.4 | 2.9
Total operating expenses | 28.7 | 29.2
Operating income | 8.6 | 5.4
Interest expense, net | 3.1 | 2.2
Other expense, net | 0.3 | 0.3
Income before income tax | 5.3 | 2.9
Income tax expense (benefit) | 0.3 | (1.5
Net income | 4.9 | % | 4.3 | %

Net Revenue and Gross Profit

Comparison of the Year Ended December 31, 2025 to the Year Ended December 31, 2024

Net revenue for the year ended December 31, 2025 was $319.9 million, a $52.9 million, or 14.2%, decrease from $372.8 million in the prior year. The decrease was due to a decline in demand for gaming accessories in the current year.

For the year ended December 31, 2025, gross margin increased to 37.3% from 34.6%, in the comparable prior year period primarily due to the unfavorable impact of fair value step-up adjustment in the prior year period relating to the PDP acquisition, partially offset by higher tariffs in 2025.

Operating Expenses

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-12_item1_business.md)

Item 1 - Busi ness

Our mission is to deliver the ultimate experience to gamers by providing high-quality, high-performance gaming accessories, including headsets, controllers, keyboards, mice, flight and racing simulation hardware, microphones, and more. For over 50 years, we have been a pioneer and key innovator in audio technology, and today we are one of the most recognized brand names in gaming. Headquartered in San Diego, California, we were incorporated in the state of Nevada in 2010, and our stock is traded on the Nasdaq Global Market under the symbol TBCH.

According to retail sales tracking data from The Circana Group ("Circana"), we have been the market share leader in console gaming headsets for 16-years running with a vast portfolio of headsets designed to be multiplatform compatible with the latest Xbox, PlayStation, and Nintendo consoles, as well as for personal computers ("PCs") and mobile and tablet devices. Our PC product portfolio includes PC gaming headsets, keyboards, mice, microphones, and other PC gaming peripherals, and we expanded our brand beyond gaming headsets to include our gaming controller product line, as well as flight simulation. In 2024, we acquired Performance Designed Products ("PDP"), another leading gaming accessory brand with a robust slate of products, including gaming controllers for all major platforms and licensing deals with popular gaming and entertainment properties.

Gaming Accessories Business

We launched our first gaming headset and the first ever console gaming headset – the X51 – in 2005 and have gone on to become the leading brand in gaming headsets, as well as a top five overall gaming accessory business in the world. We design and market a broad assortment of gaming headsets and audio accessories for Xbox, PlayStation, and Nintendo consoles, as well as for PC, mobile and tablet devices. Our 2024 acquisition of PDP, and prior acquisitions of ROCCAT (2019) and Neat Microphones (2021) expanded our reach into the global markets for PC gaming headsets, keyboards, mice, and other gaming accessories. Additionally, in 2021, we further expanded our reach beyond gaming headsets with the launch of the first Turtle Beach game controllers for Xbox/PC, as well as flight simulation accessories. In 2024, we entered the racing simulation gaming accessory market. Our gaming accessories are distributed globally, with more than 475 thousand points of distribution, including major retailers such as Amazon, Argos, Best Buy, Target, and Walmart.

Our brand offers gamers a broad assortment of gaming accessories available at price tiers ranging from entry-level ~$30 to ultra-premium $650+. These price tiers correspond to customer profiles, beginning with entry-level gamers and progressing through casual, enthusiast, core, as well as with professional streamers, content creators, and competitive esports gamers. Each successive price tier incorporates higher-level features, comfort, and finish. For example, premium headsets typically include features like larger 50mm speakers, metal headbands, memory foam, powerful amplified 3D surround sound, active noise-cancellation, and Bluetooth connectivity. Additional features include mic monitoring which allows you to hear the volume of your own voice inside your headset, gaming audio presets like bass and/or vocal boost, our exclusive Superhuman Hearing® sound setting which delivers a competitive advantage, a removable or flip-to-mute microphone, our proprietary ProSpecs™ glasses-friendly technology, and long-lasting rechargeable batteries.

Gaming consoles like the latest Xbox, PlayStation, and Nintendo Switch systems have evolved into full home entertainment hubs, and mobile tablet devices have become mainstream entertainment platforms with gaming on mobile and tablet devices now representing approximately 50% of the global gaming market. We continue to evolve our product portfolio to reflect how content is consumed. While each Turtle Beach headset is designed for a primary platform, such as a specific console or PC model, nearly all can be used with multiple platforms and are compatible with mobile and tablet devices through a standard 3.5mm jack or Bluetooth connectivity. Additionally, our products are often displayed in multiple in-store sections at retailers. This includes platform-specific gaming aisles for Xbox, PlayStation, Nintendo, PC, Virtual Reality (VR), and mobile and tablet products, as well as displayed on in-store kiosks that allow shoppers to experience each headset's fit, feel, and audio quality, increasing the prominence of our brand in physical retail locations, as well as online.

Industry Overview

We operate in a nearly $200.0 billion global games and accessories market, according to Newzoo Peripheral Market Forecast. The global gaming audience now exceeds global cinema and music markets with over 3.5 billion active gamers worldwide. Gaming peripherals, such as headsets, controllers, keyboards, mice, microphones, and flight and racing simulation controls are estimated to be an $11.2 billion business globally.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-12_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-12_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-12_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-03-12_item7_mdna.md, 10-K_2026-03-12_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
