# Triage pack — ZUMZ · Zumiez Inc

_Generated 2026-09-04 13:14 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** ZUMZ · **Name:** Zumiez Inc
- **CIK:** 0001318008
- **SIC:** 5600 — Retail-Apparel & Accessory Stores
- **Fiscal year end (MM-DD):** 02-03
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/ZUMZ

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Zumiez Inc
- **CIK:** 1,318,008 · **SIC:** 5600 (Retail-Apparel & Accessory Stores) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LineOfCredit

**Valuation**

| metric | value |
|---|---|
| price | 17.70 |
| mktcap | $298.6M |
| ev | $231.7M |
| ev_ebit | 13.6x |
| fcf | $42.4M |
| fcf_yield | 14.2% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 5.6% |
| net_debt | -$66.9M |
| net_debt_ebit | -3.9x |
| cash | $66.9M |
| ltd | $0.00 |
| equity | $305.9M |
| ltd_tag | LineOfCredit |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $929.1M |
| revenue_prior | $889.2M |
| rev_growth | 4.5% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $17.0M |
| net_income | $13.4M |
| cfo | $53.5M |
| capex | $11.1M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -5.1% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 16,872,215 |
| shares_py | 17,770,640 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 11.6% |
| r6m | -27.4% |
| off_52w_high | -42.2% |
| adv20 | $3.8M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.81 |
| r_ev_ebit | 0.63 |
| r_roic | 0.54 |
| r_rev_growth | 0.51 |
| r_buyback | 0.88 |
| score | 0.73 |

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
| rank | 43 |

**Screen rationale:** top-quartile FCF yield 14.2%; buying back stock -5.1%; net cash; 12-1 momentum 11.6%


## 3. Share count trend

- Shares outstanding: **16,872,215** (CY2026Q2I) vs **17,770,640** prior year (CY2025Q2I)
- Change: **-5.1%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-01** — Item 5.02 (officer / director change or comp arrangement): On June 30, 2026, Mr. Christopher C. Work, Chief Financial Officer of Zumiez Inc. (the "Company"), gave notice of his decision to step down from his position with the Company.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 15,974 sh / $334,532 -> net $-334,532 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 15 (open-market buys 0, sales 5).

| code | rows |
|---|---|
| A | 6 |
| F | 2 |
| M | 2 |
| S | 5 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-06-04_2-02-results.md)

_Extraction: started at the first release heading, 'First Quarter Comparable Sales Increased 4.0%'; skipped 8 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - PRESS RELEASE (exh_991.htm)

First Quarter Comparable Sales Increased 4.0%

Operating Loss Improved to $15.2 million

LYNNWOOD, Wash., June 04, 2026 (GLOBE NEWSWIRE) -- Zumiez Inc. (NASDAQ: ZUMZ) a leading specialty retailer of apparel, footwear, equipment and accessories for young men and women, today reported results for the first quarter ended May 2, 2026.

Net sales for the first quarter ended May 2, 2026 (13 weeks) increased 4.9% to $193.3 million from $184.3 million in the first quarter ended May 3, 2025 (13 weeks). Comparable sales for the thirteen weeks ended May 2, 2026, increased 4.0%. Net loss in the first quarter of fiscal 2026 was $13.3 million, or $0.82 per share, compared to a net loss of $14.3 million, or $0.79 per share, in the first quarter of the prior fiscal year. The first quarter of 2025 was negatively impacted by $2.9 million, or approximately $0.13 per share related to the settlement of a wage and hours lawsuit in California. Though operating income and net income improved year-over-year, EPS was down slightly given that the Company was in a loss position in the first quarter and reduced share counts through its share buyback programs.

On May 2, 2026, the Company had cash and current marketable securities of $124.2 million compared to cash and current marketable securities of $101.0 million on May 3, 2025. The increase was primarily driven by $47.5 million of cash flow from operations and the release of $3.0 million in restricted cash, partially offset by $19.0 million related to share repurchases and $10.5 million of capital expenditures. The Company repurchased 0.3 million shares during the first quarter of 2026 at an average cost including commission of $23.56 per share and a total cost of $6.2 million.

