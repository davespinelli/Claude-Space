# Triage pack — EBF · ENNIS, INC.

_Generated 2026-09-04 13:14 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** EBF · **Name:** ENNIS, INC.
- **CIK:** 0000033002
- **SIC:** 2761 — Manifold Business Forms
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/EBF

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** ENNIS, INC.
- **CIK:** 33,002 · **SIC:** 2761 (Manifold Business Forms) · **Exchange:** NYSE

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 21.30 |
| mktcap | $538.9M |
| ev | $489.8M |
| ev_ebit | 9.3x |
| fcf | $41.0M |
| fcf_yield | 7.6% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 15.9% |
| net_debt | -$49.1M |
| net_debt_ebit | -0.9x |
| cash | $49.1M |
| ltd | $0.00 |
| equity | $310.7M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $392.4M |
| revenue_prior | $394.6M |
| rev_growth | -0.6% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $52.7M |
| net_income | $42.6M |
| cfo | $52.7M |
| capex | $11.7M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -1.9% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 25,298,272 |
| shares_py | 25,795,161 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 28.5% |
| r6m | 2.8% |
| off_52w_high | -5.5% |
| adv20 | $3.4M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.62 |
| r_ev_ebit | 0.80 |
| r_roic | 0.82 |
| r_rev_growth | 0.33 |
| r_buyback | 0.79 |
| score | 0.72 |

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
| rank | 48 |

**Screen rationale:** cheap at 9.3x EV/EBIT; high ROIC 15.9%; buying back stock -1.9%; debt data missing (net cash unverified); 12-1 momentum 28.5%


## 3. Share count trend

- Shares outstanding: **25,298,272** (CY2026Q2I) vs **25,795,161** prior year (CY2025Q2I)
- Change: **-1.9%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-02 among the 3 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 15 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 10 |
| M | 5 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-06-22_2-02-results.md)

_Extraction: started at the first release heading, 'ENNIS, INC. REPORTS RESULTS FOR THE'; skipped 8 forward-looking-statement block(s); 5 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (ebf-ex99_1.htm)

ENNIS, INC. REPORTS RESULTS FOR THE

QUARTER ENDED MAY 31, 2026 AND DECLARES QUARTERLY DIVIDEND

Midlothian, TX. June 22, 2026 -- Ennis, Inc. (the "Company"), (NYSE: EBF), today reported financial results for the quarter ended May 31, 2026. Highlights include:

•
Revenues were $98.6 million for the current quarter, an increase of $1.4 million or 1.4% over the same quarter last year.

•
Earnings per diluted share for the current quarter were $0.39 as compared to $0.38 for the same quarter last year.

•
Gross profit margin for the quarter was 31.5% compared to 31.1% for the comparative quarter last year.

Financial Overview

The Company's revenues for the first quarter ended May 31, 2026 were $98.6 million compared to $97.2 million for the same quarter last year, an increase of 1.4%. Gross profit totaled $31.1 million, or 31.5%, as compared to $30.2 million, or 31.1% for the same quarter last year. The Company's gross profit margin improved sequentially from 29.2% for the fourth quarter ended in fiscal year 2026. Net earnings for the quarter were $9.9 million, or $0.39 per diluted share as compared to $9.8 million, or $0.38 per diluted share for the same quarter last year. Operating cash flow increased to $21.2 million compared to $8.0 million in the prior-year quarter, and cash balances increased to $49.1 million at May 31, 2026 from $34.6 million at February 28, 2026.

Keith Walters, Chairman, Chief Executive Officer and President, commented, "Our performance for the quarter met our expectations. Revenue increased 1.4% over the prior-year quarter, while gross profit margin improved to 31.5%, compared to 31.1% in the prior year and 29.2% in the fourth quarter of fiscal 2026. EBITDA increased to $18.0 million or 18.2% of sales, compared to $17.7 million, or 18.2% of sales, in the same quarter last year.

"Acquisitions completed during fiscal year 2026 contributed approximately $4.5 million in revenue during the quarter and positively impacted diluted earnings per share by $0.02, primarily reflecting non-comparable ownership periods relative to the prior-year quarter. We remain focused on realizing operational efficiencies and maintaining disciplined pricing practices across our businesses.

"Over the past year, we proactively positioned ourselves to address the closure of the sole domestic producer of carbonless paper by securing inventory and developing alternative supply sources. We are successfully transitioning to those suppliers and do not anticipate any disruption to customer service, product availability or product quality.

