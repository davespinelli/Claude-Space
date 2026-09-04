# Triage pack — ANIK · Anika Therapeutics, Inc.

_Generated 2026-09-04 23:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** ANIK · **Name:** Anika Therapeutics, Inc.
- **CIK:** 0000898437
- **SIC:** 3841 — Surgical & Medical Instruments & Apparatus
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/ANIK

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Anika Therapeutics, Inc.
- **CIK:** 898,437 · **SIC:** 3841 (Surgical & Medical Instruments & Apparatus) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 21.00 |
| mktcap | $281.0M |
| ev | $242.6M |
| ev_ebit | n/a |
| fcf | $4.4M |
| fcf_yield | 1.6% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -8.8% |
| net_debt | -$38.4M |
| net_debt_ebit | n/a |
| cash | $38.4M |
| ltd | $0.00 |
| equity | $137.3M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $112.8M |
| revenue_prior | $119.9M |
| rev_growth | -5.9% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$11.1M |
| net_income | -$11.0M |
| cfo | $11.2M |
| capex | $6.8M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -7.2% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 13,382,966 |
| shares_py | 14,418,090 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 113.0% |
| r6m | 47.4% |
| off_52w_high | -4.7% |
| adv20 | $2.6M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.28 |
| r_ev_ebit | 0.00 |
| r_roic | 0.14 |
| r_rev_growth | 0.16 |
| r_buyback | 0.92 |
| score | 0.35 |

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
| rank | 369 |

**Screen rationale:** buying back stock -7.2%; debt data missing (net cash unverified); 12-1 momentum 113.0%


## 3. Share count trend

- Shares outstanding: **13,382,966** (CY2026Q2I) vs **14,418,090** prior year (CY2025Q2I)
- Change: **-7.2%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-14** — Item 1.01 (Entry into a Material Definitive Agreement): On July 10, 2026, we entered into a Fifth Amendment to Credit Agreement,
- **2026-06-23** — Item 5.02 (officer / director change or comp arrangement): Sixth Amendment and Restatement of the Anika Therapeutics, Inc. 2017 Omnibus Incentive Plan
- **2026-04-29** — Item 5.02 (officer / director change or comp arrangement): On April 24, 2026, both William R. Jellison, a Class I member of the Board of Directors (the "Board") of the Company, and Glenn R. Larsen, Ph.D., a Class II member of the Board, notified the Board of their resignation from the Board, including from all...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 19,200 sh / $264,260 vs sells 0 sh / $0 -> net $264,260 (BUYING).
Distinct insiders buying (code P): 3. Largest buy: Griffin Stephen D. bought 12,200 sh @ $12.29 ($149,881) on 2026-04-30.

Form 4 filings parsed: 12; transaction rows: 26 (open-market buys 4, sales 0).

| code | rows |
|---|---|
| A | 10 |
| F | 4 |
| M | 8 |
| P | 4 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-29_2-02-results.md)

_Extraction: started at the first release heading, 'Anika Reports Second Quarter 2026 Financial Results'; skipped 8 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99.1 - PRESS RELEASE (exh_991.htm)

Anika Reports Second Quarter 2026 Financial Results

Commercial Channel Revenue Increased 17% to a Record $13.9 Million

Delivered $3.3 Million of Net Income, 65% Gross Margin, and $7.1 Million of Adjusted EBITDA, Highest Since 2020

Raising Full-Year 2026 Financial Guidance and Revising 2027 Revenue Forecast

BEDFORD, Mass., July 29, 2026 (GLOBE NEWSWIRE) -- Anika Therapeutics, Inc. (Nasdaq: ANIK), a global leader in the osteoarthritis ("OA") pain management and regenerative solutions spaces focused on early-intervention orthopedics, today announced financial results for the second quarter of 2026.

