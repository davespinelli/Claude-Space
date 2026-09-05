# Triage pack — SRTA · Strata Critical Medical, Inc.

_Generated 2026-09-05 01:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** SRTA · **Name:** Strata Critical Medical, Inc.
- **CIK:** 0001779128
- **SIC:** 8000 — Services-Health Services
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/SRTA

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Strata Critical Medical, Inc.
- **CIK:** 1,779,128 · **SIC:** 8000 (Services-Health Services) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

> **EARNINGS QUALITY FLAG — one-off items likely.**
> net income more than 3x operating income.
> Reported net income is not supported by the operating engine that is supposed to produce it (typical causes: gains on sale, legal settlements, deferred-tax valuation-allowance releases, bargain-purchase gains). Reconcile net income to operating income in the earnings release (section 7) before treating any earnings-based metric here as repeatable.

**Valuation**

| metric | value |
|---|---|
| price | 5.37 |
| mktcap | $475.1M |
| ev | $458.7M |
| ev_ebit | n/a |
| fcf | -$58.5M |
| fcf_yield | -12.3% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -6.7% |
| net_debt | -$16.3M |
| net_debt_ebit | n/a |
| cash | $16.3M |
| ltd | $0.00 |
| equity | $279.3M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $197.1M |
| revenue_prior | $146.8M |
| rev_growth | 34.3% |
| rev_growth_note | n/a |
| eq_flag | net income more than 3x operating income |
| ebit | -$22.4M |
| net_income | $41.3M |
| cfo | -$48.9M |
| capex | $9.6M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 8.3% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 88,466,806 |
| shares_py | 81,695,605 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 41.0% |
| r6m | 13.1% |
| off_52w_high | -17.0% |
| adv20 | $5.3M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.07 |
| r_ev_ebit | 0.00 |
| r_roic | 0.17 |
| r_rev_growth | 0.91 |
| r_buyback | 0.14 |
| score | 0.31 |

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
| rank | 406 |

**Screen rationale:** revenue +34.3%; debt data missing (net cash unverified); 12-1 momentum 41.0%; EARNINGS QUALITY: net income more than 3x operating income — one-off items likely


## 3. Share count trend

- Shares outstanding: **88,466,806** (CY2026Q2I) vs **81,695,605** prior year (CY2025Q2I)
- Change: **8.3%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-03 among the 3 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 41,417 sh / $242,507 -> net $-242,507 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 19 (open-market buys 0, sales 3).

| code | rows |
|---|---|
| A | 12 |
| F | 4 |
| S | 3 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-04_2-02-results.md)

_Extraction: started at the first release heading, 'Second Quarter Ended June 30, 2026 Financial Highlights: Q2 2026 vs. Q'; skipped 7 forward-looking-statement block(s); 30 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (srta-earningreleasexq22026.htm)

Second Quarter Ended June 30, 2026 Financial Highlights: Q2 2026 vs. Q2 2025

▪ Total revenue increased 60.7% to $72.5 million in Q2 2026 versus $45.1 million in the prior year period driven by organic growth in Logistics, the addition of our Clinical business through the acquisition of Keystone in Q3 2025 and the contribution from Clinical acquisitions completed during Q2 2026.

▪ Logistics revenue, which represents the Company's organic revenue growth, increased 6.9% to $48.2 million in Q2 2026 versus $45.1 million in the prior year period driven primarily by higher Air revenue. Compared to the year ago period, strength in Organ Procurement Organization customers and softness in Transplant Center customers drove shorter trip distances, muting overall revenue in the period. The Clinical business continued to drive growth in Logistics revenue compared to the prior year period.

▪ Gross profit increased 68.9% to $15.2 million in Q2 2026 versus $9.0 million in the prior year period driven by the addition of our Clinical business and the contribution from Clinical acquisitions completed during Q2 2026, partially offset by a modest decline in Logistics gross profit.

▪ Gross margin increased 100 basis points to 21.0% in Q2 2026 versus 20.0% in the prior year period driven primarily by the positive mix impact from the addition of our Clinical business and the contribution from Clinical acquisitions completed during Q2 2026, partially offset by a decline in Logistics gross margin.

▪ Logistics gross profit decreased 1.3% to $8.9 million in Q2 2026 versus $9.0 million in the prior year period. Logistics gross margin of 18.4% in Q2 2026 decreased 160 basis points versus 20.0% the prior year period driven primarily by an increase in the fuel surcharge, fuel costs, customer mix, modestly lower owned fleet profitability and lower ground margins.

