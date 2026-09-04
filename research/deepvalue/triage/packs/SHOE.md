# Triage pack — SHOE · SHOE STATION GROUP INC

_Generated 2026-09-04 15:12 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** SHOE · **Name:** SHOE STATION GROUP INC
- **CIK:** 0000895447
- **SIC:** 5661 — Retail-Shoe Stores
- **Fiscal year end (MM-DD):** 01-30
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/SHOE

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** SHOE STATION GROUP INC
- **CIK:** 895,447 · **SIC:** 5661 (Retail-Shoe Stores) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 13.65 |
| mktcap | $370.6M |
| ev | $254.5M |
| ev_ebit | 3.8x |
| fcf | $26.6M |
| fcf_yield | 7.2% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 9.5% |
| net_debt | -$116.1M |
| net_debt_ebit | -1.7x |
| cash | $116.1M |
| ltd | $0.00 |
| equity | $673.4M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $1.1B |
| revenue_prior | $1.2B |
| rev_growth | -5.6% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $66.8M |
| net_income | $52.3M |
| cfo | $71.3M |
| capex | $44.7M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -0.7% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 27,151,308 |
| shares_py | 27,335,733 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -24.8% |
| r6m | -29.8% |
| off_52w_high | -45.3% |
| adv20 | $10.5M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.60 |
| r_ev_ebit | 0.95 |
| r_roic | 0.69 |
| r_rev_growth | 0.17 |
| r_buyback | 0.72 |
| score | 0.63 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q1I |
| shares_period | CY2026Q2I |
| shares_py_period | CY2025Q2I |
| capex_missing | False |
| ltd_missing | True |

**Other screen columns**

| metric | value |
|---|---|
| rank | 114 |

**Screen rationale:** cheap at 3.8x EV/EBIT; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **27,151,308** (CY2026Q2I) vs **27,335,733** prior year (CY2025Q2I)
- Change: **-0.7%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-03-09** — Item 5.02 (officer / director change or comp arrangement): Compensation for Interim President and Chief Executive Officer

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 31,000 sh / $500,030 vs sells 0 sh / $0 -> net $500,030 (BUYING).
Distinct insiders buying (code P): 1. Largest buy: JACKSON W KERRY bought 31,000 sh @ $16.13 ($500,030) on 2026-04-02.

Form 4 filings parsed: 12; transaction rows: 14 (open-market buys 1, sales 0).

| code | rows |
|---|---|
| A | 6 |
| F | 3 |
| G | 4 |
| P | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-05-21_2-02-results.md)

_Extraction: started at the first release heading, 'SHOE CARNIVAL REPORTS FIRST QUARTER 2026 RESULTS'; skipped 43 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (scvl-ex99_1.htm)

SHOE CARNIVAL REPORTS FIRST QUARTER 2026 RESULTS

May 21, 2026

FOR IMMEDIATE RELEASE

FORT MILL, S.C. - Shoe Carnival, Inc. (Nasdaq: SCVL) (the "Company"), a leading omnichannel retailer of footwear and accessories for the family, today reported results for the first quarter ended May 2, 2026.

First Quarter 2026 Highlights

•
Net sales of $270.7 million, compared to $277.7 million in the first quarter of 2025.

•
Shoe Carnival banner net sales declined 2.2 percent, a meaningful improvement compared to the trends experienced through Fiscal 2025; Shoe Station banner net sales declined 3.1 percent.

•
Gross profit margin of 33.3 percent, compared to 34.5 percent in the first quarter of 2025.

•
GAAP diluted loss per share ("EPS") of $(0.21); adjusted diluted earnings per share ("Adjusted EPS") (1) of $0.23, consistent with consensus analyst expectations (non-GAAP), which excludes charges associated with the previously announced Chief Executive Officer transition ("CEO Transition") and the completion of a strategic review of the Company's rebanner program.

•
Pretax charges of $13.6 million ($11.9 million after-tax, or $0.43 per diluted share) recorded during the quarter, comprised of $5.3 million related to the CEO Transition and $8.3 million related to the strategic review, including impairment of store locations and write-offs of rebanner-related and corporate fixed assets.

•
Cash, cash equivalents, and marketable securities of $129.3 million at quarter-end, an increase of $36.4 million compared to the prior-year period; the Company ended the first quarter of 2026 debt-free.

•
Repurchased 390,492 shares of common stock during the first quarter of 2026 for approximately $7.0 million.

