# Triage pack — LMAT · LEMAITRE VASCULAR INC

_Generated 2026-09-04 18:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** LMAT · **Name:** LEMAITRE VASCULAR INC
- **CIK:** 0001158895
- **SIC:** 3841 — Surgical & Medical Instruments & Apparatus
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/LMAT

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** LEMAITRE VASCULAR INC
- **CIK:** 1,158,895 · **SIC:** 3841 (Surgical & Medical Instruments & Apparatus) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 80.49 |
| mktcap | $1.8B |
| ev | $1.8B |
| ev_ebit | 26.7x |
| fcf | $74.5M |
| fcf_yield | 4.0% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 13.6% |
| net_debt | -$26.6M |
| net_debt_ebit | -0.4x |
| cash | $26.6M |
| ltd | $0.00 |
| equity | $420.3M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $249.6M |
| revenue_prior | $219.9M |
| rev_growth | 13.5% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $67.9M |
| net_income | $57.7M |
| cfo | $81.3M |
| capex | $6.8M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 1.0% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 22,869,257 |
| shares_py | 22,637,522 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -15.9% |
| r6m | -23.6% |
| off_52w_high | -31.1% |
| adv20 | $27.8M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.43 |
| r_ev_ebit | 0.33 |
| r_roic | 0.78 |
| r_rev_growth | 0.74 |
| r_buyback | 0.44 |
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
| rank | 202 |

**Screen rationale:** high ROIC 13.6%; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **22,869,257** (CY2026Q2I) vs **22,637,522** prior year (CY2025Q2I)
- Change: **1.0%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-04-14** — Item 5.02 (officer / director change or comp arrangement): (b) On April 8, 2026, Bridget Ross notified the Board of Directors (the "Board") of LeMaitre Vascular, Inc. (the "Company") of her intent not to stand for re-election as a Class II director of the Company at the Company's 2026 Annual Meeting of Stockholders...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 49,409 sh / $5,345,700 -> net $-5,345,700 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 59 (open-market buys 0, sales 3).

| code | rows |
|---|---|
| A | 53 |
| G | 1 |
| M | 2 |
| S | 3 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-04_2-02-results.md)

_Extraction: no Highlights/Results/quarter heading found; started at the top of the exhibit; skipped 9 forward-looking-statement block(s)._

## EX-99.1 - EX-99.1 (d320964dex991.htm)

EX-99.1
d320964dex991.htm
EX-99.1

EX-99.1

Exhibit 99.1

LeMaitre Q2 2026 Financial Results

BURLINGTON, MA, August 4, 2026 – LeMaitre Vascular, Inc. (Nasdaq: LMAT), a provider of vascular devices, implants, and services, today
reported Q2 2026 results, announced a quarterly dividend of $0.25/share, and provided guidance.

Q2 2026:

• | Sales $70.4mm, +10% (+10% organic) vs. Q2 2025

• | Gross margin 72.1% (+210 bps)

• | Op. income $20.4mm (+26%)

• | Op. margin 29%

• | EPS $0.74 (+23%)

• | Cash up $9.0mm sequentially to $376.2mm

Artegraft sales increased 34% in the quarter. Grafts (+23%), carotid shunts (+18%), and patches (+4%) each posted records, as did EMEA (+18%), APAC (+18%) and
the Americas (+5%). Catheters were down 11% in the quarter due to recall-driven overstocking in Q2 2025. Q2 organic growth was 12% excluding catheters.

Gross margin of 72.1% was up 210 bps due to higher prices, mix shift, and operational efficiencies. Operating income of $20.4mm (+26%) also benefited from
headcount restraint: 660 at 6/30/2026 vs. 658 at 6/30/2025.

Chairman/CEO George LeMaitre said, "Our focus on the Artegraft international launch
paid off in Q2. The product is now approved in 56 countries, accounting for 21% of sales. So our largest product is now our fastest-growing product. To underpin the Artegraft launch and pave the way for RFA, we continue to build our sales force, go
direct in new countries and we're now undertaking six international warehouse expansions. $376m of cash provides strategic optionality."

