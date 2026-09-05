# Triage pack — RDGT · Ridgetech Inc.

_Generated 2026-09-05 02:05 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** RDGT · **Name:** Ridgetech Inc.
- **CIK:** 0001856084
- **SIC:** 5912 — Retail-Drug Stores and Proprietary Stores
- **Fiscal year end (MM-DD):** 03-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/RDGT

**Fetcher warnings for this ticker:** 10-K 2026-07-31: heading split missed Item 1 - Business, Item 1A - Risk Factors; no 10-Q in recent filings; no proxy (DEF 14A) in recent filings

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Ridgetech Inc.
- **CIK:** 1,856,084 · **SIC:** 5912 (Retail-Drug Stores and Proprietary Stores) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 0.90 |
| mktcap | $119.8M |
| ev | $101.9M |
| ev_ebit | n/a |
| fcf | -$1.4M |
| fcf_yield | -1.2% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | -$17.9M |
| net_debt_ebit | n/a |
| cash | $17.9M |
| ltd | $0.00 |
| equity | n/a |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $132.2M |
| revenue_prior | $120.0M |
| rev_growth | 10.2% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$1.9M |
| net_income | -$1.3M |
| cfo | -$1.4M |
| capex | $449.00 |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | n/a |
| share_chg_src | n/a |
| shares | 133,090,838 |
| shares_py | 5,855,009 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -99.6% |
| r6m | -99.7% |
| off_52w_high | -99.9% |
| adv20 | $3.7M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.17 |
| r_ev_ebit | 0.00 |
| r_roic | 0.50 |
| r_rev_growth | 0.66 |
| r_buyback | 0.50 |
| score | 0.27 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | n/a |
| shares_period | CY2026Q1I |
| shares_py_period | CY2025Q1I |
| capex_missing | False |
| ltd_missing | True |

**Other screen columns**

| metric | value |
|---|---|
| rank | 434 |

**Screen rationale:** debt data missing (net cash unverified); WARNING 6m return below -40%


## 3. Share count trend

_No usable share count for the prior year (dei cover-page count absent and no fallback tag available); share trend not computed._

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No 8-K filings fetched for this ticker._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 99,845 sh / $161,185 vs sells 72,615 sh / $115,655 -> net $45,530 (BUYING).
Distinct insiders buying (code P): 1. Largest buy: HRT FINANCIAL LP bought 30,939 sh @ $1.52 ($47,027) on 2026-06-30.

Form 4 filings parsed: 7; transaction rows: 9 (open-market buys 5, sales 3).

| code | rows |
|---|---|
| P | 6 |
| S | 3 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release

_Not available: no 8-K with a readable release exhibit was fetched. Current-quarter results are unknown from this pack._

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-07-31_item7_mdna.md)

_Extraction: no Overview/Results heading found; took the start of Item 7._

ITEM 7. MAJOR SHAREHOLDERS AND RELATED PARTY TRANSACTIONS.

A. MAJOR SHAREHOLDERS

Please refer to Item 6.E "Directors,
Senior Management and Employees - Share Ownership." As of the date of this annual report, we are not aware of any person or entity
that beneficially owns 5% or more of our outstanding ordinary shares.

To our knowledge, (A) we are
not directly or indirectly owned or controlled by (i) another corporation or (ii) any foreign government and (B) there are no arrangements
(including any announced or expected takeover bid), the operation of which may at a subsequent date result in a change in our control.

All of our shareholders, including
our directors and executive officers, have the same voting rights with respect to their ordinary shares. Our Chairman of the Board, Lingtao
Kong, holds 100,000 Series A Preferred Shares, which carry one hundred votes per share and are convertible into ordinary shares in accordance
with the Statement of Rights applicable to the Series A Preferred Shares, as described under "Item 10.B. Memorandum and Articles
of Association — Preferred Shares" below.

B. RELATED PARTY TRANSACTIONS.

Subscription Agreement for Series A Preferred
Shares

On July 16, 2026, the Company entered into a Subscription
Agreement (the "Subscription Agreement") with Mr. Lingtao Kong, Chairman of the Board of Directors, pursuant to which the
Company issued 100,000 Series A Preferred Shares to Mr. Kong for an aggregate subscription price of US$100. The Audit Committee reviewed
and approved the Subscription Agreement and the related-party aspects of the transactions contemplated thereby, including potential conflicts
of interest. The issuance was approved for the purposes of promoting continuity of leadership, strategic direction and corporate stability,
retaining and incentivizing Mr. Kong's continued service to the Company, enhancing the Company's ability to respond to hostile takeover
attempts or other unsolicited change-of-control transactions, and achieving those objectives in a manner that minimizes economic dilution
to existing shareholders. Each Series A Preferred Share carries 100 votes per share and votes together with holders of ordinary shares
as a single class on all matters submitted to a vote of shareholders, unless otherwise required by applicable law or the Company's
memorandum and articles of association. The Series A Preferred Shares are subject to conversion, transfer, and other restrictions as described
under "Item 10.B. Memorandum and Articles of Association — Preferred Shares" below.