Total revenue for the second quarter was $32.6 million, compared to $28.2 million in the prior-year period. Performance was driven by record Commercial Channel revenue of $13.9 million , representing organic growth of 17% year-over-year , and continued strength in the OEM Channel supported by favorable US Monovisc and Orthovisc sales.

Gross profit for the second quarter was $21.2 million , compared to $14.4 million in the prior-year period. Gross margin expanded to 65% , reflecting higher sales volume, increased manufacturing production and improved sales mix.

Total operating expenses were $18.3 million, compared to $18.5 million in the prior-year period. Operating expense performance reflected continued cost discipline across the business while maintaining targeted investments to support commercial growth and strategic development programs. Excluding approximately $0.8 million of one-time severance-related expenses, adjusted operating expenses were $17.5 million, representing a decline of 6% versus the prior-year period.

Net income was $3.3 million for the second quarter, representing a 10% margin. Adjusted EBITDA was $7.1 million, representing a 22% Adjusted EBITDA margin reflecting continued benefits from commercial growth, gross margin expansion, and disciplined expense management.

"Our second quarter results mark a positive step forward in improving the performance of our business. We achieved record Commercial Channel revenue, substantial gross margin expansion, and our highest adjusted EBITDA since 2020. The actions we initiated earlier this year are delivering early gains as we continue to drive operational excellence throughout the Company. Additionally, our growth has diversified across channels and geographies, highlighted by a record quarter of international revenue." said Steve Griffin, President and Chief Executive Officer.

"Our OEM business continues to perform well, supported by stronger transfer unit volumes driven by J&J DePuy Synthes, order timing across both the Monovisc and Orthovisc product lines, favorable U.S. Monovisc end market sales, and continued international growth. These drivers increased production, throughput and manufacturing yields, resulting in meaningful gross margin expansion and operating leverage. Combined with disciplined expense management, a 20% reduction in G&A expenses (or 30% excluding one-time severance-related charges), and lower stock-based compensation expense, these improvements are translating into meaningful profitability gains.

Given our first-half performance, we are raising our full-year financial outlook. Most notably, we are raising our adjusted EBITDA margin outlook to 13%-17%, driven by improved operating leverage. Our improved outlook is supported by favorable OEM sales trends, continued Commercial Channel growth, operational improvements, and disciplined cost management. While we expect some moderation in revenue and profitability during the second half relative to the strong first half, reflecting the timing of certain OEM orders, we remain encouraged by the underlying trends in the business and our ability to deliver improved full-year performance. We are still early in our company-wide transformation, yet the results achieved in the first half reinforce that our strategy is working and that disciplined execution against our mission is creating sustainable value.

As we continue to advance toward filing the Cingal New Drug Application ("NDA") we're making steady progress on the bioequivalence study for Triamcinolone Hexacetonide and are accelerating the necessary Chemistry, Manufacturing and Controls ("CMC"), activities required to file Cingal as a drug-drug combination product. Additionally, we remain actively engaged with the U.S. Food and Drug Administration ("FDA") on Hyalofast, with discussions focusing primarily on the co-primary clinical endpoints within the Premarket Approval ("PMA") submission.

Given the timing uncertainty that remains in our regulatory review process, particularly as our discussions with the FDA on Hyalofast evolve, we are adopting a new revenue guidance practice. Going forward, our forecast will only include revenue from products that have received regulatory approval or clearance. As a result, our 2027 Commercial Channel revenue guidance no longer includes revenue associated with Hyalofast."

Second Quarter 2026 Business Highlights and Updates

Strong first-half execution drove record revenue performance, significant gross margin expansion, and a raise to full-year revenue and EBITDA guidance.

Commercial Channel revenue increased 17% year-over-year to a record $13.9 million, representing the strongest quarter in Company history.

International revenue reached a record $12.6 million, increasing 22% year-over-year and exceeding the prior quarterly record by 5%, reflecting continued strength across key markets and the increasing contribution from Anika's global commercial organization.

