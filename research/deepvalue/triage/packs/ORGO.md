# Triage pack — ORGO · Organogenesis Holdings Inc.

_Generated 2026-09-04 18:10 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** ORGO · **Name:** Organogenesis Holdings Inc.
- **CIK:** 0001661181
- **SIC:** 2834 — Pharmaceutical Preparations
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/ORGO

**Fetcher warnings for this ticker:** 10-K 2026-02-26: heading split missed Item 1 - Business

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Organogenesis Holdings Inc.
- **CIK:** 1,661,181 · **SIC:** 2834 (Pharmaceutical Preparations) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 1.64 |
| mktcap | $211.0M |
| ev | $164.9M |
| ev_ebit | 3.7x |
| fcf | -$24.5M |
| fcf_yield | -11.6% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 34.6% |
| net_debt | -$46.1M |
| net_debt_ebit | -1.0x |
| cash | $46.1M |
| ltd | $0.00 |
| equity | $148.3M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $564.2M |
| revenue_prior | $482.0M |
| rev_growth | 17.0% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $44.7M |
| net_income | $37.0M |
| cfo | -$10.3M |
| capex | $14.2M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 1.4% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 128,674,548 |
| shares_py | 126,857,709 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -52.2% |
| r6m | -43.4% |
| off_52w_high | -74.9% |
| adv20 | $1.6M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.07 |
| r_ev_ebit | 0.96 |
| r_roic | 0.95 |
| r_rev_growth | 0.80 |
| r_buyback | 0.39 |
| score | 0.54 |

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
| rank | 212 |

**Screen rationale:** cheap at 3.7x EV/EBIT; high ROIC 34.6%; revenue +17.0%; debt data missing (net cash unverified); WARNING 6m return below -40%


## 3. Share count trend

- Shares outstanding: **128,674,548** (CY2026Q2I) vs **126,857,709** prior year (CY2025Q2I)
- Change: **1.4%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-06** — Item 1.01 (Entry into a Material Definitive Agreement): On August 6, 2026, Organogenesis Holdings Inc. (the "Corporation") entered into an At-the-Market Sales Agreement (the "Sales Agreement") with BTIG, LLC ("BTIG") and Citizens JMP Securities, LLC ("Citizens" and together with BTIG, the "Agents"), each as sales...
- **2026-06-16** — Item 5.02 (officer / director change or comp arrangement): On June 15, 2026, the holders of our Series A Convertible Preferred Stock voted by written consent to re-elect Garrett Lustig to our board of directors, to serve until the next Annual Meeting of Stockholders and until his successor is elected and qualified.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 15,000 sh / $40,093 vs sells 0 sh / $0 -> net $40,093 (BUYING).
Distinct insiders buying (code P): 2. Largest buy: Driscoll Michael Joseph bought 10,000 sh @ $2.67 ($26,688) on 2026-03-09.

Form 4 filings parsed: 12; transaction rows: 31 (open-market buys 2, sales 0).

| code | rows |
|---|---|
| A | 20 |
| F | 7 |
| M | 2 |
| P | 2 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'Organogenesis Holdings Inc. Reports Second Quarter 2026 Financial Resu'; skipped 8 forward-looking-statement block(s); 5 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (orgo-ex99_1.htm)

Organogenesis Holdings Inc. Reports Second Quarter 2026 Financial Results

CANTON, Mass., (August 6, 2026) -- Organogenesis Holdings Inc. (Nasdaq: ORGO), a leading regenerative medicine and tissue innovations company focused on empowering healing through the development, manufacture, and sale of product solutions for the Advanced Wound Care and Surgical & Sports Medicine markets, today reported financial results for the second quarter ended June 30, 2026.

Second Quarter 2026 Financial Results Summary:

•
Net revenue of $42.8 million for the second quarter of 2026, a decrease of $58.0 million compared to net revenue of $100.8 million for the second quarter of 2025. Net revenue for the second quarter of 2026 consists of:

o
Net revenue from Advanced Wound Care products of $36.1 million, a decrease of 61% from the second quarter of 2025.

o
Net revenue from Surgical & Sports Medicine products of $6.7 million, a decrease of 18% from the second quarter of 2025.

•
Net loss of $96.3 million for the second quarter of 2026, compared to a net loss of $9.4 million for the second quarter of 2025, an increase in net loss of $86.9 million.

•
Adjusted net loss of $89.0 million for the second quarter of 2026, compared to an adjusted net loss of $7.5 million for the second quarter of 2025, an increase in adjusted net loss of $81.5 million.