Equity Exchange Agreements

On January 31, 2025, we entered
into (i) that certain Equity Exchange Agreement with Mr. Lingtao Kong and Ridgeline, pursuant to which the Company acquired from Mr. Kong
all of the issued and outstanding ordinary shares of Ridgeline, by issuing 14,834 our ordinary shares to Mr. Kong, and (ii) that certain
Equity Exchange Agreement with Renovation, Mr. Lei Liu, Ms. Li Qi, and Oakview, pursuant to which Renovation transferred all equity in
Jiuxin Investment to Oakview, in exchange for irrevocable surrender for no consideration by Mr. Liu, Ms. Qi, Oakview and their affiliates
in total 16,990 our ordinary shares back to us. The transactions were closed on February 28, 2025. Following the closing of these transactions,
we changed our name from "China Jo-Jo Drugstores, Inc." to "Ridgetech, Inc.", effective as of February 28, 2025.
We also changed our trading symbol on The Nasdaq Stock Market LLC from "CJJD" to "RDGT", effective as of March
4, 2025. Effective as of the closing, Mr. Liu and Ms. Qi resigned from our board of directors and any other officer positions with us
(including Mr. Liu's role as our Chief Executive Officer), and Mr. Ming Zhao, our Chief Financial Officer, was appointed as our
interim Chief Executive Officer to hold such office until a permanent Chief Executive Officer is duly appointed.

Share Surrender

In October 2024, Mr. Lei Liu,
our former Chairman of the Board and Chief Executive Officer, agreed to surrender for no consideration in total 52,500 fully-paid ordinary
shares, par value $0.24 per share, of the Company, and Mr. Ming Zhao, our Chief Financial Officer, agreed to surrender for no consideration
in total 2,500 ordinary shares, par value $0.24 per share, of the Company, such ordinary shares in each case to be immediately cancelled
by the Company. In November 2024, Mr. Liu agreed to surrender for no consideration in total additional 420,715 fully-paid ordinary shares,
par value $0.24 per share, of the Company, to be immediately cancelled by the Company. The Company shall make available for reissuance
to participants under the Company's 2010 Equity Incentive Plan an equivalent number of ordinary shares as surrendered and cancelled
in connection with the share surrender. No grants, cash payments or other consideration has been or will be made to replace such ordinary
shares or otherwise in connection with the share surrender.

Other Related Party Transactions

In connection with the divestiture
of Jiuxin Investment and its owned and controlled entities during the fiscal year ended March 31, 2025, we have revised the presentation
of our historical consolidated financial statements to exclude the operations of the divested entities for all periods presented. This
re-presentation is intended to provide a consistent basis of comparison that reflects our continuing operations. As a result, certain
financial information for prior periods included in this annual report including the amounts disclosed for the fiscal year ended March
31, 2024, differs from the corresponding financial information presented in our annual report on Form 20-F for the fiscal year ended March
31, 2024.

Due from related parties: | March 31, 2026 | March 31, 2025 | March 31, 2024
Due from a director of subsidiaries (1) | 329,258 | - | 7,202
Hangzhou Kahamadi Biotechnology Co., Ltd | - | - | 12,535
Total | 329,258 | - | 19,737

Due to related parties: | March 31, 2026 | March 31, 2025 | March 31, 2024
Due to a director of subsidiaries (2) | - | 2,130 | 2,140
Total | - | 2,130 | 2,140

(1) | Advances to directors of our subsidiaries.

(2) | Borrowed from a director of subsidiaries.

C. INTERESTS OF EXPERTS
AND COUNSEL.

Not applicable.

## 9. 10-K Item 1 - Business

_Not available: the fetcher did not split out this section for this filing. Describe the business from the MD&A overview above instead, and say so in the note._

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | **MISSING** |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-07-31_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | **MISSING** |

**Present:** meta.json, form4_summary.md, 10-K_2026-07-31_item7_mdna.md

**Missing:** 8-K filings, 8-K earnings press release exhibit, 10-K Item 1 - Business (business description), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
