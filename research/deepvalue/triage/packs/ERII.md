# Triage pack — ERII · Energy Recovery, Inc.

_Generated 2026-09-04 17:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** ERII · **Name:** Energy Recovery, Inc.
- **CIK:** 0001421517
- **SIC:** 3559 — Special Industry Machinery, NEC
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/ERII

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Energy Recovery, Inc.
- **CIK:** 1,421,517 · **SIC:** 3559 (Special Industry Machinery, NEC) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 7.65 |
| mktcap | $390.5M |
| ev | $329.1M |
| ev_ebit | 13.8x |
| fcf | $17.4M |
| fcf_yield | 4.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 17.0% |
| net_debt | -$61.4M |
| net_debt_ebit | -2.6x |
| cash | $61.4M |
| ltd | $0.00 |
| equity | $172.5M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $135.0M |
| revenue_prior | $144.9M |
| rev_growth | -6.9% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $23.9M |
| net_income | $23.0M |
| cfo | $18.8M |
| capex | $1.3M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -4.0% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 51,044,875 |
| shares_py | 53,198,386 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -37.2% |
| r6m | -28.7% |
| off_52w_high | -57.8% |
| adv20 | $8.1M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.45 |
| r_ev_ebit | 0.62 |
| r_roic | 0.84 |
| r_rev_growth | 0.14 |
| r_buyback | 0.85 |
| score | 0.58 |

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
| rank | 165 |

**Screen rationale:** high ROIC 17.0%; buying back stock -4.0%; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **51,044,875** (CY2026Q2I) vs **53,198,386** prior year (CY2025Q2I)
- Change: **-4.0%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-13** — Item 5.02 (officer / director change or comp arrangement): On July 9, 2026, the Board of Directors (the "Board") of Energy Recovery, Inc (the "Registrant") appointed Mr. John Mitchell to its Board.
- **2026-06-11** — Item 5.02 (officer / director change or comp arrangement): On May 28, 2026, Energy Recovery, Inc. (the "Company") filed a Current Report on Form 8-K (the "Original Report") to announce the appointment of Mr. Alex Buehler as the Company's Interim President and Chief Executive Officer.
- **2026-05-28** — Item 5.02 (officer / director change or comp arrangement): On May 25, 2026, Mr. David Moon informed the Board of Directors (the "Board") of Energy Recovery, Inc. (the "Company") of his intention to accelerate his previously announced retirement and resign from all positions within the Company, including as President...
- **2026-05-06** — Item 5.02 (officer / director change or comp arrangement): On May 6, 2026, the Company announced that David Moon, President and Chief Executive Officer of the Company, has notified the Board of Directors (the "Board") of his intention to retire following the appointment of his replacement.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 31,180 sh / $266,107 vs sells 24,754 sh / $218,314 -> net $47,793 (BUYING).
Distinct insiders buying (code P): 2. Largest buy: TONDREAU PAMELA L. bought 20,000 sh @ $8.34 ($166,840) on 2026-05-13.

Form 4 filings parsed: 12; transaction rows: 16 (open-market buys 2, sales 4).

| code | rows |
|---|---|
| A | 6 |
| F | 2 |
| M | 2 |
| P | 2 |
| S | 4 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-05_2-02-results.md)

_Extraction: started at the first release heading, 'Energy Recovery Reports its Second Quarter 2026 Financial Results'; skipped 11 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (ex991earningsrelease2026-q2.htm)

Energy Recovery Reports its Second Quarter 2026 Financial Results