"Our financial position remains strong. During the quarter, cash increased to $49.1 million from $34.6 million at the end of fiscal year 2026, driven by operating cash flow of $21.2 million. We continue to operate with no debt and maintain ample liquidity to support operations, pursue acquisition opportunities and return capital to shareholders through our quarterly dividend.

"We are encouraged by our first quarter performance and believe our strong balance sheet, disciplined cost structure and acquisition strategy position us well for the remainder of fiscal year 2027."

Non-GAAP Reconciliations

To provide important supplemental information to both management and investors regarding financial and business trends used in assessing its results of operations, from time to time the Company reports the non-GAAP financial measure of EBITDA (EBITDA is calculated as net earnings before interest expense, tax expense, depreciation, and amortization). The Company may also report adjusted gross profit margin, adjusted earnings and adjusted diluted earnings per share, each of which is a non-GAAP financial measure.

Management believes that these non-GAAP financial measures provide useful information to investors as a supplement to reported GAAP financial information. Management reviews these non-GAAP financial measures on a regular basis and uses them to evaluate and manage the performance of the Company's operations. Other companies may calculate non-GAAP financial measures differently than the Company, which limits the usefulness of the Company's non-GAAP measures for comparison with these other companies. While management believes the Company's non-GAAP financial measures are useful in evaluating the Company, when this information is reported it should be considered as supplemental in nature and not as a substitute or an alternative for, or superior to, the related financial information prepared in accordance with GAAP. These measures should be evaluated only in conjunction with the Company's comparable GAAP financial measures.

The following table reconciles EBITDA, a non-GAAP financial measure, for the three-months ended May 31, 2026 and 2025 to the most comparable GAAP measure, net earnings (dollars in thousands).

Three months ended
May 31, | May 31,
2026 | 2025
Net earnings | 9,879 | 9,799
Income tax expense | 3,843 | 3,716
Depreciation and amortization | 4,239 | 4,183
EBITDA (non-GAAP) | 17,961 | 17,698
% of sales | 18.2 | % | 18.2 | %

In Other News

On June 19, 2026 the Board of Directors declared a quarterly cash dividend of 25.0 cents per share on the Company's common stock. The dividend is payable on August 10, 2026 to shareholders of record on July 10, 2026.

About Ennis

Founded in 1909, the Company is one of the largest private-label printed business product suppliers in the United States. Headquartered in Midlothian, Texas, Ennis has production and distribution facilities strategically located throughout the USA to serve the Company's national network of distributors. Ennis manufactures and sells business forms, other printed business products, printed and electronic media, integrated forms and labels, presentation products, flex-o-graphic printing, advertising specialties, internal bank forms, plastic cards, secure and negotiable documents, specialty packaging, direct mail, envelopes, tags and labels and other custom products. For more information, visit www.ennis.com .

Midlothian, Texas 76065

Phone: (972) 775-9801

Fax: (972) 775-9820

www.ennis.com