•
Adjusted EBITDA loss of $34.4 million for the second quarter of 2026, compared to Adjusted EBITDA loss of $3.6 million for the second quarter of 2025, an increase in EBITDA loss of $30.7 million.

"We are encouraged by signs of measured improvement in business trends in the second quarter, though the pace of recovery from the significant market contraction is slower than we expected," said Gary S. Gillheeney, Sr., President, Chief Executive Officer and Chair of the Board for Organogenesis. "Our business is built on efficacy and outcomes, and that is driving our expanding share as the market resets and customers turn to solutions they can trust. We remain convinced that we occupy the strongest long-term position and will remain the leader with the best evidence-based regenerative medicine products, while advancing the ReNu program to unlock new markets for the company."

Second Quarter 2026 Financial Results:

﻿

Three Months Ended June 30, | Change
2026 | 2025 | %
(in thousands, except for percentages)
Advanced Wound Care | 36,146 | 92,696 | (56,550 | (61 | %)
Surgical & Sports Medicine | 6,659 | 8,083 | (1,424 | (18 | %)
Net product revenue | 42,805 | 100,779 | (57,974 | (58 | %)

Net product revenue for the second quarter of 2026 was $42.8 million, compared to $100.8 million for the second quarter of 2025, a decrease of $58.0 million, or 58%. The decrease in net product revenue was driven by a decrease of $56.6 million, or 61%, in net product revenue for Advanced Wound Care products.

Gross profit for the second quarter of 2026 was $19.1 million, or 45% of net product revenue, compared to $73.1 million, or 73% of net product revenue for the second quarter of 2025, a decrease of $54.0 million, or 74%.

Operating expenses for the second quarter of 2026 were $94.7 million compared to $113.6 million for the second quarter of 2025, a decrease of $18.8 million, or 17%. Cost of goods sold was $23.7 million for the second quarter of 2026, compared to $27.6 million for the second quarter of 2025, a decrease of $4.0 million, or 14%. Selling, general and administrative expenses were $54.0 million for the second quarter of 2026, compared to $73.8 million for the second quarter of 2025, a decrease of $19.8 million, or 27%. R&D expense was $18.3 million for the second quarter of 2026, compared to $10.4 million for the second quarter of 2025, an increase of $7.9 million, or 76%.

Operating loss for the second quarter of 2026 was $51.0 million, compared to an operating loss of $12.6 million for the second quarter of 2025, an increase in operating loss of $38.4 million.

Total other income, net, for the second quarter of 2026 was $0.1 million, compared to $0.7 million for the second quarter of 2025, a decrease of $0.6 million.

Net loss for the second quarter of 2026 was $96.3 million, or $(0.77) per share, compared to net loss of $9.4 million, or $(0.10) per share, for the second quarter of 2025, an increase in net loss of $86.9 million, or $(0.67) per share.

Adjusted net loss was $89.0 million for the second quarter of 2026, compared to adjusted net loss of $7.5 million for the second quarter of 2025, an increase in adjusted net loss of $81.5 million.

Adjusted EBITDA loss was $34.4 million for the second quarter of 2026, compared to Adjusted EBITDA loss of $3.6 million for the second quarter of 2025, an increase in adjusted EBITDA loss of $30.7 million.

Non-GAAP operating loss was $41.1 million for the second quarter of 2026, compared to non-GAAP operating loss of $10.0 million for the second quarter of 2025, an increase in non-GAAP operating loss of $31.1 million.

Six Months ended June 30,2026 Financial Results:

Six Months Ended June 30, | Change
2026 | 2025 | %
(in thousands, except for percentages)
Advanced Wound Care | 65,628 | 172,623 | (106,995 | (62 | %)
Surgical & Sports Medicine | 13,427 | 14,849 | (1,422 | (10 | %)
Net product revenue | 79,055 | 187,472 | (108,417 | (58 | %)

Net product revenue for the six months ended June 30, 2026 was $79.1 million, compared to $187.5 million for the six months ended June 30, 2025, a decrease of $108.4 million, or 58%. The decrease in net product revenue was driven by a decrease of $107.0 million, or 62%, in net product revenue for Advanced Wound Care products.

Gross profit for the six months ended June 30, 2026 was $29.6 million, or 37% of net product revenue, compared to $136.1 million, or 73% of net product revenue for the six months ended June 30, 2025, a decrease of $106.5 million, or 78%.

Operating expenses for the six months ended June 30, 2026 were $200.9 million compared to $227.0 million for the six months ended June 30, 2025, a decrease of $26.2 million, or 12%. Cost of goods sold was $49.4 million for the six months ended June 30, 2026, compared to $51.4 million for the six months ended June 30, 2025, a decrease of $1.9 million, or 4%. Selling, general and administrative expenses were $119.2 million for the six months ended June 30, 2026, compared to $146.3 million for the six months ended June 30, 2025, a decrease of $27.2 million, or 19%. R&D expense was $33.5 million for the six months ended June 30, 2026, compared to $21.0 million for the six months ended June 30, 2025, an increase of $12.4 million, or 59%.

Operating loss for the six months ended June 30, 2026 was $119.9 million, compared to an operating loss of $39.3 million for the six months ended June 30, 2025, an increase in operating loss of $80.6 million.

Total other income, net, for the six months ended June 30, 2026 was $0.5 million, compared to $1.7 million for the six months ended June 30, 2025, a decrease of $1.2 million.

Net loss for the six months ended June 30,2026 was $149.4 million, or $(1.21) per share, compared to net loss of $28.2 million, or $(0.27) per share, for the six months ended June 30, 2025, an increase in net loss of $121.2 million, or $(0.94) per share.

Adjusted net loss was $132.8 million for the six months ended June 30, 2026, compared to adjusted net loss of $20.9 million for the six months ended June 30, 2025, an increase in adjusted net loss of $111.8 million.

Adjusted EBITDA loss was $82.5 million for the six months ended June 30, 2026, compared to Adjusted EBITDA loss of $16.2 million for the six months ended June 30, 2025, an increase in adjusted EBITDA loss of $66.4 million.

Non-GAAP operating loss was $97.1 million for the six months ended June 30, 2026, compared to non-GAAP operating loss of $29.3 million for the six months ended June 30, 2025, an increase in non-GAAP operating loss of $67.7 million.

As of June 30, 2026, the Company had $46.8 million in cash, cash equivalents and restricted cash and no outstanding debt obligations, compared to $94.3 million in cash, cash equivalents and restricted cash and no outstanding debt obligations as of December 31, 2025.

Fiscal Year 2026 Outlook:

For the year ending December 31, 2026, the Company now expects:

•
Total net revenue between $179.0 million and $215.0 million, representing a decline in the range of 62% to 68%, as compared to total net revenue of $564.2 million for the year ended December 31, 2025.

o
Our updated total revenue guidance continues to reflect the expectation that we see sequential improvement in our revenue trends in the in the third and fourth quarters, however, at a more measured rate versus what our prior guidance assumed, resulting in a second half revenue decline in the range of approximately 64% to 74% year over year, and compared to our prior guidance range which assumed a decline in the range of 45% to 52% year-over-year.

Second Quarter Earnings Conference Call:

Management will host a conference call at 5:00 p.m. Eastern Time on August 6th to discuss the results of the quarter, and to provide a corporate update with a question and answer session. Those who would like to participate may access the live webcast here , or access the teleconference here . The live webcast can also be accessed via the company's website at investors.organogenesis.com. The webcast will be archived on the company website for approximately one year .

ORGANOGENESIS HOLDINGS INC.

UNAUDITED CONDENSED CONSOLIDATED BA LANCE SHEETS

(amounts in thousands, except share and per share data)

June 30, | December 31,
2026 | 2025
Assets
Current assets:
Cash and cash equivalents | 46,097 | 93,679
Restricted cash | 747 | 652
Accounts receivable, net | 100,937 | 217,451
Inventories, net | 29,280 | 29,627
Asset held for sale | 3,613 | 2,425
Prepaid expenses and other current assets | 19,628 | 18,354
Total current assets | 200,302 | 362,188
Property and equipment, net | 101,531 | 103,711
Intangible assets, net | 3,004 | 9,145
Goodwill | 28,772 | 28,772
Operating lease right-of-use assets, net | 49,912 | 55,749
Deferred tax asset, net | — | 29,962
Other assets | 22,925 | 9,203
Total assets | 406,446 | 598,730
Liabilities, Redeemable Convertible Preferred Stock, and Stockholders' Equity
Current liabilities:
Current portion of finance lease obligations | 859 | 9,435
Current portion of operating lease obligations - related party | 4,647 | 4,258
Current portion of operating lease obligations | 3,807 | 4,949
Accounts payable | 29,291 | 31,949
Accrued expenses and other current liabilities | 18,359 | 49,533
Total current liabilities | 56,963 | 100,124
Finance lease obligations, net of current portion | 10,820 | 12,788
Operating lease obligations, net of current portion - related party | 25,738 | 28,237
Operating lease obligations, net of current portion | 21,079 | 22,470
Other liabilities | 3,714 | 1,193
Total liabilities | 118,314 | 164,812
Commitments and contingencies (Note 15)
Series A redeemable convertible preferred stock, $0.0001 par value; 130,000 shares authorized, issued and outstanding; liquidation preference of $147,963 and $142,217 at June 30, 2026 and December 31, 2025, respectively. | 139,864 | 133,789
Stockholders' equity:
Preferred stock, $0.0001 par value; 870,000 shares authorized; none issued or outstanding | — | —
Common stock, $0.0001 par value; 400,000,000 shares authorized; 129,403,096 and 127,680,424 shares issued; 128,674,548 and 126,951,876 shares outstanding at June 30, 2026 and December 31, 2025, respectively. | 13 | 13
Additional paid-in capital | 300,756 | 303,194
Accumulated deficit | (152,501 | (3,078
Total stockholders' equity | 148,268 | 300,129
Total liabilities, redeemable convertible preferred stock, and stockholders' equity | 406,446 | 598,730

ORGANOGENESIS HOLDINGS INC. UNAUDITED CONDENSED CONSOLIDATED STATEMENTS OF OPERATIONS AND COMPREHENSIVE LOSS

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-26_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

Organogenesis is a leading regenerative medicine company focused on empowering healing through the development, manufacturing, and sale of products for the advanced wound care and surgical and sports medicine markets. Our products have been shown through clinical and scientific studies to support and in some cases accelerate tissue healing and improve patient outcomes. We are advancing the standard of care in each phase of the healing process through multiple breakthroughs in tissue engineering and cell therapy. Our solutions address large and growing markets driven by aging demographics and increases in comorbidities such as diabetes, obesity, cardiovascular and peripheral vascular disease. We offer our differentiated products and in-house customer support to a wide range of health care customers including hospitals, wound care centers, government facilities, ASCs and physician offices. Our mission is advancing healing and recovery beyond expectations.

We offer a comprehensive portfolio of products in the markets we serve that address patient needs across the continuum of care. We have and intend to continue to generate data from clinical trials, real-world outcomes and health economics research that validate the clinical efficacy and value proposition offered by our products. Several of our existing and pipeline products in our portfolio have PMA, or 510(k) clearance from the FDA. Given the extensive time and cost required to conduct clinical trials and receive FDA approvals, we believe that our data and regulatory approvals provide us with a strong competitive advantage. Our product development expertise and multiple technology platforms provide a robust product pipeline, which we believe will drive future growth.

In the Advanced Wound Care market, we focus on the development and commercialization of advanced wound care products for the treatment of chronic and acute wounds in various treatment settings. We have a comprehensive portfolio of regenerative medicine products capable of supporting patients from early in the wound healing process through wound closure regardless of wound type. Our Advanced Wound Care products include Apligraf for the treatment of VLUs and DFUs; Dermagraft for the treatment of DFUs (manufacturing and distribution currently suspended pending transition to our new manufacturing facility in Smithfield, RI); PuraPly AM and PuraPly XT as antimicrobial barriers and native, cross-linked extracellular matrix ("ECM") scaffold for a broad variety of wound types; CYGNUS Dual as a dual-layered amniotic membrane that promotes an optimal environment for wound healing; CYGNUS Matrix as a dehydrated placental allograft that promotes an optimal environment for wound healing; VIA Matrix, Affinity, Novachor, and NuShield placental allografts to address a variety of wound sizes and types as a protective barrier and ECM scaffold, and SimpliMax as a dehydrated amnion allograft that provides a protective barrier and supports an optimal environment for inherent healing of a wide range of acute and chronic wounds. We have a highly trained and specialized direct wound care sales force paired with comprehensive customer support services.

In the Surgical & Sports Medicine market, we are leveraging our broad regenerative medicine capabilities to address chronic and acute surgical wounds and tendon and ligament injuries. Our Sports Medicine products include NuShield and Cygnus Matrix for surgical applications in targeted soft tissue repairs; and Affinity, Novachor, PuraPly MZ, PuraPly AM, and PuraPly SX for management of open wounds in the surgical setting. We currently sell these products through independent agencies and our direct sales force.

Local Coverage Determinations and CMS Proposed and Final Rules

On April 25, 2024, seven MACs published new proposed LCDs for skin substitute grafts/CTPs for the treatment of DFUs and VLUs in the Medicare population. These LCDs were finalized by the MACs on November 14, 2024, and were originally set to become effective on February 12, 2025. However, on January 24, 2025, the MACs announced a delay in the implementation of the LCDs until April 13, 2025, and on April 11, 2025, the MACs announced another delay in the implementation of the LCDs until January 1, 2026. On December 15, 2025, CMS released a fact sheet stating that the MACs will issue updated LCDs that were to become effective January 1, 2026. The fact sheet included a new categorization of products as covered, non-covered, or those subject to a 12-month status quo period. However, on December 24, 2025, CMS announced that the LCDs had been withdrawn by the MACs

and the most recent draft LCDs were removed from the Medicare Coverage Database. Any future changes or other developments related to these or other LCDs or coverage decisions could negatively affect utilization of our products, our business, and our revenue.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The following table sets forth, for the periods indicated, our results of operations (amounts in thousands):

Year Ended December 31,
2025 | 2024 | 2023
Revenue:
Net product revenue | 563,030 | 482,043 | 433,140
Grant income | 1,139 | — | —
Total revenue | 564,169 | 482,043 | 433,140
Operating expenses:
Cost of goods sold | 137,522 | 115,741 | 106,481
Selling, general and administrative | 326,236 | 294,513 | 269,754
Research and development | 44,542 | 50,271 | 44,380
Write-down to fair value for asset held for sale | 11,175 | — | —
Impairment of property and construction | — | 18,842 | —
Write-down of capitalized internal-use software costs | — | 3,959 | —
Total operating expenses | 519,475 | 483,326 | 420,615
Income (loss) from operations | 44,694 | (1,283 | 12,525
Other income (expense), net:
Interest income (expense), net | 2,281 | (1,544 | (2,190
Other income (expense), net | (5 | 20 | 57
Total other income (expense), net | 2,276 | (1,524 | (2,133
Net income (loss) before income taxes | 46,970 | (2,807 | 10,392
Income tax benefit (expense) | (9,938 | 3,668 | (5,447
Net income and comprehensive income | 37,032 | 861 | 4,945

EBITDA and Adjusted EBITDA

The following table presents a reconciliation of GAAP net income to Non-GAAP EBITDA and Non-GAAP Adjusted EBITDA, for each of the periods presented:

Year Ended December 31,
2025 | 2024 | 2023
(in thousands)
Net income | 37,032 | 861 | 4,945
Interest expense (income), net | (2,281 | 1,544 | 2,190
Income tax expense (benefit) | 9,938 | (3,668 | 5,447
Depreciation and amortization | 15,273 | 13,623 | 10,448
Amortization of intangible assets | 3,323 | 3,403 | 4,918
EBITDA | 63,285 | 15,763 | 27,948
Stock-based compensation expense | 13,298 | 10,578 | 8,996
Write-down to fair value for asset held for sale (1) | 11,175 | — | —
Restructuring charge (2) | 516 | — | 3,796
Legal and consulting fees (3) | — | — | 1,182
Sales retention (4) | — | — | 694
Impairment of property and construction (5) | — | 18,842 | —
Write-down of capitalized software costs (6) | — | 3,959 | —
Disposal of construction in progress (7) | — | 645 | —
FDA BLA fees for ReNu (8) | 4,682 | — | —
PFS regulation related charges (9) | 3,723 | — | —
Inventory write-downs (10) | 1,458 | — | —
Adjusted EBITDA | 98,137 | 49,787 | 42,616

(1)
Amount reflects the fair value adjustment of a purchased building classified as held for sale. See Note 8, Property and Equipment, Net.

(2)
Amounts reflect employee retention and benefits as well as other exit costs associated with our restructuring activities. See Note 11, Restructuring , to our audited consolidated financial statements included in this Annual Report on Form 10-K.

(3)
Amount reflects the legal and consulting fees incurred related to the published and subsequently withdrawn 2023 LCDs.

(4)
Amount reflects the compensation expenses related to retention for those sales employees impacted by the published and subsequently withdrawn 2023 LCDs.

(5)
Amount reflects the impairment of a purchased building and associated unfinished construction work. See Note 8, Property and Equipment, Net to our audited consolidated financial statements included in this Annual Report on Form 10-K.

(6)
Amount reflects the write-down of costs previously capitalized as construction in progress in the development of internal-use software, that the Company determined have no future value. See Note 8, Property and Equipment, Net to our audited consolidated financial statements included in this Annual Report on Form 10-K.

(7)
Amount reflects construction in progress terminated and disposed of at one of our Canton, Massachusetts facilities, resulting from the Company's decision to move certain operations to the Smithfield Facility.

(8)
Amount reflects fees paid to the FDA in connection with the ReNu BLA filing.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business

_Not available: the fetcher did not split out this section for this filing. Describe the business from the MD&A overview above instead, and say so in the note._

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | **MISSING** |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-26_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-26_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-02-26_item7_mdna.md

**Missing:** 10-K Item 1 - Business (business description), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