Given that the acquisition of our Clinical business as well as the sale of our Passenger business occurred in Q3 2025, and the recent Clinical acquisitions completed during Q2 2026, year-over-year comparisons of Clinical metrics, Net Income, Adjusted SG&A, Adjusted EBITDA and cash flow are not meaningful. Please see below for sequential comparisons for these metrics.

Second Quarter Ended June 30, 2026 Financial Highlights: Q2 2026 vs. Q1 2026

▪ Clinical revenue rose 22.6% to $24.3 million in Q2 2026 versus $19.8 million in Q1 2026. Excluding Clinical acquisitions completed during Q2 2026, Clinical revenue rose 15.1% in Q2 2026 versus Q1 2026 driven primarily by Transplant Clinical revenue, which rose 23.8% and Other Clinical revenue, that rose 6.5%.

▪ Clinical gross profit increased 27.8% to $6.3 million in Q2 2026 versus $5.0 million in Q1 2026. Clinical gross margin increased to 26.1% in Q2 2026 versus 25.0% in Q1 2026.

▪ Total Selling, General and Administrative expenses decreased $1.6 million to $14.0 million in Q2 2026 versus $15.6 million in Q1 2026. Adjusted SG&A (1) decreased $0.1 million to $9.1 million in Q2 2026 versus $9.2 million in Q1 2026.

▪ Net income from continuing operations decreased $12.9 million to $(10.5) million in Q2 2026 versus $2.4 million in Q1 2026 primarily due to $5.0 million of accelerated trademark amortization related to our brand integration and a $10.5 million decrease in other non-operating income related to the non-cash revaluation of transaction earn-out liabilities.

▪ Adjusted EBITDA (1) was $7.9 million in Q2 2026 versus $6.4 million in Q1 2026. Adjusted EBITDA margin rose to 10.9% in Q2 2026 versus 9.5% in Q1 2026. The 140 basis points increase in Adjusted EBITDA margin versus Q1 2026 was driven by the increase in Clinical gross margin and the mix shift to Clinical partially offset by the reduction in Logistics gross margin.

▪ Cash flow from operating activities was $5.7 million in Q2 2026. In Q2 2026, the $2.2 million difference between Adjusted EBITDA and operating cash flow was driven primarily by the $1.7 million increase in working capital related to the timing of expenses.

(1) See "Use of Non-GAAP Financial Information" and "Key Metrics and Non-GAAP Financial Information" sections attached to this release for an explanation of Non-GAAP measures used and reconciliations to the most directly comparable GAAP financial measure.

▪ Capital expenditures of $2.8 million in Q2 2026 were driven primarily by aircraft capitalized maintenance.

▪ Free Cash Flow, before aircraft and engine acquisitions (1) was $2.9 million in Q2 2026.

▪ Ended Q2 2026 with $22.8 million in cash and short term investments.

Business Highlights and Recent Updates

▪ In late April 2026, we completed the acquisition of Ohio Valley Perfusion Associates, a regional provider of perfusion services to cardiac surgery programs in Ohio and Pennsylvania, strengthening our cardiac care footprint in the region.

▪ In early June 2026, we completed the acquisition of Louisville Perfusion Services ("LPS"), a regional provider of perfusion and blood management services to cardiac surgery programs in Kentucky.

▪ In late June 2026, we completed the acquisition of Heart and Lung Transplant National Recovery Program ("HLT-NRP"), a provider of transplant surgical recovery services in the United States. HLT-NRP strengthens and adds scale to our organ recovery platform by increasing our network of experienced transplant surgeons available to complete recoveries, especially in key markets such as Florida and California.

▪ In late July 2026, we signed an agreement to take over Statline's Transplant Center Organ Placement customer relationships on a rolling basis over the next year, bringing us long-term contracted attachment points with up to eight new customers that we believe could lead to incremental clinical or logistics business over time.

Financial Outlook

Today, we are updating our 2026 guidance:

▪ Revenue of $285-295 million ( previously: $260-275 million )

▪ Adjusted EBITDA (2) of $33-35 million ( previously: $29-33 million )

▪ Free cash flow, before aircraft and engine acquisitions (2) of: $15-22 million ( previously: $15-22 million )