OEM Channel performance benefited from strong transfer units, favorable order timing and Monovisc volume growth, partially offset by lower Orthovisc sales.

Integrity global units increased both sequentially and year-over-year during the second quarter, driven by growing international demand and continued adoption of larger implant shapes and sizes in the US. Year-to-date sales grew 39% year over year.

Hyalofast PMA activities continue to advance, with the Company remaining actively engaged with the FDA as it works through the ongoing review process and responses to the previously disclosed deficiency letter.

Cingal development remains on track, with bioequivalence study enrollment progressing as planned. Concurrently, the required CMC activities supporting hyaluronic acid as a drug are accelerating in preparation for the NDA submission.

Second Quarter 2026 Continuing Operations Financial Summary

Revenue: $32.6 million, up 16% year over year

Commercial Channel revenue: $13.9 million, up 17%

OEM Channel revenue: $18.7 million, up 14%

Gross margin: 65%

Operating expenses: $18.3 million

GAAP income (loss) from continuing operations : $3.3 million , $0.24 per diluted share

Adjusted net income from continuing operationsˆ: $5.9 million , $0.42 per diluted share

Adjusted EBITDAˆ: $7.1 million

Cash and cash equivalents: $38.4 million as of June 30, 2026

ˆSee description of non-GAAP financial information contained in this release.

Fiscal 2026 Guidance

Based on strong first-half operating performance, continued commercial momentum, favorable OEM dynamics, and improved profitability, Anika is raising its full-year 2026 guidance.

Updated 2026 Guidance

Raising Total Company Revenue Guidance: revenue growth of 5% to 10%, compared to previous guidance of 1% to 9%
OEM Channel revenue growth: 0% to 5%, compared to previous guidance of down 5% to flat

Commercial Channel revenue growth: 12% to 18%, compared to previous guidance of 10% to 20%

Adjusted EBITDA margin: 13% to 17%, compared to previous guidance of 5% to 10%

Updated 2027 Revenue Guidance

Anika has adopted a new revenue guidance practice. Going forward, the Company's forecast will only include revenue for products that have received regulatory approval or clearance.

2027 Commercial Channel revenue growth: 5% to 15%, compared to previous guidance of 10% to 20%

2027 OEM revenue growth: Unchanged, flat to modestly lower

2027 Total Company revenue: flat to 5% growth

Conference Call and Webcast Information

Anika's management will hold a conference call and webcast to discuss its financial results and business highlights today, Wednesday, July 29, 2026, at 8:30 am ET. The conference call can be accessed by dialing 1-800-717-1738 (toll-free domestic) or 1-646-307-1865 (international) and providing the conference ID number 60388. A live audio webcast will be available in the Investor Relations section of Anika's website, www.anika.com. A slide presentation with highlights from the conference call will be available in the Investor Relations section of the Anika website. A replay of the webcast will be available on Anika's website approximately two hours after the completion of the event.

About Anika

Anika Therapeutics, Inc. (NASDAQ: ANIK), is the global leader in the design, development, manufacturing, and commercialization of hyaluronic acid innovations. In partnership with clinicians, our sole focus is dedicated to delivering and advancing osteoarthritis pain management and orthopedic regenerative solutions. At our core is a passion to deliver a differentiated portfolio that improves patient outcomes around the world. Anika's global operations are headquartered outside of Boston, Massachusetts. For more information about Anika, please visit www.anika.com.

ANIKA, ANIKA THERAPEUTICS, CINGAL, HYALOFAST, INTEGRITY, MONOVISC, and the Anika logo are trademarks of Anika Therapeutics, Inc. or its subsidiaries or are licensed to Anika Therapeutics, Inc. for its use.

Non-GAAP Financial Information 1