Three months ended
Condensed Consolidated Operating Results | May 31, | May 31,
2026 | 2025
Net Sales | 98,615 | 97,197
Cost of goods sold | 67,532 | 66,967
Gross profit | 31,083 | 30,230
Selling, general and administrative | 17,508 | 16,947
Gain from disposal of assets | (10 | —
Income from operations | 13,585 | 13,283
Other income | 137 | 232
Earnings before income taxes | 13,722 | 13,515
Income tax expense | 3,843 | 3,716
Net earnings | 9,879 | 9,799
Weighted average common shares outstanding
Basic | 25,363,246 | 25,956,639
Diluted | 25,521,039 | 26,021,247
Earnings per share
Basic | 0.39 | 0.38
Diluted | 0.39 | 0.38
May 31, | February 28,
Condensed Consolidated Balance Sheet Information | 2026 | 2026
Assets
Current Assets
Cash | 49,082 | 34,570
Accounts receivable, net | 34,756 | 37,983
Other receivables | 785 | 1,623
Inventories, net | 56,067 | 54,895
Prepaid expenses | 2,763 | 2,699
Total Current Assets | 143,453 | 131,770
Property, plant & equipment, net | 61,534 | 63,341
Operating lease right-of-use assets, net | 8,330 | 9,503
Goodwill and intangible assets, net | 143,338 | 145,418
Other assets | 6,863 | 6,879
Total Assets | 363,518 | 356,911
Liabilities and Shareholders' Equity
Current liabilities
Accounts payable | 15,251 | 14,291
Accrued expenses | 21,632 | 16,846
Current portion of operating lease liabilities | 3,801 | 4,244
Total Current Liabilities | 40,684 | 35,381
Other non-current liabilities | 12,169 | 12,798
Total liabilities | 52,853 | 48,179
Shareholders' Equity | 310,665 | 308,732
Total Liabilities and Shareholders' Equity | 363,518 | 356,911
Three months ended
May 31, | May 31,
Condensed Consolidated Cash Flow Information | 2026 | 2025
Cash provided by operating activities | 21,232 | 7,960
Cash used in investing activities | (342 | (30,799
Cash used in financing activities | (6,378 | (11,538
Change in cash | 14,512 | (34,377
Cash at beginning of period | 34,570 | 67,000
Cash at end of period | 49,082 | 32,623

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-05-08_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

The Company – Our management believes we are the largest provider of business forms, pressure-seal forms, labels, tags, envelopes, and presentation folders to independent distributors in the United States.

Our Business Challenges – Our industry continues to experience consolidation of traditional supply channels, ongoing product obsolescence, paper supplier capacity adjustments, and periodic pricing volatility and potential supply allocations resulting from demand and supply imbalance. Technology advances have enabled electronic document distribution, web-based hosting, digital printing and print-on-demand as viable and cost-effective alternatives to traditional custom-printed documents and customer communications. Improved equipment has become more accessible to both existing and new competitors. As a result, we face highly competitive conditions in an already mature, price-competitive print industry.

In addition to the risk factors discussed under the caption "Risk Factors" in Item 1A of this Annual Report, some of the key challenges of our business include the following:

Transformation of our portfolio of products – While traditional business documents remain essential to conducting business, many are being replaced through the use of lower-cost paper grades or imported products, or are being devalued by advances in digital technologies, resulting in continued declines in demand for a portion of our product line. Transforming our product offerings in order to provide innovative, value-added solutions on a proactive basis requires ongoing investments in new and existing technologies, as well as the development of key strategic business relationships, including print-on-demand services and product offerings that support customers transitioning to digital business environments. We continue to evaluate new market opportunities and niches, including through acquisitions, and to expand our offerings in areas such as envelopes, tags, folders, healthcare wristbands, specialty packaging, direct mail, pressure seal products, secure document, in-mold labels, and long-run integrated high color web print, which provide opportunities for growth and further differentiate us from our competition. Our ability to make such investments or pursue acquisitions is dependent on our liquidity, capital resources, and operating results.

Production capacity and price competition within our industry – Industry supply of paper products continues to fluctuate as changing market conditions influence producers to idle or permanently close individual machines or mills, or convert capacity to alternative product lines, including packaging, to offset declines in demand for certain paper grades. Recent industry activity has included temporary idling of machines, permanent closures and limited increases in specialty paper capacity, reflecting ongoing adjustments in response to shifts in demand. During the current fiscal year, the only domestic producer of carbonless paper permanently closed its mill which has contributed to ongoing supply constraints for this product. As previously reported, we increased inventory levels to provide buffer stock while transitioning to alternative sources of carbonless paper.

These dynamics may result in continued supply constraints and input cost volatility for certain paper grades. Margins remain under pressure due to volume variability in certain markets, elevated input costs and ongoing pricing competition. To mitigate these impacts, we continue to manage product costs through forecasting, production and costing models, strengthening supplier relationships; negotiating procurement terms; and improving operational efficiency, while evaluating opportunities to better leverage our fixed cost structure.

Continued consolidation of our customers – Our customers are primarily distributors, many of which are consolidating or are being acquired by competitors. While we have historically maintained a significant share of business with these customers, continued consolidation may affect our sales volume, pricing, and margins.

Critical Accounting Estimates

In preparing our Consolidated Financial Statements, we are required to make estimates and assumptions that affect the disclosures and reported amounts of assets and liabilities at the date of the Consolidated Financial Statements and the reported amounts of revenues and expenses during the reporting period. We evaluate our estimates and judgments on an ongoing basis, including those related to allowance for credit losses, inventory valuations, property, plant and equipment, intangible assets, pension plan obligations, accrued liabilities and income taxes. We base our estimates and judgments on historical experience and on various other factors that we believe to be reasonable under the circumstances. Actual results may differ materially from these estimates under different assumptions or conditions. We believe the following accounting estimates are the most critical due to the application of significant subjective assumptions and judgments in the preparation of such estimates, which are included in our Consolidated Financial Statements.

In December 2023, the Financial Accounting Standards Board ("FASB") issued Accounting Standards Update ("ASU") No. 2023-09, Improvements to Income Tax Disclosures (Topic 740). The ASU requires disaggregated information about a reporting entity's effective tax rate reconciliation. Refer to Note 14, Income taxes.

Pension Plan – We maintain the Pension Plan for certain eligible employees. Included in our financial results are Pension Plan costs that are measured using actuarial valuations and require the use of a number of significant assumptions. Changes in these assumptions can result in different expense and liability amounts and future actual pension cost experience and funding requirements may differ materially from current estimates.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The following discussion provides information which we believe is relevant to understanding our results of operations and financial condition. The discussion and analysis should be read in conjunction with the accompanying Consolidated Financial Statements and notes thereto. Unless otherwise indicated, this financial overview is for the continuing operations of the Company, which are comprised of the production and sales of business forms and other business products. The operating results of the Company for fiscal year 2026 and the comparative fiscal years 2025 and 2024 are included in the tables below.

Consolidated Summary

Consolidated Statements of | Fiscal Years Ended
Operations - Data ( in thousands) | 2026 | 2025 | 2024
Net sales | 392,403 | 100.0 | % | 394,618 | 100.0 | % | 420,109 | 100.0 | %
Cost of goods sold | 271,992 | 69.3 | 277,324 | 70.3 | 294,767 | 70.2
Gross profit margin | 120,411 | 30.7 | 117,294 | 29.7 | 125,342 | 29.8
Selling, general and administrative | 67,734 | 17.3 | 65,378 | 16.6 | 68,830 | 16.4
(Gain) loss from disposal of assets | (13 | — | (58 | — | 53 | —
Income from operations | 52,690 | 13.4 | 51,974 | 13.2 | 56,459 | 13.4
Other income (expense), net | 5,904 | 1.5 | 3,480 | 0.9 | 2,664 | 0.6
Earnings before income taxes | 58,594 | 14.9 | 55,454 | 14.1 | 59,123 | 14.1
Provision for income taxes | 15,967 | 4.1 | 15,232 | 3.9 | 16,526 | 3.9
Net earnings | 42,627 | 10.9 | % | 40,222 | 10.2 | % | 42,597 | 10.1 | %

Net Sales . Our net sales were $392.4 million for fiscal year 2026, compared to $394.6 million for fiscal year 2025, a decrease of $2.2 million, or 0.6%. The decrease was primarily driven by lower organic volumes of approximately $25.0 million, reflecting continued softness in portions of the print market and ongoing pricing competition. The decline was largely offset by approximately $22.8 million increase in revenues generated from our recent acquisitions. Industry demand continues to be influenced by the long-term shift toward digital alternatives, although print remains an essential component in many of our customers' operations. We continue to focus on, and maintain our pricing discipline, while optimizing our product mix to mitigate volume-related pressures.

Our net sales were $394.6 million for fiscal year 2025 compared to $420.1 million for fiscal year 2024, a decrease of $25.5 million or 6.1%, primarily due to a $38.7 million decrease in volume demand, partially offset by an approximately $13.2 million increase in revenues generated from our recent acquisitions during fiscal year 2024 and 2025.

Cost of Goods Sold . Manufacturing costs decreased $5.3 million, or 1.9% from $277.3 million for fiscal year 2025 to $272.0 million for fiscal year 2026, primarily reflecting lower sales volumes, partially offset by higher input costs in certain categories. Our gross profit was $120.4 million or 30.7% of sales for fiscal year 2026, compared to $117.3 million or 29.7% of sales for fiscal year 2025. The improvement in gross margin was driven by pricing discipline, product mix, and ongoing cost management initiatives, including procurement strategies and manufacturing efficiencies.

Manufacturing costs decreased $17.5 million, or 5.9%, from $294.8 million for fiscal year 2024 to $277.3 million for fiscal year 2025 primarily as a result of decreased sales volume. Our gross profit was $117.3 million or 29.7% of sales for fiscal year 2025, compared to $125.3 million or 29.8% for fiscal year 2024.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-05-08_item1_business.md)

ITEM 1. BUSINESS

Overview

Ennis, Inc. (collectively with its subsidiaries, the " Company ," " Registrant ," " Ennis ," or " we ," " us ," or " our ") was organized under the laws of Texas in 1909. Ennis is primarily a "trade printer" that manufactures a broad range of printed products that are resold throughout the United States through a network of independent distributors. This distributor channel encompasses independent print distributors, commercial printers, direct mail, fulfillment companies, payroll and accounts payable software companies, and advertising agencies, among others. We also sell products to many of our competitors to satisfy their customers' needs.

Business Overview

Our management believes we are the largest provider of business forms, pressure-seal forms, labels, tags, envelopes, and presentation folders to independent distributors in the United States.

We are in the business of manufacturing, designing and selling business forms and other printed business products primarily to distributors located in the United States. We operate approximately 50 manufacturing plants throughout the United States in 20 strategically located states as one reportable segment; printing services and manufacture of business forms. Approximately 95% of the business products we manufacture are custom and semi-custom products, constructed in a wide variety of sizes, colors, number of parts and quantities on an individual job basis, depending upon the customers' specifications.

The products we sell include snap sets, continuous forms, laser cut sheets, tags, labels, envelopes, integrated products, jumbo rolls and pressure sensitive products in short, medium and long runs under the following labels: Ennis®, Royal Business Forms®, Block Graphics®, ColorWorx®, Enfusion®, Uncompromised Check Solutions®, VersaSeal®, Ad Concepts SM , FormSource Limited SM , Star Award Ribbon Company®, Witt Printing®, Genforms®, PrintGraphics®, Calibrated Forms®, PrintXcel®, Printegra®, Forms Manufacturers SM , Mutual Graphics®, TRI-C Business Forms SM , Major Business Systems SM , Independent Printing SM , Hayes Graphics®, Wright Business Graphics SM , Wright 360 SM , Integrated Print & Graphics SM , the Flesh Company SM , AmeriPrint SM ; Stylecraft SM , UMC Print SM ; Eagle Graphics SM , Diamond Graphics SM , Printing Technologies SM and CFC Print & Mail SM . We also sell the Adams McClure® brand (which provides Point of Purchase advertising); the Admore®, Folder Express®, and Independent Folders® brands (which provide presentation folders and document folders); Ennis Tag & Label SM (which provides custom printed, high performance labels and custom and stock tags); Allen-Bailey Tag & Label SM , Atlas Tag & Label®, Kay Toledo Tag®, and Special Service Partners® (SSP) (which provides custom and stock tags and labels); Trade Envelopes®, Block Graphics®, Wisco®, National Imprint Corporation®, Northeastern Envelope Company SM , and Envelope Superstore SM (which provide custom and imprinted envelopes); Northstar® and General Financial Supply® (which provide financial and security documents); Infoseal SM and PrintXcel® (which provide custom and stock pressure seal documents). School Photo Marketing and National School Forms are a one-stop shop for over 1,400 school portrait photographers and professional photo labs nationwide, providing them with a complete array of products and services that reach over 15 million families and 30,000 schools, primarily in the K-8 market. We sell predominantly through independent distributors, as well as to many of our competitors. Northstar Computer Forms, Inc., one of our wholly-owned subsidiaries, also sells direct to a small number of customers, generally large banking organizations (where a distributor is not acceptable or available to the end-user). Adams McClure, LP, a wholly-owned subsidiary, also sells direct to a small number of customers, where sales are generally through advertising agencies.

The printing industry generally sells its products either predominantly to end users, a market dominated by a few large manufacturers, such as R.R. Donnelley and Taylor Corporation, or, like the Company, through a variety of independent distributors and distributor groups. While it is not possible, because of the lack of adequate public statistical information, to determine the Company's share of the total business products market, management believes the Company is the largest producer of business forms, pressure-seal forms, labels, tags, envelopes, and presentation folders in the United States distributing primarily through independent distributors.

There are a number of competitors that operate in this segment. We believe our strategic locations and buying power permit us to compete on a favorable basis within the distributor market on competitive factors, such as service, quality, and price.

Distribution of business forms and other business products throughout the United States is primarily done through independent distributors, including business forms distributors, resellers, direct mail, commercial printers, software companies, and advertising agencies.

Raw materials principally consist of a wide variety of weights, widths, colors, sizes, and qualities of paper for business products purchased primarily from one major supplier at favorable prices based on our high volume of business with that supplier relative to our competitors.

Business products usage in the printing industry is generally not seasonal. General economic conditions and contraction of the traditional business forms industry are the predominant factors in quarterly volume fluctuations.

Recent Acquisitions

We have completed a number of acquisitions in recent years.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-05-08_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-05-08_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-05-08_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-06-22_2-02-results.md, 10-K_2026-05-08_item7_mdna.md, 10-K_2026-05-08_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