Pro forma, assuming all acquisitions completed in 2026 closed on January 1 2026, our 2026 revenue and Adjusted EBITDA guidance would be approximately:

▪ Revenue of $295-305 million

▪ Adjusted EBITDA (2) of $36-38 million

Conference Call

The Company will conduct a conference call starting at 8:00 a.m. ET on August 4, 2026 to discuss the results for the second quarter ended June 30, 2026.

A live audio-only webcast of the call may be accessed from the Investor Relations section of the Company's website at https://ir.stratacritical.com/. An archived replay of the call will be available on the Investor Relations section of the Company's website for one year.

(1) See "Use of Non-GAAP Financial Information" and "Key Metrics and Non-GAAP Financial Information" sections attached to this release for an explanation of Non-GAAP measures used and reconciliations to the most directly comparable GAAP financial measure.

(2) We have not reconciled the forward-looking Adjusted EBITDA and free cash flow, before aircraft and engine acquisitions guidance included above to the most directly comparable GAAP measures because this cannot be done without unreasonable effort due to the variability and low visibility with respect to certain costs, the most significant of which are, with respect to Adjusted EBITDA, incentive compensation (including stock-based compensation), transaction-related expenses, and certain fair value measurements, which are potential adjustments to future earnings, and with respect to free cash flow, before aircraft and engine acquisitions, changes in operating assets and liabilities. We expect the variability of these items to have a potentially unpredictable, and a potentially significant, impact on our future GAAP financial results.

Use of Non-GAAP Financial Information

Strata believes that the non-GAAP measures discussed below, viewed in addition to and not in lieu of our reported U.S. generally accepted accounting principles ("GAAP") results, provide useful information to investors by providing a more focused measure of operating results, enhance the overall understanding of past financial performance and future prospects, and allow for greater transparency with respect to key metrics used by management in its financial and operational decision making. The non-GAAP measures presented herein may not be comparable to similarly titled measures presented by other companies. Adjusted EBITDA, Adjusted SG&A, Free Cash Flow, Free Cash Flow before aircraft and engine acquisitions, and Clinical revenue, excluding acquisitions, have all been reconciled to the nearest GAAP measure in the tables within this press release.

Adjusted EBITDA – Strata reports Adjusted EBITDA, which is a non-GAAP financial measure. Strata defines Adjusted EBITDA as net income (loss) from continuing operations adjusted to exclude: (1) depreciation and amortization; (2) stock-based compensation; (3) change in fair value of warrant liabilities and other assets and liabilities; (4) interest income and expense; (5) income tax; (6) impairment of intangible assets or property and equipment; and (7) certain other non-recurring items that management does not believe are indicative of the Company's ongoing operating performance and would impact the comparability of results between periods.

Adjusted SG&A – Strata defines Adjusted selling, general and administrative ("SG&A") expenses as SG&A adjusted to exclude: (1) depreciation; (2) stock-based compensation; (3) impairment of property and equipment; and (4) other non-cash items and certain other non-recurring items that management does not believe are indicative of the Company's ongoing operating performance that would impact the comparability of results between periods.

Free Cash Flow, and Free Cash Flow before aircraft and engines acquisitions – Strata defines Free Cash Flow as net cash provided by / (used in) operating activities less capital expenditures and capitalized software development costs (net of proceeds from disposals). Free Cash Flow before aircraft and engines acquisitions is defined as Free Cash Flow excluding cash outflows related to aircraft and engines acquisitions. Strata believes these measures provide valuable insights into the Company's cash-generating capacity. In particular, Free Cash Flow before aircraft and engines acquisitions highlights the cash generated by Strata's continuing operations prior to the impact of aircraft and engines acquisitions, which are discretionary and strategic in nature.

Clinical revenue, excluding Clinical acquisitions that closed in Q2 2026 – Strata defines Clinical revenue, excluding Clinical acquisitions that closed in Q2 2026, as total Clinical revenue, including Transplant Clinical and Other Clinical revenue, less revenue attributable to businesses acquired during the period presented. Strata believes this measure is useful to investors because it facilitates the evaluation of organic period-over-period growth in the Clinical segment by excluding growth attributable to acquired businesses.

Financial Results

STRATA CRITICAL MEDICAL, INC.

Condensed Consolidated Balance Sheets

(in thousands, except share data, unaudited)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-03_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