"We continue to make important progress towards sustained profitable growth," said Rick Brooks, Chief Executive Officer of Zumiez Inc. "First quarter comparable sales increased mid-single digits for the second consecutive year driven by ongoing strength in our North American business and strong mid-single digit comps in Europe. Sales trends in the U.S. remained nicely positive during the quarter despite increasing pressure on consumers, underscoring the success of our recent merchandise assortments and customer experience initiatives. While still in the early innings, the work we are doing to replicate our full-price selling model in Europe is gaining traction, contributing to year-over-year improvements in sales and margin. Despite some softness in North America during the May period, we are encouraged that we have been able to grow sales and margin through the challenges in the macro environment and feel we are well positioned to capitalize during the key back-to-school and holiday seasons when the consumer has a reason to come out and shop."

May 2026 Sales

Net sales for the four-week period ended May 30, 2026, increased 0.1% compared to the four-week period ended May 31, 2025. Comparable sales for the four-week period ending May 30, 2026, decreased 0.1% from the comparable period in the prior year. From a regional perspective, comparable sales for North America decreased 1.5% and other international comparable sales increased 7.2%.

Fiscal 2026 Second Quarter Outlook

The Company is introducing guidance for the three months ending August 1, 2026. Net sales are projected to be in the range of $210 to $215 million. Earnings per share are expected to be between a loss of $0.23 and a loss of $0.08.

In fiscal 2026 the Company currently intends to open approximately 5 new stores all located in North America and close roughly 26 stores, including 20 in North America and 6 internationally.

Conference call Information

To access the conference call, please pre-register using this link (Registration Link) . Registrants will receive confirmation with dial-in details. The conference call will also be available to interested parties through a live webcast at https://ir.zumiez.com. To avoid delays, we encourage participants to dial into the conference call fifteen minutes ahead of the scheduled start time. A replay of the webcast will also be available for a limited time at https://ir.zumiez.com.

About Zumiez Inc.

Zumiez is a leading specialty retailer of apparel, footwear, accessories and hardgoods for young men and women who want to express their individuality through the fashion, music, art and culture of action sports, streetwear, and other unique lifestyles. As of May 30, 2026, we operated 715 stores, including 560 in the United States, 45 in Canada, 83 in Europe and 27 in Australia. We operate under the names Zumiez, Blue Tomato and Fast Times. Additionally, we operate ecommerce web sites at zumiez.com, zumiez.ca, blue-tomato.com and fasttimes.com.au.

Zumiez Inc.

(425) 551-1500, ext. 1337

Investor Contact:

ICR

Brendon Frey

(203) 682-8200

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-12_item7_mdna.md)

_Extraction: started at 'Results of Operations'._

Results of Operations

The following table presents selected items on the consolidated statements of income (loss) as a percent of net sales:

Fiscal 2025 | Fiscal 2024 | Fiscal 2023
Net sales | 100.0 | % | 100.0 | % | 100.0 | %
Cost of goods sold | 64.2 | % | 65.9 | % | 67.9 | %
Gross profit | 35.8 | % | 34.1 | % | 32.1 | %
Selling, general and administrative expenses | 34.0 | % | 33.9 | % | 39.5 | %
Operating profit (loss) | 1.8 | % | 0.2 | % | -7.4 | %
Interest and other income, net | 0.8 | % | 0.3 | % | 0.3 | %
Earnings (loss) before income taxes | 2.6 | % | 0.5 | % | -7.1 | %
Provision for income taxes | 1.2 | % | 0.7 | % | 0.1 | %
Net income (loss) | 1.4 | % | -0.2 | % | -7.2 | %

Fiscal 2025 Results Compared With Fiscal 2024

Net Sales