Non-GAAP financial measures should be considered supplemental to, and not a substitute for, the Company's reported financial results prepared in accordance with GAAP. Furthermore, the Company's definition of non-GAAP measures may differ from similarly titled measures used by others. Because non-GAAP financial measures exclude the effect of items that will increase or decrease the Company's reported results of operations, Anika strongly encourages investors to review the Company's consolidated financial statements and publicly filed reports in their entirety. The Company presents these non-GAAP financial measures because it uses them as supplemental measures in internally assessing the Company's operating performance, and, in the case of Adjusted EBITDA, it is set as a key performance metric to determine executive compensation. The Company also recognizes that these non-GAAP measures are commonly used in determining business performance more broadly and believes that they are helpful to investors, securities analysts, and other interested parties as a measure of comparative operating performance from period to period.

Adjusted EBITDA

Adjusted EBITDA is defined by the Company as GAAP net income (loss) from continuing operations excluding depreciation and amortization, interest and other income (expense), income taxes, stock-based compensation expense, and non-recurring professional fees and severance costs.

Adjusted Net Income (Loss) from Continuing Operations and Adjusted Earnings Per Share ("EPS") from Continuing Operations

Adjusted net income (loss) is defined by the Company as GAAP net income (loss) from continuing operations, on a tax effected basis, excluding stock-based compensation, severance costs and non-recurring professional fees. Adjusted diluted EPS from continuing operations is defined by the Company as GAAP diluted EPS from continuing operations excluding stock-based compensation, severance costs and non-recurring professional fees, each on a tax effected basis.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-03_item7_mdna.md)

_Extraction: started at 'Results of Operations'._

Results of Operations

Year ended December 31, 2025 compared to year ended December 31, 2024

Statement of Operations Detail