Strata Critical Medical, Inc. (f/k/a Blade Air Mobility, Inc.) ("Strata" or the "Company") is a time-critical logistics and medical services provider to the United States healthcare industry. The Company operates one of the nation's largest air transport and surgical services networks for transplant hospitals and organ procurement organizations, offering an integrated "one call" solution for donor organ recovery. Strata's core services include air and ground logistics, surgical organ recovery, organ placement and normothermic regional perfusion for the transplant industry, as well as perfusion staffing and equipment solutions for cardiovascular surgery centers, offered under the Trinity Medical Solutions ("Trinity") and Keystone brands.

Strata's mission is to increase the number of organs that are successfully transplanted while leveraging the Company's expertise and resources to provide other medical and logistics services to a broader customer base. Strata's goals are closely aligned with those of all participants in the transplant ecosystem, including transplant centers, regulators, Organ Procurement Organizations ("OPOs") and other service providers. We believe that, by working with Strata, industry participants can save money, save more lives and operate more efficiently.

Beginning with the fourth quarter of 2025, following the integration of Keystone, Strata operates across two segments: Logistic and Clinical (see Note 11, to the consolidated financial statements included in this Annual Report on form 10-K for further information on reportable segments), both offering services related to organ transplant and the broader healthcare industry. All of Strata's services are provided to transplant centers, organ procurement organizations, hospitals or other businesses that pay the Company directly. Strata provides:

Logistics Segment

Strata's Logistics segment is marketed under the Trinity brand name and includes the following:

• Air Logistics – Air transportation of human organs for transplant as well as related staff, equipment, blood samples, and tissue samples. Service is typically provided on fixed wing aircraft operating specifically for each individual organ. Strata also offers on-board couriers for commercial flights and "next flight out" shipping coordination.

• Ground Logistics – Ground transportation of human organs for transplant as well as related staff, equipment, blood samples, and tissue samples.

• Organ Placement – Administrative services related to the acceptance of potential donor organs for recipients and support coordinating with the transplant process.

Clinical Segment

Strata's Clinical segment is marketed under the Keystone brand name and includes the following:

Transplant Clinical

• Organ Recovery – Surgical procurement of donor organs.

• Normothermic Regional Perfusion ("NRP") – In situ perfusion of donor organs with oxygenated blood to improve clinical outcomes and enable functional assessment prior to recovery.

• Preservation - Operation of devices utilized to preserve organs prior to being transplanted into a recipient.

Other Clinical Services

• Cardiac Care – Cardiac perfusion, blood management & autotransfusion and disposables. Services are typically provided under contract with hospitals to support open-heart surgery procedures.

• Other – Extracorporeal Membrane Oxygenation ("ECMO") services, perfusion temporary staffing and equipment rental offered to healthcare providers.

Outlined below are recent material transactions impacting this Annual Report on Form 10-K.

Sale of Passenger business

On August 29, 2025, the Company completed the previously disclosed sale of its Passenger business to Joby Aero, Inc. ("Joby Buyer"), pursuant to an Equity Purchase Agreement, dated August 1, 2025 (the "Joby Purchase Agreement"). The Passenger business acquired by the Joby Buyer pursuant to the Joby Purchase Agreement consisted of the Company's business of offering, selling, promoting, marketing, planning, booking, brokering, coordinating and arranging the transportation of passengers on aircraft operated by other entities and related ground transportation services. The purchase price received by the Company upon the consummation of the transactions contemplated by the Joby Purchase Agreement was approximately $76.0 million based on the closing price per share of $14.27 of Joby Aviation Inc's ("Joby Aviation") common stock as of August 28, 2025), after giving effect to certain pre-closing adjustments and indemnity holdbacks pursuant to the terms of the Joby Purchase Agreement, consisting of 5,325,585 shares of Joby Aviation's common stock, par value $0.0001 per share (the "Buyer Shares"). The Company subsequently sold the Buyer Shares received in connection with closing for net proceeds of $70.2 million. The Company may receive up to an additional $35.0 million in consideration upon the satisfaction of certain financial performance and employee retention targets described in the Joby Purchase Agreement during the 12 and 18 months, respectively, following the closing of this transaction, payable in cash or Buyer Shares at Joby Buyer's election, as well as the release of up to $10.0 million in indemnity holdbacks. The number of Buyer Shares issued to the Company, if any, shall be based on the average of the daily volume-weighted average sales price per Buyer Share on the New York Stock Exchange for each of the ten consecutive trading days ending on and including the first trading day preceding the applicable measurement dates described in the Joby Purchase Agreement.