(1) A description of non-GAAP Adjusted EPS and a reconciliation of non-GAAP Adjusted EPS to the corresponding GAAP measure is provided at the end of this press release .

"Since returning to the Chief Executive Officer role in late February, I have worked with our Board and management team to complete a comprehensive review of the Company's strategic direction and capital deployment," said Cliff Sifford, Interim President and Chief Executive Officer.

"Our review confirmed that the Shoe Carnival and Shoe Station banners each serve distinct consumer segments, and that the Company is best positioned to operate both banners as permanent, independent components of our portfolio. While there is more work to do, I am pleased that our first quarter results came in within the range of consensus analyst expectations on the key financial metrics, with sales modestly ahead of consensus and Adjusted EPS matching consensus. The Shoe Carnival banner narrowed its year-over-year sales decline meaningfully compared to Fiscal 2025 trends. In addition, we continue to feel confident about growth opportunities for the Shoe Station banner - both through new

store growth in markets that serve the target consumer segment and rebannering of select Shoe Carnival locations that meet the criteria for conversion to Shoe Station."

"Our underlying business delivered Adjusted EPS in line with consensus expectations during a quarter of significant strategic transition. We ended the quarter with $129 million in cash and marketable securities and no debt, and we returned $7 million to shareholders through share repurchases. We are reaffirming our previously communicated Fiscal 2026 guidance, with the back-to-school and fall selling periods representing the bulk of our expected annual earnings opportunity. We intend to manage Fiscal 2026 with disciplined capital deployment, continued progress on inventory normalization, and preparation for opening new stores in Fiscal 2027," concluded Mr. Sifford.

First Quarter 2026 Operating Results

Net sales in the first quarter of 2026 were $270.7 million compared to $277.7 million in the first quarter of 2025. Comparable store sales declined 2.1 percent.

By banner:

•
Shoe Carnival net sales were $177.3 million, representing 65 percent of total net sales, and declined 2.2 percent, inclusive of a comparable store net sales decline of 1.7 percent. This was an improvement compared to mid-to-high single digit quarterly declines throughout Fiscal 2025.

•
Shoe Station net sales were $93.4 million, representing 35 percent of total net sales, and declined 3.1 percent, inclusive of a comparable store net sales decline of 2.9 percent. Improved trends in rebanner store sales were more than offset by slower growth from the Shoe Station e-commerce sales channel.

Gross profit margin in the first quarter of 2026 was 33.3 percent, a decrease of 120 basis points compared to the first quarter of 2025. Merchandise margin decreased 140 basis points primarily driven by increased promotional activity and higher e-commerce-related shipping costs. The decrease was partially offset by 20 basis points from primarily lower buying, distribution and occupancy costs.

Selling, general and administrative expenses ("SG&A") on a GAAP basis increased $12.3 million compared to the first quarter of 2025. Non-GAAP adjusted SG&A ("Adjusted SG&A"), which excludes non-recurring charges of $13.6 million in the first quarter of 2026 related the CEO Transition and the Company's strategic review of its rebanner strategy, decreased $1.3 million.

Income tax expense in the first quarter of 2026 was $0.6 million and was impacted by nondeductible CEO severance payments that increased income tax expense by approximately $1.6 million. The Company's effective tax rate in the first quarter of 2026 was (11.2)% compared to 28.1% in the first quarter of 2025. The Company's non-GAAP adjusted effective tax rate ("Adjusted Tax Rate") in the first quarter of 2026, which excludes the impacts related to the CEO Transition and the strategic review, was 27.0 percent.

The GAAP net loss for the first quarter of 2026 was $(5.6) million, or $(0.21) per diluted share. Excluding the impacts from the non-recurring charges recorded in the quarter, non-GAAP adjusted net income ("Adjusted Net Income") and Adjusted EPS were $6.2 million and $0.23 per diluted share, respectively, compared to net income of $9.3 million and EPS of $0.34 in the first quarter of 2025.

Descriptions of Adjusted Net Income, Adjusted EPS, Adjusted SG&A and Adjusted Tax Rate, and reconciliations to the corresponding GAAP measures, are provided at the end of this press release.

Capital Management and Cash Flow

Fiscal 2025 marked the 21st consecutive fiscal year the Company ended with no debt, fully funding operations and strategic investments from operating cash flow and cash reserves. The first quarter of