Business Outlook

Q3 2026 Guidance | Q4 2026 Guidance | Full Year Guidance
Sales | $66.3mm - $68.3mm (Mid $67.3mm, +10%, +11% org.) | $71.1mm - $73.1mm (Mid $72.1mm, +12%, +12% org.) | $274.3mm - $278.3mm (Mid $276.3mm, +11%, +11% org.)
Gross Margin | 72.2% | 72.6% | 72.4%
Op. Income | $17.3mm - $18.8mm (Mid $18.1mm, -11%, +7% adj.) | $19.8mm - $21.2mm (Mid $20.5mm, +9%) | $75.3mm - $78.2mm (Mid $76.8mm, +13%, +19% adj.)
Op. Margin (Mid) | 27% | 29% | 28%
EPS | $0.66 - $0.71 (Mid $0.69, -9%, +11% adj.) | $0.75 - $0.81 (Mid $0.78, +15%) | $2.84 - $2.94 (Mid $2.89, +15%, +21% adj.)

* | Q3 2025 results included a non-recurring benefit from the Employee Retention Tax Credit. Non-GAAP adjusted figures exclude this benefit. A reconciliation of GAAP to non-GAAP projected results is included.

Quarterly Dividend

On July 28, 2026, the
Company's Board of Directors approved a quarterly dividend of $0.25/share of common stock. The dividend will be paid on September 3, 2026, to stockholders of record on August 20, 2026.

Share Repurchase Program

On February 19, 2026, the
Company's Board of Directors authorized the repurchase of up to $100.0mm of the Company's common stock. The repurchase program may be suspended or discontinued at any time and will conclude on February 18, 2027, unless extended by
the Board.

Conference Call Reminder

Management will conduct a conference call at 5:00pm ET today. The conference call will be broadcast live over the Internet. Individuals interested in
listening to the webcast can log on to the Company's website at www.lemaitre.com/investor . Access to the live call is available by registering online here . All registrants will receive
dial-in information and a PIN allowing them to access the live call. The audio webcast can also be accessed live or via replay through a webcast at www.lemaitre.com/investor . For individuals unable to
join the live conference call, a replay will be available on the Company's website.

A reconciliation of GAAP to
non-GAAP results is included in the tables attached to this release.

About LeMaitre

LeMaitre is a provider of devices, implants, and services for the treatment of peripheral vascular disease, a condition that affects more than
200 million people worldwide. The Company develops, manufactures, and markets disposable and implantable vascular devices to address the needs of its core customer, the vascular surgeon.

LeMaitre is a registered trademark of LeMaitre Vascular, Inc. This press release may include other trademarks and trade names of the Company.

For more information about the Company, please visit www.lemaitre.com .

Use of Non-GAAP Financial Measures

LeMaitre management believes that in order to better understand the Company's short- and long-term financial trends, investors may wish to consider
certain non-GAAP financial measures as a supplement to financial performance measures prepared in accordance with GAAP. Non-GAAP financial measures are not based on a
comprehensive set of accounting rules or principles and do not have standardized meanings. These non-GAAP measures result from facts and circumstances that may vary in frequency and/or impact on continuing
operations. Non-GAAP measures should be considered in addition to, and not as a substitute for, GAAP financial performance measures. In addition to the description provided below, reconciliation of GAAP to non-GAAP results is provided in the financial statement tables included in this press release.

In this press release,
the Company has reported non-GAAP sales growth percentages after adjusting for the impact of foreign currency exchange, business development transactions, and/or other events. The Company refers to the
calculation of non-GAAP sales growth percentages as "organic" or "adjusted." The Company analyzes non-GAAP sales on a constant currency basis,
net of acquisitions and other non-recurring events. Because changes in foreign currency exchange rates have a non-operating impact on net sales, and acquisitions,
divestitures, product discontinuations, factory closures, and other strategic transactions are episodic in nature and are highly variable to the reported sales results, the Company believes that evaluating growth in sales on a constant currency
basis net of such transactions provides an additional and meaningful assessment of sales to management. Additionally, the Company has provided percentages for operating income and EPS guidance adjusted to exclude the effects of the employee
retention tax credit received in 2025. Management believes that viewing projected growth in operating income and EPS excluding those effects provides an alternative and meaningful view of the Company's projected profitability.