The sale qualified as a discontinued operation under ASC 205-20. The Passenger business acquired by Joby Buyer included all operations previously reported within the Passenger segment, as well as certain assets and activities previously

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The following table presents our consolidated statements of operations for the periods indicated:

Year Ended December 31,
2025 | % of Revenue | 2024 | % of Revenue
(in thousands, except share and per share data)
Revenue | 197,141 | 100% | 146,817 | 100%
Cost of revenue | 156,015 | 79% | 117,228 | 80%
Gross Profit | 41,126 | 21% | 29,589 | 20%
Operating expenses
Selling, general and administrative | 60,875 | 31% | 50,856 | 35%
Amortization of intangible assets | 2,604 | 1% | 1,258 | 1%
Total operating expenses | 63,479 | 32% | 52,114 | 35%
Operating loss from continuing operations | (22,353) | (22,525)
Other non-operating income (loss)
Interest income | 4,241 | 7,214
Change in fair value of warrant liabilities | 4,278 | (850)
Change in fair value of assets and other liabilities | (1,037) | —
Realized loss from sales of short-term investments | (5,195) | —
Total other non-operating income | 2,287 | 6,364
Loss from continuing operations before income taxes | (20,066) | (16,161)
Income tax expense (benefit) from continuing operations | — | —
Net loss from continuing operations | (20,066) | (16,161)
Net income (loss) from discontinued operations | 61,413 | (11,146)
Net income (loss) | 41,347 | (27,307)
Basic and diluted earnings (loss) per share
Continuing operations | (0.24) | (0.21)
Discontinued operations | 0.75 | (0.14)
Total basic and diluted earnings (loss) per share | 0.50 | (0.35)
Weighted-average number of shares outstanding, basic and diluted | 82,092,345 | 77,499,423

Comparison of Years Ended December 31, 2025 and 2024

Revenue

Disaggregated revenue by segment was as follows:

Year Ended December 31,
2025 | 2024 | % Change
(in thousands, except percentages)
Logistics
Logistics | 176,793 | 146,817 | 20.4 | %
Clinical
Transplant clinical | 8,964 | — | NM(1)
Other clinical | 11,384 | — | NM(1)
Total Clinical | 20,348 | — | NM(1)
Total revenue | 197,141 | 146,817 | 34.3 | %

(1) Percentage not meaningful.

For the years ended December 31, 2025 and 2024, revenue increased by $50.3 million or 34.3%, from $146.8 million in 2024 to $197.1 million in 2025.

Logistics revenue increased by $30.0 million, or 20.4% from $146.8 million in 2024 to $176.8 million in 2025, driven by growth in flight hours, ground transportation and revenue per trip. The increase in flight hours was attributable to both existing and new clients, with several major new contracted clients commencing operations in the second quarter of the year 2025.

Clinical revenue was $20.3 million in 2025, reflecting the acquisition of Keystone in mid-September 2025. There was no clinical revenue in 2024. Clinical revenue in 2025 was comprised of transplant clinical revenue of $9.0 million and other clinical revenue of $11.4 million.

Gross Profit and Gross Margin

Year Ended December 31,
2025 | 2024 | Change
(in thousands, except percentages)
Gross profit:
Logistics | 36,631 | 29,589 | 23.8 | %
Clinical | 4,495 | — | NM(1)
Total gross profit | 41,126 | 29,589 | 39.0 | %
Gross margin:
Logistics | 21 | % | 20 | %
Clinical | 22 | % | —
Total gross margin | 21 | % | 20 | %

(1) Percentage not meaningful.

For the years ended December 31, 2025 and 2024, Logistics gross profit increased by $7.1 million, or 23.8%, from $29.6 million in 2024 to $36.6 million in 2025, attributable to the 20.4% increase in revenue and an increase in gross margin from 20% to 21% attributable primarily to operational leverage in ground services with the expansion of ground hubs. For the year ended December 31, 2025, Clinical gross profit of $4.5 million was attributable to the acquisition of Keystone in mid-September 2025.

Total gross margin increased from 20% in 2024 to 21% in 2025, attributable primarily to the acquisition of Keystone in mid-September 2025, which operates at a higher average gross margin, as well as an improvement in Logistics gross margin, as discussed above.

Selling, General and Administrative

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-03_item1_business.md)

Part I.

Item 1. Business

Business Overview