2026 was also debt-free. At the end of the first quarter of 2026, the Company held approximately $129.3 million in cash, cash equivalents, and marketable securities, an increase of 39 percent compared to the end of the first quarter of 2025. Cash flow from operations increased $32.7 million while capital expenditures declined $2.9 million.

Merchandise inventories at the end of first quarter 2026 were $417.2 million, down $11.2 million compared to the end of the first quarter of 2025. The Company continues to expect inventory declines of $50 to $65 million by the end of Fiscal 2026 compared to the end of Fiscal 2025.

Dividend and Share Repurchase Program

During the first quarter of 2026, the Company returned approximately $12 million to shareholders through dividends and share repurchases. The $5 million in dividend payments in the first quarter of 2026 were paid at an increased rate of $0.17 per share, up 13.3 percent compared to the first quarter of 2025. This increase represented the 12th consecutive year the Company increased its quarterly dividend rate. The new Fiscal 2026 annualized rate represents a compounded annual growth rate of approximately 15.5 percent over the past 12 years. The Company has now paid a dividend for 56 consecutive quarters.

Approximately $7 million of shares were repurchased during the first quarter of 2026. As of May 2, 2026, $43 million remained available under the Company's share repurchase authorization.

Fiscal 2026 Guidance

The Company is reaffirming its previously communicated Fiscal 2026 guidance, which continues to contemplate:

•
Net sales of $1.125 billion to $1.147 billion, representing a range of down 1 percent to up 1 percent versus Fiscal 2025;

•
Adjusted EPS of $1.40 to $1.60;

•
Gross profit margin of approximately 34 percent, representing approximately 260 basis points of compression versus Fiscal 2025;

•
Reductions in Adjusted SG&A of $12 to $14 million versus Fiscal 2025; and

•
An Adjusted Tax Rate of approximately 26 percent.

The Company's Adjusted EPS, Adjusted SG&A and Adjusted Tax Rate guidance excludes the impact of the CEO Transition costs previously identified and the strategic review charges recorded during the first quarter of 2026. A reconciliation of the Adjusted EPS guidance to the corresponding GAAP measure is provided in a table at the end of this press release. Please refer to "Note Regarding Forward-Looking Non-GAAP Measures" at the end of this press release for further information regarding the reconciliation of Adjusted SG&A and Adjusted Tax Rate guidance.

Annual Shareholder Meeting

As previously announced, the Company will hold its Annual Meeting of Shareholders at 11:00 a.m. Eastern Time on June 10, 2026. Information about the annual meeting and related material, including the Company's proxy statement and annual report, can be found on the Company's website.

Conference Call

Today, at 9:00 a.m. Eastern Time, the Company will host a conference call to discuss its first quarter results. Participants can listen to the live webcast of the call by visiting Shoe Carnival's Investors webpage at www.shoecarnival.com. While the question-and-answer session will be available to all listeners, questions from the audience will be limited to institutional analysts and investors. A replay of

the webcast will be available on the Company's website shortly after the conclusion of the conference call and will be archived for one year.

About Shoe Carnival

Shoe Carnival, Inc. is one of the nation's largest omnichannel family footwear retailers, offering a broad assortment of dress, casual and athletic footwear for men, women and children with emphasis on national name brands. As of May 21, 2026, the Company operated 426 stores in 35 states and Puerto Rico under its Shoe Carnival and Shoe Station banners and offers shopping at www.shoecarnival.com and www.shoestation.com. Headquartered in Fort Mill, SC, and with distribution and support operations located in Evansville, IN, Shoe Carnival, Inc. trades on The Nasdaq Stock Market LLC under the symbol SCVL.

Press releases and annual reports are available on the Company's website at www.shoecarnival.com.

Contact Information

W. Kerry Jackson

Chief Financial Officer

(812) 867-4034

scvlir@scvl.com

SHOE CARNIVAL, INC.

CONDENSED CONSOLIDATED BALANCE SHEETS

(In thousands)

(Unaudited)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-26_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview of Our Business

Shoe Carnival, Inc. is one of the nation's largest omnichannel sellers of footwear for the family, and our goal is to be the leading family footwear retailer in the United States. Our product assortment, whether shopping in a physical store or through our e-commerce sales channel, is primarily branded footwear and includes dress and casual shoes, sandals, boots, work, and a wide assortment of athletic shoes. We carry shoes in two general categories – athletics and non-athletics with subcategories for men's, women's and children's and we also carry certain accessories. In addition to our physical stores, through our e-commerce sales channel, customers can purchase the same assortment of merchandise in all categories of footwear with expanded options in certain instances. During Fiscal 2025, we operated two banners: Shoe Carnival and Shoe Station. For a description of these two banners, including the in-store environment, target customer and product assortment, see PART I, ITEM 1 of this Annual Report on Form 10-K.