Net sales were $929.1 million for fiscal 2025 compared to $889.2 million for fiscal 2024, an increase of $39.9 million or 4.5%. The increase in sales was primarily driven by a 4.3% increase in comparable sales, reflecting strength in key brands and fashion trends in the market, and was partially offset by the net closure of 11 stores subsequent to fiscal 2024.

Comparable sales increased 4.3% driven by an increase in dollars per transaction and partially offset by a decrease in transactions. The increase in dollars per transaction was driven by an increase in average unit retail, and an increase in units per transaction. For the year, our largest growth in comparable sales was in our women's category, followed by men's, hardgoods, and accessories. Footwear was the only category with a decrease in comparable sales.

By region, North America sales increased $37.1 million or 5.1% and other international sales increased $2.8 million or 1.7% during fiscal 2025 compared to fiscal 2024. Net sales for the year ended January 31, 2026, included a $9.6 million increase due to the change in foreign exchange rates, which consisted of a $10.0 million increase in Europe, partially offset by a decrease of $0.3 million in Canada, and a decrease of $0.1 million in Australia. Excluding the impact of changes in foreign exchange rates, North America sales increased $37.4 million or 5.2% and other international sales decreased $7.1 million or 4.2% during fiscal 2025 compared to fiscal 2024.

Gross Profit

Gross profit was $332.5 million for fiscal 2025 compared to $303.0 million for fiscal 2024, an increase of $29.5 million, or 9.7%. As a percentage of net sales, gross profit increased 170 basis points in fiscal 2025 to 35.8%. The increase was primarily driven by a 90 basis point improvement in product margin (defined as net sales minus cost of goods sold excluding shrinkage, buying, occupancy, distribution and warehousing costs and freight costs for store merchandise transfers), 70 basis points of leverage in store occupancy costs related to both higher sales and closure of underperforming stores.

Selling, General and Administrative Expenses

Selling, general and administrative ("SG&A") expenses were $315.5 million for fiscal 2025 compared to $301.1 million for fiscal 2024, an increase of $14.4 million, or 4.8%. SG&A expenses as a percent of net sales increased 10 basis points in fiscal 2025 to 34.0%. The increase was primarily driven by 50 basis point increase in annual incentive compensation due to improved operating results, 40 basis point increase due to $3.6 million of wage and hour litigation settlements in California, partially offset by 60 basis points in non-wage store operating costs related to closure of store year over year, and 30 basis points of efficiencies in store wages due to higher sales and closure of low performing stores at the end of fiscal 2024.

Net Income (Loss)

Net income for fiscal 2025 was $13.4 million, or $0.78 per diluted share, compared with net loss of $1.7 million, or $0.09 per diluted share, for fiscal 2024. Our effective income tax rate for fiscal 2025 was 44.4% compared to 142.0% for fiscal 2024. The change in effective income tax rate for fiscal 2025 compared to fiscal 2024 was primarily driven by improved operating results and the allocation of foreign losses in certain jurisdictions, which are subject to a valuation allowance. The introduction of new valuation allowances in certain jurisdictions contributed $4.2 million of income tax expense, while continued losses in jurisdictions with established valuation allowances added $5.0 million, resulting in a $9.2 million total income tax expense for fiscal 2025 compared to $5.1 million in fiscal 2024.

Liquidity and Capital Resources

Our cash requirements are subject to change as business conditions warrant and opportunities arise. Our primary uses of cash are for operational expenditures, inventory purchases, common stock repurchases and capital investments, including new stores, store remodels, store relocations, store fixtures and ongoing infrastructure improvements. Historically, our main source of liquidity has been cash flows from operations.

The significant components of our working capital are inventories and liquid assets such as cash, cash equivalents, current marketable securities and receivables, reduced by accounts payable and accrued expenses. Our working capital position benefits from the fact that we generally collect cash from sales to customers the same day or within several days of the related sale, while we typically have longer payment terms with our vendors.