Investors are encouraged to review the reconciliation of these non-GAAP financial measures to their most directly
comparable GAAP financial measures set forth in the tables captioned "Reconciliation of GAAP to Non-GAAP Financial Measures" below.

(amounts in
thousands)

June 30, 2026 | December 31, 2025
(unaudited)
Assets
Current assets:
Cash and cash equivalents | 26,625 | 28,244
Short-term marketable securities | 349,615 | 330,876
Accounts receivable, net | 35,682 | 33,610
Inventory and other deferred costs | 70,503 | 70,422
Prepaid expenses and other current assets | 5,872 | 5,080
Total current assets | 488,297 | 468,232
Property and equipment, net | 29,591 | 26,997
Right-of-use leased assets | 19,998 | 15,762
Goodwill | 65,945 | 65,945
Other intangibles, net | 30,544 | 33,089
Deferred tax assets | 734 | 759
Other assets | 5,440 | 4,906
Total assets | 640,549 | 615,690
Liabilities and stockholders' equity
Current liabilities:
Accounts payable | 3,236 | 3,646
Accrued expenses | 22,880 | 29,411
Acquisition-related obligations | 380 | 322
Lease liabilities - short-term | 3,439 | 2,944
Total current liabilities | 29,935 | 36,323
Convertible senior notes, net | 169,091 | 168,645
Lease liabilities - long-term | 17,724 | 14,003
Deferred tax liabilities | 1,998 | 1,735
Other long-term liabilities | 1,459 | 1,468
Total liabilities | 220,207 | 222,174
Stockholders' equity
Common stock | 245 | 244
Additional paid-in capital | 236,161 | 228,407
Retained earnings | 206,017 | 184,715
Accumulated other comprehensive loss | (4,165 | (2,411
Treasury stock | (17,916 | (17,439
Total stockholders' equity | 420,342 | 393,516
Total liabilities and stockholders' equity | 640,549 | 615,690

LEMAITRE VASCULAR, INC. (NASDAQ: LMAT)

CONDENSED CONSOLIDATED STATEMENT OF OPERATIONS

(amounts
in thousands, except per share amounts)

(unaudited)

For the three months ended | For the six months ended
June 30, 2026 | June 30, 2025 | June 30, 2026 | June 30, 2025
Net sales | 70,382 | 64,232 | 136,933 | 124,103
Cost of sales | 19,618 | 19,258 | 37,773 | 37,709
Gross profit | 50,764 | 44,974 | 99,160 | 86,394
Operating expenses:
Sales and marketing | 14,408 | 14,895 | 28,923 | 29,107
General and administrative | 11,110 | 10,396 | 23,156 | 20,883
Research and development | 4,847 | 3,541 | 8,907 | 7,636
Total operating expenses | 30,365 | 28,832 | 60,986 | 57,626
Income from operations | 20,399 | 16,142 | 38,174 | 28,768
Other income (expense):
Investment income | 3,386 | 2,980 | 6,710 | 5,883
Interest expense | (1,302 | (1,299 | (2,602 | (2,589
Other income (loss), net | (294 | 247 | (421 | 249
Income before income taxes | 22,189 | 18,070 | 41,861 | 32,311
Provision for income taxes | 5,139 | 4,291 | 9,132 | 7,521
Net income | 17,050 | 13,779 | 32,729 | 24,790
Earnings per share of common stock
Basic | 0.75 | 0.61 | 1.43 | 1.10
Diluted | 0.74 | 0.60 | 1.42 | 1.08
Weighted - average shares outstanding:
Basic | 22,858 | 22,614 | 22,830 | 22,592
Diluted | 24,531 | 22,892 | 24,505 | 22,896
Cash dividends declared per common share | 0.25 | 0.20 | 0.50 | 0.40

LEMAITRE VASCULAR, INC. (NASDAQ: LMAT)

CONDENSED CONSOLIDATED STATEMENT OF CASH FLOWS

(amounts
in thousands)

(unaudited)

For the six months ended
June 30, 2026 | June 30, 2025
Operating activities
Net income | 32,729 | 24,790
Adjustments to reconcile net income to net cash provided by operating activities
Depreciation and amortization | 5,285 | 5,200
Stock-based compensation | 4,027 | 3,990
Amortization of issuance costs on convertible notes | 446 | 433
Non-cash investment income | (805 | —
Provision for inventory write-downs | 1,548 | 1,030
Provision for credit losses | 333 | 337
Foreign currency transaction effect on income | 145 | (279
Changes in operating assets and liabilities:
Accounts receivables | (2,877 | (5,299
Inventory and other deferred costs | (1,935 | (3,454
Prepaid expenses and other assets | (1,363 | 1,676
Accounts payable and other liabilities | (6,475 | (1,250
Accrued interest | — | 2,156
Net cash provided by operating activities | 31,058 | 29,330
Investing activities
Purchases of short-term marketable securities | (231,434 | (17,849
Purchases of property and equipment | (5,096 | (2,725
Payments related to acquisitions, net of cash acquired | (158 | (95
Proceeds from short-term marketable securities | 212,489 | —
Net cash used in investing activities | (24,199 | (20,669
Financing activities
Proceeds from stock option exercises | 3,728 | 3,072
Deferred payments for acquisitions | (95 | (1,433
Payment of withholding taxes in connection with net settlement of equity awards | (477 | (605
Common stock cash dividend paid | (11,427 | (9,037
Net cash used in financing activities | (8,271 | (8,003
Effect of exchange rate changes on cash and cash equivalents | (207 | 909
Net (decrease) increase in cash and cash equivalents | (1,619 | 1,567
Cash and cash equivalents at beginning of period | 28,244 | 25,610
Cash and cash equivalents at end of period | 26,625 | 27,177

LEMAITRE VASCULAR, INC. (NASDAQ: LMAT)

SELECTED NET SALES INFORMATION

(amounts in thousands)

(unaudited)

For the three months ended | For the six months ended
June 30, 2026 | June 30, 2025 | June 30, 2026 | June 30, 2025
% | % | % | %
Net Sales by Geography
Americas | 43,454 | 62 | % | 41,321 | 64 | % | 85,050 | 62 | % | 80,279 | 65 | %
Europe, Middle East and Africa | 22,137 | 31 | % | 18,840 | 29 | % | 42,424 | 31 | % | 35,799 | 29 | %
Asia Pacific | 4,791 | 7 | % | 4,071 | 7 | % | 9,459 | 7 | % | 8,025 | 6 | %
Total Net Sales | 70,382 | 100 | % | 64,232 | 100 | % | 136,933 | 100 | % | 124,103 | 100 | %

LEMAITRE VASCULAR, INC (NASDAQ: LMAT)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-26_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We are a global provider of medical devices and human tissue cryopreservation services largely used in the treatment of peripheral vascular disease, end-stage renal disease, and cardiovascular disease. We develop, manufacture, and market vascular devices to address the needs of vascular surgeons and, to a lesser degree, other specialties such as cardiac surgeons, general surgeons, and neurosurgeons. Our diversified portfolio of devices consists of brand name products that are used in arteries and veins and are well known to vascular surgeons. Our principal product offerings are sold globally, primarily in the United States, Europe, Canada, and Asia Pacific, or APAC. We estimate that the annual worldwide market for peripheral vascular devices exceeds $9 billion, within which we estimate that the market for our products is approximately $1 billion. We have grown our business using a three-pronged strategy: 1) pursuing a focused call point, 2) competing for sales of low-rivalry, niche products, and 3) expanding our worldwide direct sales force while acquiring complementary devices. We have used acquisitions as a primary means of further penetrating the peripheral vascular device market, and we expect to continue this strategy in the future. We currently manufacture most of our products in our Burlington, Massachusetts headquarters.

Our products and services are used primarily by vascular surgeons who treat peripheral vascular disease through both open surgical methods and endovascular techniques. In contrast to interventional cardiologists and interventional radiologists, vascular surgeons can perform both open surgical and minimally invasive endovascular procedures, and therefore can provide a wider range of treatment options to their patients. Recently we have also begun to explore adjacent market customers, such as cardiac surgeons and interventional cardiologists.

Our principal product lines include the following: anastomotic clips, biologic vascular and dialysis grafts, biologic vascular and cardiac patches, carotid shunts, embolectomy and occlusion catheters, radiopaque marking tape, synthetic vascular and dialysis grafts, and valvulotomes. Through our RestoreFlow allografts business, we also process and cryopreserve human vascular and cardiac tissue.

Our principal biologic offerings include vascular and cardiac patches as well as vascular and dialysis grafts. In 2025, biologics represented 53% of our worldwide sales. We believe our biologic devices represent differentiated and, in many cases, growing product segments.

Our business opportunities include the following:

•
growing our direct sales force in North America, Europe, and APAC, including replacing distributors with our direct sales personnel;

•
increasing the average selling prices of our devices;

•
introducing our products into new territories upon receipt of regulatory approvals or registrations;

•
acquiring complementary products and the transition of distributor sales to LeMaitre;

•
updating existing products and introducing new products through research and development, and

•
consolidating product manufacturing into our Burlington, Massachusetts facilities.

We sell our products and services primarily through a direct sales force. Our worldwide headquarters is located in Burlington, Massachusetts, and we also have a North American sales office in Vaughan, Canada. Our European headquarters is located in Sulzbach, Germany, and we also have European sales offices in Milan, Italy; Madrid, Spain; Hereford, England; Dublin, Ireland; Maisons-Alfort, France; and Glattbrugg, Switzerland. Our APAC headquarters is located in Singapore, and we also have APAC sales offices in Tokyo, Japan; Shanghai, China; Docklands, Australia; Seoul, Korea; and Bangkok, Thailand. During the year ended December 31, 2025, approximately 95% of our net sales were generated in territories in which we employ direct sales representatives. We sell our products in other countries through distributors. As of December 31, 2025, our sales force comprised 160 sales representatives and export managers in North America, Europe, and APAC.

Historically we have experienced success in lower-rivalry niche segments. In the valvulotome market, for example, our differentiated devices have historically allowed us to increase average selling prices without incurring significant unit share loss. In contrast, we have experienced less success in competitive markets such as the polyester vascular graft market, where we face competition from larger companies with greater resources and lower per unit costs.

We have also experienced success in international markets, such as Europe, where we have a significant sales force, and sometimes offer lower average selling prices than in North America. If we continue to seek growth opportunities outside of North America, we may experience downward pressure on our gross margin.

We obtain regulatory approvals for our devices and services in new product categories and geographies to further access the broader peripheral device market and selected other markets, thus extending our geographic reach. Recent approvals include approvals to sell the XenoSure patch for carotid indication in Japan in May 2023, and the Pruitt Irrigation Occlusion Catheter in China in October 2023; approvals to sell the Artegraft bovine graft in Thailand and Malaysia in August 2024 and South Africa in October 2024, and the XenoSure patch for cardiac indications in China in December 2024; and approvals to sell the Artegraft bovine graft in the European Union (EU) in April 2025, Australia in June 2025, and Canada in December 2025, the Pruitt Aortic Occlusion Catheter in the EU in May 2025, and the Pruitt Occlusion Catheter in China in June 2025.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Comparison of the year ended December 31, 2025 to the year ended December 31, 2024

The following table sets forth, for the periods indicated, our net sales by geography, and the change between the specified periods expressed as a percentage increase or decrease:

2025 | 2024 | $ Change | Percent change
($ in thousands)
Net sales | 249,602 | 219,863 | 29,739 | 14 | %
Net sales by geography:
Americas | 159,665 | 144,583 | 15,082 | 10 | %
Europe, Middle East and Africa | 73,122 | 59,969 | 13,153 | 22 | %
Asia Pacific | 16,815 | 15,311 | 1,504 | 10 | %
Total | 249,602 | 219,863 | 29,739 | 14 | %

Net sales. Net sales increased by $29.7 million, or 14%, to $249.6 million for the year ended December 31, 2025, compared to $219.9 million for the year ended December 31, 2024. The increase was driven primarily by higher average selling prices, higher unit volumes shipped to customers, the European launch of Artegraft, and additional sales representatives. Graft sales increased $16.0 million, valvulotome sales increased $4.7 million, shunt sales increased $3.5 million, catheter sales increased $2.8 million, and patch sales increased $1.8 million. We estimate that the weaker U.S. dollar increased net sales by $2.7 million during the year ended December 31, 2025, as compared to the year ended December 31, 2024.

Direct-to-hospital net sales were 95% of our total net sales for both the years ended December 31, 2025 and 2024, respectively.

Net sales by geography. Net sales in the Americas increased $15.1 million, or 10%, for the year ended December 31, 2025, as compared to the year ended December 31, 2024. The increase was driven primarily by increased sales of grafts of $10.4 million, valvulotomes of $3.1 million, and catheters of $0.9 million.

EMEA net sales increased $13.2 million, or 22%, for the year ended December 31, 2025, as compared to the year ended December 31, 2024. The increase was driven primarily by increased sales of grafts of $5.1 million, which includes the launch of Artegraft, shunts of $2.8 million, catheters of $2.1 million, patches of $1.8 million, and valvulotomes of $1.3 million.

Asia Pacific net sales increased $1.5 million, or 10%, for the year ended December 31, 2025, as compared to the year ended December 31, 2024. The increase was driven primarily by increased sales of grafts and patches of $0.5 million each, valvulotomes of $0.3 million, and clips of $0.2 million.

Gross Profit. The following table sets forth the change in our gross profit and gross margin for the periods indicated:

2025 | 2024 | Change | Percent change
($ in thousands)
Gross profit | 178,539 | 150,901 | 27,638 | 18 | %
Gross margin | 71.5 | % | 68.6 | % | 2.9 | % | *

* Not applicable

Gross profit increased $27.6 million, or 18%, to $178.5 million for the year ended December 31, 2025, as compared to $150.9 million for the year ended December 31, 2024, and gross margin increased by 290 basis points to 71.5% in the period, as compared to 68.6% for the year ended December 31, 2024. The increase in gross profit was driven primarily by increased sales, particularly from grafts, valvulotomes, and shunts, and the receipt of the U.S. Employee Retention Credit ("ERC"). The increase in gross margin was driven primarily by the ERC, greater manufacturing efficiencies, and sales price increases, partially offset by increased shipping and warehousing costs and unfavorable product mix, including increased sales of comparatively lower margin allograft preservation services, ovine grafts, and single lumen embolectomy catheters. The ERC received in 2025 had a favorable impact of $2.7 million, or 109 basis points, to the gross margin.

Operating Expenses. The following table sets forth the change in our operating expenses for the periods indicated and the change between the specified periods expressed as a percentage increase or decrease:

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-26_item1_business.md)

Item 1. B usiness

Overview

We are a global provider of medical devices and human tissue cryopreservation services largely used in the treatment of peripheral vascular disease, end-stage renal disease, and cardiovascular disease. We develop, manufacture, and market vascular devices to address the needs of vascular surgeons and, to a lesser degree, other specialties such as cardiac surgeons, general surgeons, and neurosurgeons. Our diversified portfolio of devices consists of brand name products that are used in arteries and veins and are well known to vascular surgeons. Our principal product offerings are sold globally, primarily in the United States, Europe, Canada and Asia Pacific. We estimate that the annual worldwide market for peripheral vascular devices exceeds $9 billion, within which we estimate that the market for our products is approximately $1 billion.

We sell our products and services primarily through a direct sales force. Our worldwide headquarters is located in Burlington, Massachusetts, and we also have a North American sales office in Vaughan, Canada. Our European headquarters is located in Sulzbach, Germany, and we also have European sales offices in Milan, Italy; Madrid, Spain; Hereford, England; Dublin, Ireland; Maisons-Alfort, France; and Glattbrugg, Switzerland. Our Asia Pacific headquarters is located in Singapore, and we also have Asia Pacific sales offices in Tokyo, Japan; Shanghai, China; Docklands, Australia; Seoul, Korea; and Bangkok, Thailand. During the year ended December 31, 2025, approximately 95% of our net sales were generated in territories in which we employ direct sales representatives. We also sell our products in other countries through distributors. As of December 31, 2025, our sales force comprised 160 sales representatives and export managers in North America, Europe, and Asia Pacific.

The Peripheral Vascular Disease Market

Based on industry statistics, we estimate that peripheral vascular disease affects more than 200 million people worldwide and that the annual worldwide market for all peripheral vascular devices exceeds $9 billion. The disease encompasses a number of conditions in which the arteries or veins that carry blood to or from the legs, arms, or organs other than the heart become narrowed, obstructed, weakened, or otherwise compromised. In many cases peripheral vascular disease goes undetected, sometimes leading to life-threatening events (including stroke, ruptured aneurysm, and pulmonary embolism) or death. Clinical studies have identified several factors that increase the risk of peripheral vascular disease, including smoking, diabetes, obesity, high blood pressure, lack of exercise, coronary artery disease, high cholesterol, and being over the age of 65. Demographic trends suggest an increase in the prevalence of peripheral vascular disease over time, driven primarily by rising levels of obesity and diabetes and an aging population. We believe that our strong brands, established sales force, suite of peripheral vascular device offerings, and broad network of vascular surgeon customers position us to capture an increasing share of this market.

Vascular surgeons treat peripheral vascular disease and perform vascular procedures associated with other diseases, such as end-stage renal disease. We estimate that there are more than 22,000 vascular surgeons worldwide. In contrast to other specialists, such as interventional cardiologists and interventional radiologists, vascular surgeons perform both open vascular surgeries and endovascular procedures. Open vascular surgery involves opening the body, cutting vessels, and suturing. Endovascular procedures typically are minimally invasive, catheter-based, and treat vessels from within using real-time imaging. We estimate that in 2025, over 95% of our net sales were from devices used in open surgical procedures, including open vascular surgeries and open cardiac surgeries.

Our Business Strategies

We have grown our business by using a three-pronged strategy: 1) pursuing a focused call point, 2) competing for sales of low-rivalry, niche products, and 3) expanding our worldwide direct sales force while acquiring complementary devices. We have used acquisitions as a primary means of further penetrating the peripheral vascular device market, and we expect to

continue this strategy in the future. We currently manufacture most of our products in our Burlington, Massachusetts headquarters.

•
Focused call point. We have historically directed our product offering and selling efforts towards the vascular surgeon, and estimate that in 2025 approximately 80% of our sales were from devices and cryopreserved tissue used by vascular surgeons. As vascular surgeons typically perform both open vascular surgeries and endovascular procedures, we sell devices in both the open and endovascular markets to the same end user. More recently we have begun to focus on adjacent market end users, such as cardiac surgeons, who can be served by our devices and tissue processing capabilities.

•
Low rivalry niche segments. We seek to build and maintain leading positions in niche segments, which we define as under $400 million in annual worldwide revenue. We believe that the relative lack of focus on these segments by larger companies, as well as the differentiated features and consistent availability and quality of our products, enable higher selling prices and expanded market presence.

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

**Present:** meta.json, form4_summary.md, 8-K_2026-08-04_2-02-results.md, 10-K_2026-02-26_item7_mdna.md, 10-K_2026-02-26_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