As of our Fiscal 2025 year end, we operated 426 stores across 35 states and Puerto Rico, consisting of 144 Shoe Station locations and 282 Shoe Carnival locations. As more fully described in PART I, ITEM 1 of this Annual Report on Form 10-K, at the end of Fiscal 2025, Shoe Station bannered stores represented approximately 34% of our total store fleet, compared to approximately 10% at the end of Fiscal 2024. During Fiscal 2025, we rebannered 101 stores into Shoe Station stores, consisting of 73 Shoe Carnival stores and all 28 Rogan's stores.

On November 13, 2025, we announced that our Board of Directors unanimously approved changing our corporate name to Shoe Station Group, Inc., subject to shareholder approval at our Annual Meeting of Shareholders in June 2026. That proposed name change remains on the June 2026 agenda. The proposed corporate name change to Shoe Station Group, Inc. reflects the Board's conviction that the Shoe Station concept is our primary long-term growth vehicle.

Store Portfolio and Our Banner Strategy

The following tables set forth our physical store count for Fiscal 2025 and Fiscal 2024, as impacted by store rebanners, acquisitions, store openings and store closures.

January 31, 2026
Beginning | Permanently | End of
Banner | of Period | Opened | Acquired | Closed | Rebannered | Period
Shoe Carnival | 360 | 0 | 0 | (5 | (73 | 282
Shoe Station | 42 | 1 | 0 | 0 | 101 | 144
Rogan's | 28 | 0 | 0 | 0 | (28 | 0

February 1, 2025
Beginning | Permanently | End of
Banner | of Period | Opened | Acquired | Closed | Rebannered | Period
Shoe Carnival | 372 | 0 | 0 | (2 | (10 | 360
Shoe Station | 28 | 4 | 0 | 0 | 10 | 42
Rogan's | 0 | 0 | 28 | 0 | 0 | 28

As stated above, during Fiscal 2025, we rebannerd 101 stores into Shoe Station stores. Over time this rebanner strategy has evolved. Previous expectations were that approximately 70 additional stores would rebanner before Back-to-School in Fiscal 2026, with the Shoe Station stores then representing 51% of the current store fleet, and that over 90% of our fleet would operate as a Shoe Station store by the end of Fiscal 2028, with remaining locations to be evaluated for potential rebannering, outlet repositioning, or closure. This transition to substantially all Shoe Station stores was expected to generate both inventory reductions, as Shoe Station's merchandising model requires less inventory per store, as well as cost savings from reduced dual-brand complexity across merchandising, marketing, systems, supply chain and back office.

In evaluating the performance of the 101 stores that were rebannered in Fiscal 2025, particularly Net Sales in the second-half of Fiscal 2025, we observed that, while Shoe Station's e-commerce results have been a meaningful contributor to banner-level sales growth, demonstrating strong consumer response to the Shoe Station brand and assortment online, there was significant variability in in-store sales performance across rebannered locations, with some stores performing well and others not achieving anticipated results.

As a result, we made the strategic decision to slow the pace of store rebanners in Fiscal 2026 from previously announced timelines to allow time to identify which consumer demographics are responding most favorably to the Shoe Station format, to determine which marketing channels are most effective in driving new customer acquisition, and to refine product mix in rebannered stores to improve in-store conversion. We now expect to rebanner approximately 21 stores during the first half of Fiscal 2026 while this evaluation is conducted.

The Shoe Station banner is expected to continue as our primary growth banner as we leverage our CRM customer data to identify opportunities both within our current markets as well as new markets outside of our current footprint that are best suited for the Shoe Station format.

However, in markets where Shoe Carnival has historically been a dominant family footwear retailer, those stores will continue to operate under the Shoe Carnival banner. The Shoe Carnival banner continues to serve an important customer base in a meaningful number of locations, and we expect to manage both banners accordingly.

Net Sales by Banner

For the past three fiscal years, Shoe Station has been a market leader in the Southeast, and, according to our view of available industry data, Shoe Station has been the fastest growing retailer in our industry in terms of Net Sales growth. During the same period, our Shoe Carnival banner and the family footwear industry experienced comparable stores Net Sales declines.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The following table sets forth our results of operations expressed as a percentage of Net Sales for the following fiscal years:

2025 | 2024 | 2023
Net sales | 100.0 | % | 100.0 | % | 100.0 | %
Cost of sales (including buying, distribution, and occupancy costs) | 63.4 | 64.4 | 64.2
Gross profit | 36.6 | 35.6 | 35.8
Selling, general and administrative expenses | 30.7 | 28.0 | 27.8
Operating income | 5.9 | 7.6 | 8.0
Interest and other income | (0.3 | (0.5 | (0.2
Interest expense | 0.0 | 0.0 | 0.0
Income before income taxes | 6.2 | 8.1 | 8.2
Income tax expense | 1.6 | 2.0 | 2.0
Net income | 4.6 | % | 6.1 | % | 6.2 | %

Fiscal 2025 Compared to Fiscal 2024

Net Sales

Net Sales were $1.135 billion during Fiscal 2025, a decrease of $67.6 million, or 5.6%, compared to Fiscal 2024. The decrease was primarily due to a 7.7% Net Sales decline at our Shoe Carnival banner, as we maintained pricing discipline despite pressure on lower-income consumers and reduced promotional marketing. This decrease was partially offset by continued growth from our Shoe Station banner, which contributed a 2.7% increase in Net Sales compared to Fiscal 2024. Our 5.6% comparable stores Net Sales decline included an approximate 13% decrease in units sold, partially offset by pricing increases. Our Shoe Carnival banner comparable stores Net Sales declined high-single digits, while our Shoe Station banner comparable stores Net Sales increased low-single digits. E-commerce sales were approximately 10% of merchandise sales in both Fiscal 2025 and Fiscal 2024.

Gross Profit

Gross Profit was $415.2 million in Fiscal 2025, a decrease of $13.6 million compared to Fiscal 2024. Gross profit margin in Fiscal 2025 was 36.6% compared to 35.6% in Fiscal 2024. The 100 basis point increase in gross profit margin was driven by a 180 basis point increase in merchandise margin due to disciplined pricing, favorable mix shift toward Shoe Station's higher-income consumer, and deliberate inventory management decisions made in anticipation of tariff cost increases that are expected to fully impact Fiscal 2026. This increase was partially offset by 80 basis points from buying, distribution and occupancy costs, primarily due to deleveraging on lower Net Sales in Fiscal 2025 compared to Fiscal 2024.

Selling, General and Administrative Expenses

SG&A increased $10.8 million in Fiscal 2025 to $348.4 million compared to $337.6 million in Fiscal 2024. The increase was due primarily to expenses associated with our rebanner strategy, partially offset by decreases in selling expenses impacting our other stores in Fiscal 2025 compared to Fiscal 2024. As a percent of Net Sales, SG&A were 30.7% in Fiscal 2025 compared to 28.0% in Fiscal 2024, with the increase being due primarily to the rebanner costs incurred in Fiscal 2025, which increased SG&A as a percent of Net Sales by approximately two percentage points, and deleveraging from lower Net Sales outpacing cost control measures.

Interest and Other Income and Interest Expense

Changes in our Interest and Other Income and our Interest Expense decreased our Income Before Income Taxes by $2.7 million in Fiscal 2025 compared to Fiscal 2024. This decrease was primarily due to pandemic-related tax credits of $3.0 million recognized in Fiscal 2024 associated with our acquisition of Rogan's, partially offset by higher interest earned on invested cash balances.

Income Taxes

The effective income tax rate for Fiscal 2025 was 25.7% compared to 24.3% for Fiscal 2024. The higher effective tax rate in Fiscal 2025 compared to Fiscal 2024 was due to discrete adjustments related to share-settled equity awards and favorable impacts recognized in Fiscal 2024 associated with our acquisition of Rogan's.

Liquidity and Capital Resources

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-26_item1_business.md)

ITEM 1. BUSINESS

Our Company

Shoe Carnival, Inc. is one of the nation's largest omnichannel retailers of footwear and accessories for the family. Our goal is to be the leading family footwear retailer in the United States. We operate a retail-focused business model designed to deliver a differentiated footwear shopping experience featuring national name brands. Our omnichannel approach provides customers easy access to our broad assortment of branded footwear for athletics, daily activities, special events and work through the customer's preferred delivery channel.

We have a demonstrated track record of selling branded footwear, including Nike, Skechers, Crocs, adidas, Puma, HEYDUDE, HOKA, Birkenstock, Converse and Brooks, and of generating profits without incurring debt. We have been in operation for 47 years and have been subject to SEC reporting requirements as a public company since 1993. Since 1993, we have earned a profit in every fiscal year except 1995.

As part of our long-term growth strategy, we have invested, and will continue to invest, significantly in our rebanner strategy, acquisitions, our customer relationship management ("CRM") capabilities, our e-commerce infrastructure and modernization of our store fleet as key drivers of profitable growth.

As of our Fiscal 2025 year end, we operated 426 stores across 35 states and Puerto Rico, consisting of 144 Shoe Station locations and 282 Shoe Carnival locations. During Fiscal 2025, we initiated a Shoe Station rebanner growth strategy, which has evolved over time, as described below.

Our fiscal year is a 52/53 week year ending on the Saturday closest to January 31. Unless otherwise stated, references to years 2025, 2024 and 2023 relate to the fiscal years ended January 31, 2026 ("Fiscal 2025"), February 1, 2025 ("Fiscal 2024"), and February 3, 2024 ("Fiscal 2023"), respectively. Fiscal 2026 refers to our fiscal year ending January 30, 2027. Fiscal 2023 consisted of 53 weeks, while all other years presented and discussed consisted of 52 weeks.

References to "Shoe Station" and "Shoe Carnival" are to the individual store banners, not the entire Company. References to "we," "us," "our," and the "Company" in this Annual Report on Form 10-K refer to Shoe Carnival, Inc. and its subsidiaries. Shoe Carnival, Inc. is an Indiana corporation that was initially formed in Delaware in 1993 and reincorporated in Indiana in 1996.

References to the "SEC" refer to the United States Securities and Exchange Commission.

See PART II, ITEM 7, "Management's Discussion and Analysis of Financial Condition and Results of Operations" in this Annual Report on Form 10-K for additional information regarding the trends affecting our operating results.

Our Store Banners

As of our Fiscal 2025 year end, we operated 426 stores under two banners: Shoe Carnival and Shoe Station. The following sections describe each banner and its role in the Company's strategic direction.

Shoe Carnival

Our Shoe Carnival retail concept has developed over our 47-year history and is differentiated from our competitors by our distinctive, fun and promotional marketing efforts. Shoe Carnival stores combine competitive pricing with a high-energy in-store environment that encourages customer participation. Unique features of our Shoe Carnival store experience include upbeat music, opportunities for customers to spin our spin-n-win wheel and a mic-person who runs in-store specials. These specials include contests, games and hot deals of the moment to encourage customers to take immediate advantage of our special, in-store pricing.

Footwear in our Shoe Carnival physical stores is organized by category and brand, creating strong brand statements within the aisles. These brand statements are underscored by branded signage on endcaps and in-line signage throughout the store. Our signage may highlight a vendor's product offerings or sales promotions or may highlight seasonal or lifestyle statements by grouping similar footwear from multiple vendors.

Shoe Carnival's primary customers are moderate to low-income families. Our Shoe Carnival bannered stores serve families with children through moderate-income brands and a value-oriented selection, with entry-level price points.

As of our Fiscal 2025 year end, we operated 282 Shoe Carnival bannered stores located across 31 states and Puerto Rico and offered online shopping at www.shoecarnival.com.

Shoe Station

In Fiscal 2021, we acquired our first 21 Shoe Station stores. The Shoe Station banner and retail locations serve a broader base of footwear customer. Our Shoe Station concept targets a more affluent footwear customer than our Shoe Carnival banner and has a strong track record of capitalizing on emerging footwear fashion trends and introducing new brands that meet the needs of the target customer. While value-conscious, our view is that these customers are not totally driven by price. Shoe Station serves this demographic through a differentiated assortment of premium brands and an enhanced in-store experience.

Shoe Station stores feature a modern and approachable shopping environment designed around accessibility and ease of navigation. Product is presented in curated displays that allow customers to shop our merchandise with or without assistance from our staff. The product assortment in our Shoe Station bannered stores includes higher end athletics and non-athletics shoes and more accessories. Our Shoe Station bannered stores require approximately 20 to 25 percent less inventory per store, on average, compared to our Shoe Carnival bannered stores.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-26_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-26_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-26_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-05-21_2-02-results.md, 10-K_2026-03-26_item7_mdna.md, 10-K_2026-03-26_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