At January 31, 2026 and February 1, 2025, cash, cash equivalents, and current marketable securities were $160.6 million and $147.6 million, respectively. Working capital, the excess of current assets over current liabilities, was $168.5 million at the end of fiscal 2025, an increase of 0.9% from $166.9 million at the end of fiscal 2024. The increase in cash, cash equivalents, and current marketable securities in fiscal 2025 was primarily due to cash provided by operating activities of $53.5 million, net proceeds from sale of marketable securities amounting to $4.7 million, partially offset by the $38.3 million repurchase of common stock, and capital expenditures of $11.1 million related to the opening of 6 new stores, 3 store remodels, website enhancements, and other improvements.

The following table summarizes our cash flows from operating, investing and financing activities (in thousands):

Fiscal 2025 | Fiscal 2024 | Fiscal 2023
Net cash provided by (used in)
Operating activities | 53,474 | 20,701 | 14,755
Investing activities | (6,391 | 32,602 | (8,548
Financing activities | (37,344 | (24,600 | 704
Effect of exchange rate changes on cash and cash equivalents | 2,845 | (1,458 | (1,080
Net change in cash, cash equivalents, and restricted cash | 12,584 | 27,245 | 5,831

Operating Activities

Net cash provided by operating activities increased by $32.8 million in fiscal 2025 to $53.5 million cash provided by operating activities from $20.7 million cash provided by operating activities in fiscal 2024. Net cash provided by operating activities increased by $5.9 million in fiscal 2024 to $20.7 million cash provided by operating activities from $14.8 million cash provided by operating activities in fiscal 2023. Our operating cash flows result primarily from cash received from our customers, offset by cash payments we make for inventory, employee compensation, store occupancy expenses and other operational expenditures. Cash received from our customers generally corresponds to our net sales. Because our customers primarily use credit and debit cards or cash to buy from us, our receivables from customers settle quickly. Changes to our operating cash flows have historically been driven primarily by changes in operating income, which is impacted by changes to non-cash items such as depreciation, impairment, amortization and accretion, deferred taxes, and changes to the components of working capital.

Investing Activities

Net cash used in investing activities was $6.4 million in fiscal 2025 related to $11.1 million of capital expenditures primarily for new stores openings and existing store remodels or relocations, partially offset by $4.7 million in net proceeds from sale of marketable securities. Net cash provided by investing activities was $32.6 million in fiscal 2024 related to $15.0 million of capital expenditures primarily for new stores openings and existing store remodels or relocations, partially offset by $47.6 million in net proceeds from sale of marketable securities. Net cash used in investing activities was $8.5 million in fiscal 2023 related to $20.4 million of capital expenditures primarily for new store openings and existing store remodels or relocations partially offset by $11.7 million in net sales of marketable securities.

Financing Activities

Net cash used in financing activities in fiscal 2025 was $37.3 million, related to $38.3 million used in the repurchase of common stock, partially offset by $0.9 million in net proceeds from the issuance and exercise of stock-based awards. Net cash used in financing activities in fiscal 2024 was $24.6 million, related $25.2 million used in the repurchase of common stock partially offset by $0.6 million in proceeds from the issuance and exercise of stock-based awards. Net cash provided by financing activities in fiscal 2023 was $0.7 million related to proceeds from the issuance and exercise of stock-based awards.

Capital Expenditures

Our capital requirements include construction and fixture costs related to the opening of new stores and remodel and relocation expenditures for existing stores. Future capital requirements will depend on many factors, including the pace of new store openings, the availability of suitable locations for new stores and the nature of arrangements negotiated with landlords. In that regard, our net investment to open a new store has varied significantly in the past due to a number of factors, including the geographic location and size of the new store, and is likely to vary significantly in the future.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-12_item1_business.md)

Item 1. BUSINESS

Zumiez Inc., including its wholly-owned subsidiaries, is a leading specialty retailer of apparel, footwear, accessories and hardgoods for young men and women who want to express their individuality through the fashion, music, art and culture of action sports, streetwear and other unique lifestyles. Zumiez Inc. was formed in August 1978 and is a Washington State corporation.

We operate under the names Zumiez, Blue Tomato and Fast Times. We operate ecommerce websites at zumiez.com, zumiez.ca, blue-tomato.com and fasttimes.com.au. At January 31, 2026, we operated 719 stores; 561 in the United States ("U.S."), 45 in Canada, 85 in Europe and 28 in Australia.

We acquired Blue Tomato in fiscal 2012. Blue Tomato is one of the leading European specialty retailers of apparel, footwear, accessories and hardgoods. We acquired Fast Times Skateboarding ("Fast Times") in fiscal 2016. Fast Times is an Australian leading specialty retailer of hardgoods, accessories, apparel and footwear.

We employ a sales strategy that integrates our stores with our ecommerce platform to serve our customers. There is significant interaction between our store sales and our ecommerce sales channels, and we believe that they are utilized in tandem by our customers. Our selling platforms bring the look and feel of an independent specialty shop through a distinctive store environment and high-energy sales personnel. We seek to staff our stores with store associates who are knowledgeable users of our products, which we believe provides our customers with enhanced customer service and supplements our ability to identify and react quickly to emerging trends and fashions. We design our selling platforms to appeal to teenagers and young adults and to serve as a destination for our customers. We believe that our distinctive selling platforms and compelling economics will provide continued opportunities for growth in both new and existing markets.

We believe that our customers desire authentic merchandise and fashion that is rooted in the fashion, music, art and culture of action sports, streetwear and other unique lifestyles to express their individuality. We strive to keep our merchandising mix fresh by continuously introducing new brands, styles and categories of product. Our focus on a diverse collection of brands allows us to quickly adjust to changing fashion trends. We believe that our strategic mix of apparel, footwear, accessories and hardgoods, including skateboards, snowboards, bindings, components and other equipment, allows us to strengthen the potential of the brands we sell and helps to affirm our credibility with our customers. In addition, we supplement our merchandise mix with a select offering of private label apparel and products as a value proposition that we believe complements our overall merchandise selection.

Competitive Strengths

We believe that the following competitive strengths differentiate us from our competitors and are critical to our continuing success.

Attractive Lifestyle Retailing Concept . We target a large population of young men and women, many of whom we believe are attracted to action sports, streetwear and other unique lifestyles and desire to express their personal independence and style through the apparel, footwear and accessories they wear and the equipment they use. We believe we have developed a brand image that our customers view as consistent with their attitudes, fashion tastes and identity and differentiates us in our market.

Differentiated Merchandising Strategy . We have created a highly differentiated global retailing concept by offering an extensive selection of current and relevant lifestyle brands encompassing apparel, footwear, accessories and hardgoods. The breadth of merchandise offered through our sales channels exceeds that offered by many of our competitors and includes some brands and products that are available only from us. Many of our customers desire to update their wardrobes and equipment as fashion trends evolve or the season dictates, providing us the opportunity to shift our merchandise selection seasonally. We believe that our ability to quickly recognize changing brand and style preferences and transition our merchandise offerings allows us to continually provide a compelling offering to our customers.

Deep-rooted Culture . We believe our culture and brand image enable us to successfully attract and retain high quality employees who are passionate and knowledgeable about the products we sell. We place great emphasis on customer service and satisfaction, and we have made this a defining feature of our corporate culture. To preserve our culture, we strive to promote from within and we provide our employees with the knowledge and tools to succeed through our comprehensive training programs and the empowerment to manage their stores to meet localized customer demand.

Distinctive Customer Experience . We strive to provide a convenient shopping environment that is appealing and clearly communicates our distinct brand image. We seek to integrate our store and digital shopping experiences to serve our customers whenever, wherever and however they choose to engage with us. We seek to attract knowledgeable sale associates who identify with our brand and are able to offer superior customer service, advice and product expertise. We believe that our distinctive shopping experience enhances our image as a leading source for apparel and equipment for action sports, streetwear and other unique lifestyles.

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

**Present:** meta.json, form4_summary.md, 8-K_2026-06-04_2-02-results.md, 10-K_2026-03-12_item7_mdna.md, 10-K_2026-03-12_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