Year Ended December 31,
2025 | 2024 | $ Change | % Change
(in thousands, except percentages)
Revenue | 112,819 | 119,907 | (7,088 | (6 | %)
Cost of revenue | 49,012 | 43,909 | 5,103 | 12 | %
Gross profit | 63,807 | 75,998 | (12,191 | (16 | %)
Gross margin | 57 | % | 63 | %
Operating expenses:
Research & development | 25,770 | 25,544 | 226 | 1 | %
Selling, general & administrative | 49,088 | 55,555 | (6,467 | (12 | %)
Total operating expenses | 74,858 | 81,099 | (6,241 | (8 | %)
Loss from operations | (11,051 | (5,101 | (5,950 | 117 | %
Interest and other income, net | 1,744 | 2,337 | (593 | (25 | %)
Loss before income taxes | (9,307 | (2,764 | (6,543 | 237 | %
Provision for income taxes | 672 | 6,064 | (5,392 | (89 | %)
Loss from continuing operations | (9,979 | (8,828 | (1,151 | 13 | %
Loss from discontinued operations, net of tax | (901 | (47,557 | 46,656 | (98 | %)
Net loss | (10,880 | (56,385 | 45,505 | (81 | %)

Revenue

We classify our revenue between the Original Equipment Manufacturer ("OEM") Channel and the Commercial Channel. In the OEM Channel, we are responsible for development and manufacturing of products sold to our OEM partners governed by long-term agreements, but we do not control sales, marketing, or pricing with end users. In the Commercial Channel, we have full responsibility for sales, marketing, and pricing of products through our commercial leaders, direct sales representatives, and independent distributors. Revenue from our Regenerative Solutions and international OA Pain Management businesses is included in the Commercial Channel.

The following table presents revenue by product family for fiscal years 2025 and 2024 (dollars in thousands):

Years Ended December 31,
2025 | 2024 | $ Change | % Change
OEM Channel | 64,406 | 77,770 | (13,364 | (17 | %)
Commercial Channel | 48,413 | 42,137 | 6,276 | 15 | %
112,819 | 119,907 | (7,088 | (6 | %)

Revenue for the year ended December 31, 2025 was $112.8 million, a decrease of $7.1 million, or 6%, compared to the prior year. The decrease in revenue was driven by lower pricing with our OEM channel partners, primarily J&J MedTech.

Revenue from our OEM Channel product family decreased 17% for the year ended December 31, 2025, as compared to prior year, due to a $12.6 million decrease in J&J MedTech revenue, primarily due to lower pricing contributing $10.0 million of the decrease and lower volumes contributing to $2.6 million of the decrease. There was a $0.8 million decrease in the Non-Orthopedic category revenue with prior year due to lower veterinary sales offset by higher ophthalmic and surgery product sales.

Revenue from our Commercial Channel product family increased 15% for the year ended December 31, 2025, as compared to prior year, due to international sales growth on Cingal and Orthovisc, offset by lower Monovisc shipments due to manufacturing delays. This sales growth in international OA Pain Management products was primarily related to increased product demand of $3.6 million and minimal change on pricing with international customers. We also continued our full market release of Integrity in the U.S. in 2025 which contributed to a $3.4 million increase during the year ended December 31, 2025 and we had a $0.8 million increase in Hyalofast which is sold only outside of the United States. These increases in international OA Pain Management, Hyalofast and Integrity revenues were offset by a $1.5 million decrease in Tactoset sales during 2025.

Gross Profit and Margin

Gross profit for the year ended December 31, 2025 was $63.8 million, or gross margin of 57%, as compared with $76.0 million, or gross margin of 63%, for the year ended December 31, 2024. The decrease in gross profit for the year ended December 31, 2025, primarily resulted from lower revenue, primarily related to OA Pain Management products in the U.S., product channel mix with a higher percentage of international sales which have a lower selling price, increased manufacturing costs and higher inventory reserves.

Research and Development

Research and development costs for the years ended December 31, 2025 and 2024 were as follows:

Years Ended December 31,
2025 | 2024 | $ Change | % Change
(in thousands, except percentages)
External costs by program
Hyalofast clinical study | 2,193 | 1,789 | 404 | 23 | %
Integrity development costs | 1,370 | 943 | 427 | 45 | %
Cingal clinical study | 2,998 | 363 | 2,635 | 726 | %
Regulatory external costs | 906 | 2,728 | (1,822 | (67 | %)
Other early programs and unallocated expenses | 3,631 | 3,884 | (253 | (7 | %)
Total external costs | 11,098 | 9,707 | 1,391 | 14 | %
Internal costs:
Employee compensation and benefits | 12,692 | 13,779 | (1,087 | (8 | %)
Facility and other | 1,980 | 2,058 | (78 | (4 | %)
Total internal costs | 14,672 | 15,837 | (1,165 | (7 | %)
Total research and development expense | 25,770 | 25,544 | 226 | 1 | %

Research and development external costs for the years ended December 31, 2025 and 2024 were $11.1 million and $9.7 million, respectively. The increase in research and development external costs was primarily due to increased spending on Cingal regulatory submission activities offset by lower regulatory costs related to EU MDR requirements.

Research and development internal costs for the years ended December 31, 2025 and 2024 were $14.7 million and $15.8 million, respectively. The decrease in internal research and development costs was primarily due to a reduction in headcount and a $0.1 million gain on the sale of an intangible asset during the year ended December 31, 2025.

For additional information on our research and development activities, please see the section captioned "Part I. Item 1. Business— Research and Development " in this Annual Report on Form 10-K.

Selling, General and Administrative

Selling, general and administrative ("SG&A") expenses for the year ended December 31, 2025 were $49.1 million, a decrease of $6.5 million, or 12%, as compared to the prior year. The decrease in SG&A expenses for the year ended December 31, 2025 was due primarily to lower general and administrative expenses such as $2.2 million in shareholder activism costs that occurred in prior year, $1.5 decrease in stock-based compensation and the remainder attributable to lower headcount and professional fees. We have been investing and expect to continue to invest in selling and marketing expenses primarily related to our Commercial Channel.

Loss from Continuing Operations

For the year ended December 31, 2025, the loss from continuing operations was $10.0 million, compared to a loss from continuing operations of $8.8 million for the prior year. The $1.2 million decrease in the loss from continuing operations was due to lower revenues, primarily from J&J MedTech offset somewhat by lower operating expenses, primarily related to lower SG&A expenses.

Income Taxes

The provision for income taxes was $0.7 million for the year ended December 31, 2025, resulting in an effective tax rate of (7.1%). The provision from income taxes was $6.1 million for the year ended December 31, 2024, resulting in an effective tax rate of (219.4%). The decrease in our effective rate for the year ended December 31, 2025 as compared to the year ended December 31, 2024 is primarily due to the fact that we did not incur current income taxes in the United States during the year ended December 31, 2025.

Non-GAAP Financial Measures

We present certain information with respect to adjusted Earnings Before Interest, Tax, Depreciation and Amortization ("EBITDA"), adjusted net income, adjusted diluted earnings per share or adjusted Earnings Per Share ("EPS"), which are financial measures not based on any standardized methodology prescribed by accounting principles generally accepted in the United States ("GAAP"), and is not necessarily comparable to similarly titled measures presented by other companies.

We have presented adjusted EBITDA, adjusted net income, adjusted EPS, because they are key measures used by our management and board of directors to understand and evaluate our operating performance and to develop operational goals for managing our business. We believe these financial measures help identify underlying trends in our business that could otherwise be masked by the effect of the expenses that we exclude. We believe that the exclusion of these items in calculating these measures can provide a useful tool for period-to-period comparisons of our core operating performance. Accordingly, we believe that these measures provide useful information to investors and others in understanding and evaluating our operating results, enhancing the overall understanding of our past performance and future prospects and allowing for greater transparency with respect to key financial metrics used by our management in their financial and operational decision-making.

Adjusted EBITDA

We present information below with respect to adjusted EBITDA, which we define as our net loss excluding interest and other income, net, income tax benefit, depreciation and amortization, stock-based compensation, product rationalization charges, and other non-recurring expenses.

Adjusted EBITDA is not prepared in accordance with U.S. GAAP, and should not be considered in isolation of, or as an alternative to, measures prepared in accordance with U.S. GAAP. There are a number of limitations related to the use of adjusted EBITDA rather than net income (loss), which is the nearest U.S. GAAP equivalent. Some of these limitations are:

• | adjusted EBITDA excludes depreciation and amortization, and, although these are non-cash expenses, the assets being depreciated or amortized may have to be replaced in the future, the cash requirements for which are not reflected in adjusted EBITDA;

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-03_item1_business.md)

ITEM 1. BUSINESS

Purpose and Mission

Founded in 1992, Anika Therapeutics, Inc. ("Anika" or "Company") is a global leader in the OA Pain Management and regenerative solutions space, focusing on early intervention orthopedics. The Company leverages proprietary hyaluronic acid ("HA") technology to develop highly differentiated products. Driven by strong partnerships with physicians, Anika is dedicated to pioneering HA-based innovations that redefine orthopedic care. Our mission is to restore active living, empower surgeon choice, and enhance patient outcomes worldwide.

Anika ' s Mission:

"Together, we restore active living and redefine what's possible with hyaluronic acid."

Anika ' s Core Values:

● | Trust and Respect: We build trust and show respect in every interaction.

● | Quality: We are committed to quality as we work to improve people's lives.

● | Empowerment & Teamwork: We are empowered as a team to make decisions that drive impact.

● | Focus: We focus on what matters most and are driven to be better every day.

Strategy

In October 2024, we announced a strategic shift to concentrate on our OA Pain Management and Regenerative Solutions portfolios. This strategic decision involved the sale of Arthrosurface Incorporated on October 31, 2024 and the sale of Parcus Medical, LLC on March 7, 2025, both of which were acquired in early 2020 under a previous management strategy.

As we look ahead, our focused strategy, driven by HA-based products, positions us to offer truly innovative treatments in areas of unmet need and substantial, growing markets. We will place particular emphasis on the commercial execution and adoption of the newest product in our Regenerative Solutions portfolio, the Integrity Implant System ("Integrity"), a HA-based scaffold designed for rotator cuff and other tendon repairs. The Integrity system has shown strong performance, with continuing growth in surgeries and significant adoption by new customers.

We will continue to invest in our Regenerative Solutions R&D pipeline as we prepare for the potential U.S. approval and launch of both Hyalofast and Cingal, each representing an incremental U.S. addressable market of at least $1 billion. We submitted our premarket approval ("PMA") application with the FDA for Hyalofast on October 31, 2025. We received a letter from the FDA in January 2026 in which the FDA identified a number of deficiencies in which we are preparing our response. Additionally, we will build on the international commercial momentum of our entire OA Pain Management portfolio, led by Monovisc and Cingal. Cingal has shown significant clinical success and we have been actively engaging with the FDA on next steps for regulatory approval in the U.S.

On October 31, 2024 (the "Arthrosurface Closing Date"), we completed the sale of all outstanding equity interests (the "Arthrosurface Transaction") of Arthrosurface Incorporated, a Delaware corporation and former wholly-owned subsidiary of the Company ("Arthrosurface"), which held our Arthrosurface asset group, to Phoenix Brio, Incorporated, a Delaware corporation ("Phoenix Brio"), pursuant to the terms and conditions of a Share Purchase Agreement, dated as of the Arthrosurface Closing Date (the "Arthrosurface Purchase Agreement"), by and amongst us, Arthrosurface, and Phoenix Brio.

As consideration for the Arthrosurface Transaction, at the closing, Phoenix Brio delivered to us a ten-year non-interest bearing promissory note in the principal amount of $7.0 million. Under the terms of the Purchase Agreement, we are also eligible to receive: (i) for each calendar quarter, an amount equal to a percentage of the net sales (the "Revenue Payments") for the sale of certain commercial and pipeline products during the period commencing on the Closing Date and ending on the earlier of the fifth (5th) anniversary of the Closing Date or the date on which the Buy-Out Payment (as defined below) is paid to us; and (ii) a percentage of the gross proceeds with respect to the sale of certain commercial and pipeline products in a bona fide arm's length transaction with a third party that is not an affiliate of Phoenix Brio or us occurring within the first twenty-four (24) months following the Closing Date. Phoenix Brio can also elect to make a payment in an amount equal to the greater of (A) $14.0 million or (B) ten (10) times the Revenue Payments ((A) and (B) together, the "Buy-Out Payment") paid to us during the last full calendar year prior to the consummation of a change of control transaction or Phoenix Brio's written notice to us that it is electing to make the Buy-Out Payment. Pursuant to the Arthrosurface Purchase Agreement, the aggregate consideration is subject to customary post-closing adjustments.

On March 7, 2025 (the "Parcus Closing Date"), we completed the sale of all of the outstanding equity interests of Parcus Medical, LLC, a Wisconsin limited liability company and former wholly-owned subsidiary of the Company ("Parcus"), to Medacta Americas Manufacturing, Inc., a Delaware corporation ("Medacta"), pursuant to the terms and conditions of a Membership Interest Purchase Agreement, dated as of the Closing Date (the "Parcus Purchase Agreement"), by and among the Company, Parcus and Buyer (the "Transaction"). As consideration for the Transaction, at closing, Medacta made a payment of $4.5 million in cash. Pursuant to the Parcus Purchase Agreement, the aggregate consideration is subject to customary post-closing adjustments.

Products and Services

We provide a broad array of products and services, including:

● | Osteoarthritis ( " OA " ) Pain Management : Orthovisc, Monovisc, and Cingal.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-03_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-03_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-03_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-07-29_2-02-results.md, 10-K_2026-03-03_item7_mdna.md, 10-K_2026-03-03_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