SAN LEANDRO, Calif. - August 5, 2026 – Energy Recovery, Inc. (Nasdaq:ERII) ("Energy Recovery", "Company", "we", and "our") today announced its financial results for the second quarter and six months ended June 30, 2026. Management has released a letter to shareholders reviewing business and financial updates from the second quarter and discussing our outlook for 2026. This letter is located under "News and Events" in the "Investors" section on the Energy Recovery website (https://ir.energyrecovery.com/news-events/shareholder-letters).

Second Quarter Highlights

• Revenue of $12.0 million, a decrease of $16.1 million, as compared to Q2'2025.

• Gross margin of 74.7%, as compared to gross margin of 64.0% in Q2'2025 primarily due to to indirect manufacturing costs and channel mix, partially offset by lower volume.

• Operating expenses of $14.8 million, a decrease of 10.0%, as compared to Q2'2025, primarily due to lower employee compensation costs, including stock-based compensation expense, and lower consulting costs, partially offset by restructuring charges incurred in Q2'2026.

• Loss from operations of $5.9 million, a decrease of $7.4 million as compared to income from operations of $1.5 million during Q2'2025, due primarily to lower revenue due to the war in Iran.

• Net loss of $3.2 million and adjusted EBITDA (1) loss of $2.6 million.

• Cash and investments of $98.1 million, which includes cash, cash equivalents, and short- and long-term investments.

Financial Highlights

Quarter to Date | Year to Date
Q2'2026 | Q2'2025 | vs. Q2'2025 | 2026 | 2025 | 2026 vs. 2025
(In millions, except net income (loss) per share, percentages and basis points)
Revenue | $12.0 | $28.1 | down 57% | $21.7 | $36.1 | down 40%
Gross margin | 74.7% | 64.0% | up 1070 bps | 53.7% | 62.1% | down 840 bps
Operating margin | (49.0%) | 5.3% | NM | (95.6%) | (30.7%) | NM
Net income (loss) | ($3.2) | $2.1 | down 256% | ($15.4) | ($7.8) | down 97%
Diluted earnings (loss) per share | ($0.06) | $0.04 | down $0.10 | ($0.30) | ($0.14) | down $0.16
Effective tax rate | 19.1% | 14.0%
Cash provided by operations | $16.3 | $4.1 | $37.3 | $14.8

Non-GAAP Financial Highlights (1)

Quarter to Date | Year to Date
Q2'2026 | Q2'2025 | vs. Q2'2025 | 2026 | 2025 | 2026 vs. 2025
(In millions, except adjusted net income (loss) per share, percentages and basis points)
Adjusted operating margin | (30.4%) | 12.2% | down 4260 bps | (54.0%) | (17.4%) | NM
Adjusted net income (loss) | ($1.4) | $3.7 | down 136% | ($7.1) | ($3.3) | down 116%
Adjusted earnings (loss) per share | ($0.03) | $0.07 | down $0.10 | ($0.14) | ($0.06) | down $0.08
Adjusted EBITDA | ($2.6) | $4.4 | ($9.7) | ($4.4)
Free cash flow | $15.4 | $4.0 | $35.7 | $14.5

(1) Refer to the sections "Use of Non-GAAP Financial Measures" and "Reconciliation of Non-GAAP Financial Measures" for definitions of our non-GAAP financial measures and reconciliations of GAAP to non-GAAP amounts, respectively.

NM Not Meaningful

LIVE CONFERENCE Q&A CALL:

Wednesday, August 5, 2026, 2:00 PM PT / 5:00 PM ET

US / Canada Toll-Free: +1 (877) 709-8150

Local / International Toll: +1 (201) 689-8354

CONFERENCE Q&A CALL REPLAY:

Available approximately three hours after conclusion of the live call.

Expiration: Saturday, September 5, 2026

US / Canada Toll-Free: +1 (877) 660-6853

Local / International Toll: +1 (201) 612-7415

Access code: 13760218

Investors may also access the live call and the replay over the internet on the "Events" page of the Company's website located at https://ir.energyrecovery.com/news-events/ir-calendar.

Disclosure Information

Energy Recovery uses the investor relations section on its website as means of complying with its disclosure obligations under Regulation FD. Accordingly, investors should monitor Energy Recovery's investor relations website in addition to following Energy Recovery's press releases, SEC filings, and public conference calls and webcasts.

About Energy Recovery

Energy Recovery (Nasdaq: ERII) designs and manufactures world-class energy-saving technology for critical infrastructure that communities rely on every day, driving a more resilient and sustainable future. Grounded in more than 30 years of leadership in the desalination industry, today we use our proprietary pressure exchanger technology to help customers in multiple industries improve their operations and lower their emissions. Headquartered in the San Francisco Bay Area, we operate manufacturing and R&D facilities throughout California, with sales and on-site technical support available globally. For more information, please visit www.energyrecovery.com

Contact

Investor Relations

ir@energyrecovery.com

ENERGY RECOVERY, INC.

CONDENSED CONSOLIDATED BALANCE SHEETS

(Unaudited)

June 30, 2026 | December 31, 2025
(In thousands)
ASSETS
Cash, cash equivalents and investments | 98,074 | 83,283
Accounts receivable and contract assets | 14,237 | 78,286
Inventories, net | 38,242 | 24,260
Prepaid expenses and other assets | 3,888 | 3,416
Property, equipment and operating leases | 19,298 | 20,635
Goodwill | 11,128 | 12,790
Deferred tax assets and other assets | 12,869 | 8,844
TOTAL ASSETS | 197,736 | 231,514
LIABILITIES AND STOCKHOLDERS' EQUITY
Liabilities
Accounts payable, accrued expenses, and other liabilities, current | 14,791 | 13,784
Contract liabilities and other liabilities, non-current | 2,234 | 2,109
Lease liabilities | 8,233 | 9,429
Total liabilities | 25,258 | 25,322
Stockholders' equity | 172,478 | 206,192
TOTAL LIABILITIES AND STOCKHOLDERS' EQUITY | 197,736 | 231,514

ENERGY RECOVERY, INC.

CONDENSED CONSOLIDATED STATEMENTS OF OPERATIONS

(Unaudited)

Three Months Ended June 30, | Six Months Ended June 30,
2026 | 2025 | 2026 | 2025
(In thousands, except per share data)
Revenue | 11,996 | 28,051 | 21,702 | 36,116
Cost of revenue | 3,039 | 10,097 | 8,411 | 13,704
Restructuring - inventory reserve | — | — | 1,632 | —
Gross profit | 8,957 | 17,954 | 11,659 | 22,412
Operating expenses
General and administrative | 6,801 | 7,669 | 13,256 | 16,243
Sales and marketing | 4,336 | 5,360 | 9,455 | 10,266
Research and development | 2,849 | 3,451 | 5,638 | 6,452
Restructuring charges | 855 | — | 2,391 | 539
Impairment of goodwill | — | — | 1,662 | —
Total operating expenses | 14,841 | 16,480 | 32,402 | 33,500
Income (loss) from operations | (5,884) | 1,474 | (20,743) | (11,088)
Other income, net | 802 | 914 | 1,635 | 1,993
Income (loss) before income taxes | (5,082) | 2,388 | (19,108) | (9,095)
Provision for (benefit from) income taxes | (1,884) | 334 | (3,659) | (1,269)
Net income (loss) | (3,198) | 2,054 | (15,449) | (7,826)
Net income (loss) per share
Basic | (0.06) | 0.04 | (0.30) | (0.14)
Diluted | (0.06) | 0.04 | (0.30) | (0.14)
Number of shares used in per share calculations
Basic | 51,463 | 54,257 | 52,058 | 54,578
Diluted | 51,463 | 54,486 | 52,058 | 54,578

ENERGY RECOVERY, INC.

CONDENSED CONSOLIDATED STATEMENTS OF CASH FLOWS

(Unaudited)

Six Months Ended June 30,
2026 | 2025
(In thousands)
Cash flows from operating activities:
Net loss | (15,449) | (7,826)
Non-cash adjustments | 4,979 | 4,706
Net cash provided by operating assets and liabilities | 47,813 | 17,944
Net cash provided by operating activities | 37,343 | 14,824
Cash flows from investing activities:
Net investment in marketable securities | (1,303) | 33,882
Capital expenditures | (1,689) | (326)
Proceeds from sales of fixed assets | 13 | 10
Net cash (used in) provided by investing activities | (2,979) | 33,566
Cash flows from financing activities:
Net proceeds from issuance of common stock | 132 | 1,459
Tax payment for employee shares withheld | (682) | (476)
Repurchase of common stock and net excise tax activity | (20,432) | (22,009)
Net cash used in financing activities | (20,982) | (21,026)
Effect of exchange rate differences | (20) | 60
Net change in cash, cash equivalents and restricted cash | 13,362 | 27,424
Cash, cash equivalents and restricted cash, end of period | 61,438 | 57,181

ENERGY RECOVERY, INC.

SUPPLEMENTAL FINANCIAL INFORMATION

(Unaudited)

Channel Revenue

Three Months Ended June 30, | Six Months Ended June 30,
2026 | 2025 | vs. 2025 | 2026 | 2025 | vs. 2025
(In thousands, except percentages)
Original equipment manufacturer | 5,178 | 8,357 | down 38% | 11,766 | 12,358 | down 5%
Aftermarket | 4,112 | 4,892 | down 16% | 6,866 | 8,920 | down 23%
Megaproject | 2,706 | 14,802 | down 82% | 3,070 | 14,838 | down 79%
Total revenue | 11,996 | 28,051 | down 57% | 21,702 | 36,116 | down 40%

Segment Activity

Three Months Ended June 30,
2026 | 2025
Desalination | Wastewater | Corporate and Other | Total | Desalination | Wastewater | Corporate and Other | Total
(In thousands)
Revenue | 11,483 | 513 | — | 11,996 | 25,500 | 2,339 | 212 | 28,051
Cost of revenue | 2,781 | 258 | — | 3,039 | 9,259 | 667 | 171 | 10,097
Restructuring - inventory reserve | — | — | — | — | — | — | — | —
Gross profit | 8,702 | 255 | — | 8,957 | 16,241 | 1,672 | 41 | 17,954
Operating expenses
General and administrative | 1,025 | 872 | 4,904 | 6,801 | 788 | 535 | 6,346 | 7,669
Sales and marketing | 2,453 | 1,209 | 674 | 4,336 | 2,183 | 1,097 | 2,080 | 5,360
Research and development | 2,391 | 262 | 196 | 2,849 | 1,370 | 234 | 1,847 | 3,451
Restructuring charges | — | — | 855 | 855 | — | — | — | —
Total operating expenses | 5,869 | 2,343 | 6,629 | 14,841 | 4,341 | 1,866 | 10,273 | 16,480
Operating income (loss) | 2,833 | (2,088) | (6,629) | (5,884) | 11,900 | (194) | (10,232) | 1,474
Other income, net | 802 | 914
Income (loss) before income taxes | (5,082) | 2,388

Six Months Ended June 30,
2026 | 2025
Desalination | Wastewater | Corporate and Other | Total | Desalination | Wastewater | Corporate and Other | Total
(In thousands)
Revenue | 20,390 | 1,114 | 198 | 21,702 | 33,259 | 2,644 | 213 | 36,116
Cost of revenue | 7,723 | 628 | 60 | 8,411 | 12,641 | 846 | 217 | 13,704
Restructuring - inventory reserve | — | — | 1,632 | 1,632 | — | — | — | —
Gross profit (loss) | 12,667 | 486 | (1,494) | 11,659 | 20,618 | 1,798 | (4) | 22,412
Operating expenses
General and administrative | 1,781 | 1,853 | 9,622 | 13,256 | 1,633 | 1,263 | 13,347 | 16,243
Sales and marketing | 4,938 | 2,372 | 2,145 | 9,455 | 4,291 | 2,134 | 3,841 | 10,266
Research and development | 4,007 | 398 | 1,233 | 5,638 | 2,219 | 563 | 3,670 | 6,452
Restructuring charges | 335 | 18 | 2,038 | 2,391 | 107 | 103 | 329 | 539
Impairment of goodwill | — | — | 1,662 | 1,662 | — | — | — | —
Total operating expenses | 11,061 | 4,641 | 16,700 | 32,402 | 8,250 | 4,063 | 21,187 | 33,500
Operating income (loss) | 1,606 | (4,155) | (18,194) | (20,743) | 12,368 | (2,265) | (21,191) | (11,088)
Other income, net | 1,635 | 1,993
Income before income taxes | (19,108) | (9,095)

Stock-based Compensation

Three Months Ended June 30, | Six Months Ended June 30,
2026 | 2025 | 2026 | 2025
(In thousands)
Stock-based compensation expense charged to:
Cost of revenue | 145 | 148 | 243 | 296
General and administrative | 429 | 728 | 1,398 | 1,598
Sales and marketing | 582 | 701 | 1,253 | 1,380
Research and development | 230 | 359 | 455 | 625
Total stock-based compensation expense | 1,386 | 1,936 | 3,349 | 3,899

ENERGY RECOVERY, INC.

RECONCILIATION OF NON-GAAP FINANCIAL MEASURES (1)

(Unaudited)

This press release includes certain non-GAAP financial information because we plan and manage our business using such information. The following table reconciles the GAAP financial information to the non-GAAP financial information.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-25_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

Overview

Our reportable operating segments consist of the Water and Emerging Technologies segments. These segments are based on the

industries in which the technology solutions are sold, the type of energy recovery device or other technology sold and the related solution and

service or, in the case of emerging technologies, where revenues from new and/or potential devices utilizing our pressure exchanger

technology can be brought to market. Other factors for determining the reportable operating segments include the manner in which

management evaluates the performance of the Company combined with the nature of the individual business activities. In addition, our

corporate operating expenses include expenditures in support of the water and emerging technologies segments, as well as R&D

expenditures applicable to potential future industry verticals, or enabling technologies that could benefit either or both existing business units .

On February 25, 2026 , we decided to wind down operations of the CO 2 retail grocery business within our Emerging Technologies

segment due to a fundamental change in the outlook of the business. See Note 13 , " Subsequent Events ," of the Notes for further discussion

regarding the wind down.

Global Economic and Political Environment Considerations

The markets for our products are dynamic and constantly evolving. Our products are sold in numerous countries worldwide, with a

large percentage of our sales generated outside the U.S., specifically in the Middle East, Africa and Asia markets which provide a significant

portion of our total revenue. Therefore, we are exposed to and impacted by global macroeconomic factors, U.S. and foreign government

policies and foreign exchange fluctuations. There is uncertainty surrounding macroeconomic factors in the U.S. and globally characterized by

the supply chain environment, inflationary pressure, rising interest rates, and labor shortages. These global macroeconomic factors, coupled

with the U.S. political climate, political unrest internationally, and known conflicts in Europe and the Middle East, have created global

economic and political uncertainty, and have impacted demand for certain of our products. While the impact and longevity of these factors

remain uncertain, we are constantly evaluating the extent to which these factors will impact our business, financial condition or results of

operations.

Over the long-term, demand for our energy recovery devices could correlate to global macroeconomic and geopolitical factors. Any

disruption to the economic factors and regulations in these regions, which remain uncertain, may adversely affect our results of operations

and financial condition.

Refer to Part I, Item 1, " Business ," and Part I, Item 1A, " Risk Factors ," in this Annual Report on Form 10-K for further discussion of

these trends and other risks.

Results of Operations

A discussion regarding our financial condition and results of operations for the year ended December 31, 2024 , compared to the year

ended December 31, 2023 , can be found under Item 7 in our Annual Report on Form 10-K for the year ended December 31, 2024 , filed with

the SEC on February 26, 2025 , which is available free of charge on the SEC's website at http://www.sec.gov and at our investor relations

website ( https://ir.energyrecovery.com ).

Revenue

Energy Recovery, Inc. | 2025 Annual Report (Form 10-K) | 35

As a significant portion of our revenue is derived from large project contract deliveries that are up to 36 months from contract date,

there is no specific seasonality in our revenues to highlight.

We generally track our revenues by channels. The channels we recognize and channel definitions we utilize are as follows:

• Megaproject (" MPD ") channel: The MPD channel has been the main driver of our long-term growth as revenue from this channel

benefits from a growing number of projects as well as an increase in the capacity of these projects in some cases. MPD projects

are large-scale in nature and generally have shipment timelines from 16 to 36 months from contract date. Recognition of

revenue is dependent on customers' project timing and execution of these projects.

• Original Equipment Manufacturer (" OEM ") channel: The OEM channel reflects sales to a wide variety of industries in the

desalination, wastewater, and the refrigeration markets. This channel contains projects smaller in size and revenue, and of

shorter duration compared to those projects in the MPD channel.

• Aftermarket (" AM ") channel: The AM channel represents support and services rendered to our installed customer base. AM

revenue generally fluctuates from year-to-year and is dependent on our customers' timing of product upgrades, as well as their

replenishment of spare parts and supplies.

Revenue by Channel Customers

Years Ended December 31,
2025 | 2024
Revenue | % of Revenue | Revenue | % of Revenue | Change
(In thousands, except percentages)
Megaproject | $ 82,885 | 61% | $ 95,399 | 66% | $ (12,514) | (13%)
Original equipment manufacturer | 31,940 | 24% | 31,525 | 22% | 415 | 1%
Aftermarket | 20,162 | 15% | 18,024 | 12% | 2,138 | 12%
Total revenue | $ 134,987 | 100% | $ 144,948 | 100% | $ (9,961) | (7%)

Revenue Attributable to Primary Geographical Markets by Segments

Years Ended December 31,
2025 | 2024
Water | Emerging Technologies | Total | Water | Emerging Technologies | Total
(In thousands)
Middle East | $ 68,084 | $ 92 | $ 68,176 | $ 59,538 | $ 399 | $ 59,937
Africa | 15,010 | — | 15,010 | 30,731 | — | 30,731
Other | 51,608 | 193 | 51,801 | 54,041 | 239 | 54,280
Total revenue | $ 134,702 | $ 285 | $ 134,987 | $ 144,310 | $ 638 | $ 144,948

Year ended December 31, 2025 , as compared to the year ended December 31, 2024

Revenues associated with our Water segment represented 99% of total revenues during the years ended December 31, 2025 and

2024 . Revenues associated with our Emerging Technologies segment were immaterial.

The decrease in MPD revenue of $12.5 million was due primarily to lower shipments to the Africa and Asia markets, partially offset by

higher shipments of products to the Middle East and Europe markets.

The increase in OEM revenue of $0.4 million was primarily due:

• Desalination : The increase in revenue of $2.5 million was due primarily to higher shipments of products to the Asia market.

• Wastewater : The decrease in revenue of $2.1 million was due primarily to lower shipments of products to the Asia market.

The increase in AM revenue of $2.1 million was due primarily to higher shipments to the Asia and Middle East markets.

Energy Recovery, Inc. | 2025 Annual Report (Form 10-K) | 36

Revenues attributable to domestic and international sales

Revenues are primarily attributable to international sales and are concentrated in the Middle East and Africa. See Note 10 ,

" Concentrations – Revenue by Geographic Location and Country ," of the Notes for further discussion regarding our concentration of revenue

by geographic location .

Gross Profit and Gross Margin

Gross profit represents revenue less cost of revenue. Cost of revenue consists primarily of raw materials, personnel costs (including

stock-based compensation), manufacturing overhead, warranty costs, and depreciation expense.

Years Ended December 31,
2025 | 2024 | Change
(In thousands, except percentage and basis point)
Gross profit | $ 87,931 | $ 96,933 | $ (9,002)
Gross margin | 65.1 % | 66.9 % | (180) bps

The decrease in gross profit and gross margin for the year ended December 31, 2025 , as compared to the prior year, was due

primarily to lower sales volume spread over fixed costs, increased costs related to product and channel mix, pricing and tariffs, partially offset

by a decrease in indirect manufacturing costs during the year ended December 31, 2025 .

Operating Expenses

The total material changes of general and administrative ("G&A"), sales and marketing ("S&M") and R&D operating expenses for the

year ended December 31, 2025 , as compared to the comparable period in the prior year, are discussed within the following overall operating

expenditures, and the segment and corporate operating expenses discussions below.

Years Ended December 31,
2025 | 2024
Water | Emerging Technologies | Corporate | Total | Water | Emerging Technologies | Corporate | Total
(In thousands)
General and administrative | $ 5,686 | $ 2,350 | $ 21,733 | $ 29,769 | $ 8,127 | $ 3,821 | $ 21,126 | $ 33,074
Sales and marketing | 13,664 | 5,449 | 1,813 | 20,926 | 15,683 | 7,340 | 2,400 | 25,423
Research and development | 6,344 | 6,690 | — | 13,034 | 4,523 | 11,713 | — | 16,236
Restructuring charges | 105 | 47 | 161 | 313 | 1,147 | 832 | 497 | 2,476
Total operating expenses | $ 25,799 | $ 14,536 | $ 23,707 | $ 64,042 | $ 29,480 | $ 23,706 | $ 24,023 | $ 77,209

Year ended December 31, 2025 , as compared to the year ended December 31, 2024

Overall Operating Expenditures . Overall operating expenditures decrease d by $13.2 million , or (17.1%) . This decrease was due

primarily to a decrease in employee costs, such as employee compensation and stock-based compensation, as well as lower Emerging

Technologies segment development costs, facility expenses and restructuring charges, partially offse t by impairment costs associated with

the sublease of the Katy, Texas lease incurred during the year ended December 31, 2025 .

Water Segment. Water segment related operating expenses represented 40% and 38% of overall operating expenses during the

years ended December 31, 2025 and 2024 , respectively and decrease d by $3.7 million , or (12.5%) . This decrease was due primarily to

lower employee costs, including stock-based compensation costs, and lower restructuring charges.

Energy Recovery, Inc. | 2025 Annual Report (Form 10-K) | 37

Emerging Technologies Segment. Emerging Technologies segment related operating expenses represented 23% and 31% of overall

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-25_item1_business.md)

Item 1 — Business

Overview

Energy Recovery, Inc. (the "Company", "Energy Recovery", "we", "our" and "us") designs and manufactures world-class energy-saving

technology for critical infrastructure that communities rely on every day, driving a more resilient and sustainable future. Grounded in more

than 30 years of leadership in the desalination industry, today we use our proprietary pressure exchanger technology to help customers in

multiple industries improve their operations and lower their emissions.

We have been incorporated in the state of Delaware since 2001. Our corporate headquarters, principal research and development

(" R&D "), and manufacturing facility is located in San Leandro, California. In addition, we have manufacturing and warehouse space in Tracy,

California. W e have a global direct sales team and on-site technical support staff to service customers in the United States of America (the

"U.S.") , Europe, North, South and Latin America, the Middle East, Northern Africa, and Asia.

On February 25, 2026 , we decided to wind down operations of the CO 2 retail grocery business within our Emerging Technologies

segment due to a fundamental change in the outlook of the business. See Note 13 , " Subsequent Events ," of the Notes for further discussion

regarding the wind down.

Pressure Exchanger Technology

Our pressure exchanger technology platform is at the heart of many of our solutions. It is designed to efficiently capture and transfer

pressure energy, making commercial and industrial processes more efficient and environmentally sustainable, thereby lowering costs, saving

energy, and minimizing emissions. This versatile technology is applicable to a wide range of industries that utilize pressurized fluids,

including liquids and gas, and is ideal for a wide range of pressure ratings.

Our pressure exchanger technology acts like a fluid piston, efficiently transferring energy between high- and low-pressure liquid or gas

through continuously rotating ducts. Key to the operation of a pressure exchanger is the micron-level clearances between the rotor and the

pressure exchanger's stationary components, including the sleeve and the end covers. Fluid circulating within this clearance acts as a

lubricated bearing, minimizing frictional losses and wear for an extremely efficient exchange of pressure energy. 

Energy Recovery, Inc. | 2025 Annual Report (Form 10-K) | 2

The original product application of our pressure exchanger technology, the PX ® Pressure Exchanger ® (" PX ") energy recovery device

was a major contributor to the advancement of seawater reverse osmosis desalination ("SWRO") globally, addressing "energy intensity",

which is a key pain point for the industry. The PX, which we believe is today's industry standard in energy recovery in desalination,

establishes a value proposition by reducing energy use by up to 60% in SWRO facilities. It is this significant savings that allowed SWRO to

supplant thermal desalination as today's desalination technology of choice. The PX, which uses no electricity, operates at up to 98%

efficiency and is designed to operate with no scheduled maintenance. Today we continue to push the boundaries of our core technology to

handle different operating environments and industrial applications, such as wastewater and carbon dioxide ("CO 2 ") refrigeration, and deliver

reliable, high-performance solutions that generate cost savings and increase energy efficiency for our customers.

Energy Recovery, Inc. | 2025 Annual Report (Form 10-K) | 3

Water Treatment

Markets

The need for clean water and energy optimization around the world is intensifying, driven by population growth, industrialization, rapid

urbanization, pollution, and climate change. Apart from seasonal variations, the attainable supply of fresh water generally remains fixed and

is already decreasing in some geographic areas, as we believe that the reliability of rainfall grows more erratic in many geographies, water

levels drop in rivers and aquifers, and rising oceans encroach on historically fresh water sources near the coasts. It has been projected by

the United Nations General Assembly that by 2030, global freshwater demand will exceed freshwater supply by 40%. These trends make the

markets we serve, such as desalination and wastewater treatment, increasingly critical to meet growing global water demand. Our goal is to

lower the costs and environmental impact associated with water production and treatment in the desalination and wastewater markets,

respectively. In addition, we help our customers and the end user in their sustainability compliance goals.

Reverse osmosis (" RO ") is the preferred technology in the vast majority of desalination facilities and growing in importance in

wastewater applications. As an industry leader in energy recovery device s, we deliver efficient, scalable solutions for recovering otherwise

wasted energy in the RO process, thereby helping our customers lower their operating costs and reduce carbon emissions.

Desalination

Worldwide seawater desalination plants using our products produce over 43 million cubic meters of water per day (" m 3 /day "). As

water scarcity grows in communities across the globe, we are proud of our impact in enabling more affordable, sustainable access to this vital

resource.

Typical Process Flow Diagram

* Main pump size reduced by up to 60% compared to a SWRO process not using any energy recovery device.

Energy Recovery, Inc. | 2025 Annual Report (Form 10-K) | 4

Seawater Reverse Osmosis Desalination . Energy intensive pumps are used to pressurize f eed wate rs with varying concentrations of

salts, minerals and contaminants, which is then pumped through a semi-permeable membrane to achieve the desired water quantity and

quality. This process results in fresh water, suitable for potable, agricultural and industrial use and a highly concentrated and pressurized

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-25_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-25_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-25_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-05_2-02-results.md, 10-K_2026-02-25_item7_mdna.md, 10-K_2026-02-25_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