Strata Critical Medical, Inc.(f/k/a Blade Air Mobility, Inc.) ("Strata" or the "Company") is a time-critical logistics and medical services provider to the United States healthcare industry. The Company operates one of the nation's largest air transport and surgical services networks for transplant hospitals and organ procurement organizations, offering an integrated "one call" solution for donor organ recovery. Strata's core services include air and ground logistics, organ placement, surgical organ recovery, normothermic regional perfusion and preservation for the transplant industry, as well as perfusion staffing and equipment solutions for cardiovascular surgery centers, offered under the Trinity Medical Solutions ("Trinity") and Keystone Perfusion Services LLC ("Keystone") brands.

Strata's mission is to increase the number of organs that are successfully transplanted while leveraging the Company's expertise and resources to provide other medical and logistics services to a broader customer base. Strata's goals are closely aligned with those of all participants in the transplant ecosystem, including transplant centers, regulators, Organ Procurement Organizations ("OPOs") and other service providers. We believe that, by working with Strata, industry participants can save money, save more lives and operate more efficiently by working with Strata.

Strata operates across two operating segments: Logistics and Clinical (see Note 11 to the consolidated financial statements included in this Annual Report on Form 10-K for further information on reportable segments), offering a variety of logistics and clinical services related to organ transplant and the broader healthcare industry. All of Strata's services are provided to transplant centers, organ procurement organizations, hospitals or other businesses that pay the Company directly. Strata provides:

Logistics Segment

Our Logistics segment is marketed under the Trinity brand name and includes the following:

• Air Logistics – Air transportation of human organs for transplant as well as related staff, equipment, blood samples, and tissue samples. Service is typically provided on fixed wing aircraft operating specifically for each individual organ. Strata also offers on-board couriers for commercial flights and "next flight out" shipping coordination.

• Ground Logistics – Ground transportation of human organs for transplant as well as related staff, equipment, blood samples and tissue samples.

• Organ Placement – Administrative services related to the acceptance of potential donor organs for recipients and support coordinating the transplant process.

Clinical Segment

Our Clinical segment is marketed under the Keystone brand name and includes the following:

Transplant Clinical

• Organ Recovery – Surgical procurement of donor organs.

• Normothermic Regional Perfusion ("NRP") – In situ perfusion of donor organs with oxygenated blood to improve clinical outcomes and enable functional assessment prior to recovery.

• Preservation – Operation of devices utilized to preserve organs prior to being transplanted into a recipient.

Other Clinical

• Cardiac Care – Cardiac perfusion, blood management & autotransfusion and disposables. Services are typically provided under contract with hospitals to support open-heart surgery procedures.

• Other – Extracorporeal Membrane Oxygenation (ECMO) services, perfusion temporary staffing and equipment rental offered to healthcare providers.

Our Business Model

Logistics Segment

We typically provide logistics services to transplant centers, organ procurement organizations and other businesses on a contractual basis including provisions stipulating that Strata will be the "first call" for any transportation needs.

Pricing is based on a fixed price per flight hour flown with a fuel cost surcharge above a set benchmark. Ancillary costs such as landing fees and de-icing are passed through to the end customer.

Strata leverages an asset-light air logistics business model. We primarily utilize aircraft that are owned and/or operated by third parties on Strata's behalf. In these arrangements, pilots, maintenance, hangar, insurance, and fuel are all costs borne by our network of operators, which provide aircraft flight time to Strata at fixed hourly rates. This enables our operator partners to focus on training pilots, maintaining aircraft and flying, while we maintain the relationship with our customer from booking through flight arrival.

When utilizing third-party aircraft and/or aircraft operators, we typically pre-negotiate fixed hourly rates and flight times, paying only for flights actually flown, creating a predictable and flexible cost structure. Strata provides guaranteed flight commitments to some of our third-party operators through capacity purchase agreements ("CPAs"), which enable Strata to ensure dedicated access to such aircraft with enhanced crew availability, lower costs and, in many cases, the ability to unlock more favorable rates when flying more than the minimum number of hours we guarantee to the operator. Additionally, a significant portion of trips are flown by safety-vetted operators to whom we make no commitments, providing us with additional flexible capacity for high demand periods.

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

**Present:** meta.json, form4_summary.md, 8-K_2026-08-04_2-02-results.md, 10-K_2026-03-03_item7_mdna.md, 10-K_2026-03-03_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
