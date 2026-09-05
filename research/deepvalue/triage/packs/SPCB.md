# Triage pack — SPCB · SuperCom Ltd

_Generated 2026-09-05 03:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** SPCB · **Name:** SuperCom Ltd
- **CIK:** 0001291855
- **SIC:** 3674 — Semiconductors & Related Devices
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/SPCB

**Fetcher warnings for this ticker:** 10-K 2026-04-28: heading split missed Item 1 - Business, Item 1A - Risk Factors; no 10-Q in recent filings; no proxy (DEF 14A) in recent filings; no Form 4 filings in the last 12 months

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** SuperCom Ltd
- **CIK:** 1,291,855 · **SIC:** 3674 (Semiconductors & Related Devices) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

> **EARNINGS QUALITY FLAG — one-off items likely.**
> net income more than 3x operating income.
> Reported net income is not supported by the operating engine that is supposed to produce it (typical causes: gains on sale, legal settlements, deferred-tax valuation-allowance releases, bargain-purchase gains). Reconcile net income to operating income in the earnings release (section 7) before treating any earnings-based metric here as repeatable.

**Valuation**

| metric | value |
|---|---|
| price | 10.08 |
| mktcap | $54.1M |
| ev | $63.0M |
| ev_ebit | n/a |
| fcf | -$6.4M |
| fcf_yield | -11.8% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -0.5% |
| net_debt | $8.9M |
| net_debt_ebit | n/a |
| cash | $9.8M |
| ltd | $18.7M |
| equity | $43.5M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $27.9M |
| revenue_prior | $27.6M |
| rev_growth | 0.9% |
| rev_growth_note | share count +147.1% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | net income more than 3x operating income |
| ebit | -$322k |
| net_income | $3.7M |
| cfo | -$5.5M |
| capex | $880k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 147.1% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 5,369,367 |
| shares_py | 2,172,855 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 15.8% |
| r6m | 22.2% |
| off_52w_high | -23.5% |
| adv20 | $1.3M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.07 |
| r_ev_ebit | 0.00 |
| r_roic | 0.29 |
| r_rev_growth | 0.37 |
| r_buyback | 0.01 |
| score | 0.20 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2025Q4I |
| shares_period | CY2025Q4I |
| shares_py_period | CY2024Q4I |
| capex_missing | False |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 465 |

**Screen rationale:** share count +147.1% yoy — growth may be acquisition/issuance-driven, not organic; 12-1 momentum 15.8%; EARNINGS QUALITY: net income more than 3x operating income — one-off items likely


## 3. Share count trend

- Shares outstanding: **5,369,367** (CY2025Q4I) vs **2,172,855** prior year (CY2024Q4I)
- Change: **147.1%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`
- **Flag:** share count +147.1% yoy — growth may be acquisition/issuance-driven, not organic

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No 8-K filings fetched for this ticker._

## 6. Insider activity (Form 4, trailing 12 months)

No Form 4 activity in 12 months (no observation; not a signal).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 0; transaction rows: 0 (open-market buys 0, sales 0).

| code | rows |
|---|---|

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release

_Not available: no 8-K with a readable release exhibit was fetched. Current-quarter results are unknown from this pack._

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-04-28_item7_mdna.md)

_Extraction: no Overview/Results heading found; took the start of Item 7._

ITEM 7. | MAJOR SHAREHOLDERS AND RELATED PARTY TRANSACTIONS

A. | Major Shareholders

The following table lists the beneficial ownership of our securities as of April 22, 2026 by each
person known by us to be the beneficial owner of 5% or more of the outstanding shares of any class of our securities of which 5,369,367
of our ordinary shares were issued and outstanding:

Mas Alpha Securities Fund LP

Mas Alpha holds 302,196 shares of our ordinary shares, which reflects approximately 5.6% of our issued
and outstanding ordinary shares, as reported in Mas Alpha's Schedule 13G/A filed with the SEC on August 5, 2025.

Significant Changes in the Ownership of Major Shareholders

None

Voting Rights of Major Shareholders

Our major shareholders do not have different voting rights from the other holders of our ordinary shares.

Record Holders

Based on a review of the information provided to us by our U.S. transfer agent, as of December 31, 2025,
there were approximately 24 record holders, of which 7 record holders holding approximately 99.91% of our ordinary shares had registered
addresses in the United States. These numbers are not representative of the number of beneficial holders of our shares nor are they representative
of where such beneficial holders reside, since many of these ordinary shares were held of record by brokers or other nominees (including
one U.S. nominee company, CEDE & Co., which held approximately 99.50% of our outstanding ordinary shares as of such date).

B. | Related Party Transactions

It is our policy to enter into transactions with related parties on terms that, on the whole, are no less
favorable than those that would be available from unaffiliated parties. Based on our experience in the business segments in which we operate
and the terms of our transactions with unaffiliated third parties, we believe that all of the transactions described below met our policy
standards at the time they occurred.

Mr. Arie Trabelsi has served as the Chief Executive Officer of the Company since June 1, 2012 until February
21, 2022. On May 9, 2013, the general meeting of shareholders of the Company approved the payment of management fees to Mr. Trabelsi of
$10.6 per month plus social benefits and an annual bonus of the greater of 2% of the Company's annual net profit or 0.5% of annual
revenues, but in no event greater than Mr. Trabelsi annual salary. As of December 31, 2025 and 2024, we had accrued $29,000, and $25,000,
respectively as expenses arising from services provided by Mr. Trabelsi.

On April 29, 2012, our Board of Directors approved the recording of a floating charge on our assets in
favor of Mr. Arie Trabelsi and his spouse, unlimited in amount, in order to secure loans that are given by them from time to time to us.
The short terms loans provided by Mr. Arie Trabelsi and his spouse during the years from 2011 until 2025 ranged from $0 up to $2,662,470
and bore no interest. As of December 31,2025, total loans were $0.

The relationships and related party transactions described herein are in addition to any employment arrangements
with our executive officers and directors, which are described in this Annual Report above under "ITEM 6. Directors, Senior Management
and Employees".

Indemnification Agreements

Our Articles of Association provide that we may indemnify our officers and directors for certain cases
of liability and expenses incurred by him or her as a result of an act done by him or her by virtue of being such an office holder.
In addition, we have granted indemnification letters to our office holders. For more information, please see section above captioned "
ITEM 6.C. Directors, Senior Management and Employees ⸺. Board Practices ⸺ Exculpation, Insurance and Indemnification of
Directors and Officers".

C. | Interests of Experts and Counsel

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
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-04-28_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | **MISSING** |

**Present:** meta.json, form4_summary.md, 10-K_2026-04-28_item7_mdna.md

**Missing:** 8-K filings, 8-K earnings press release exhibit, 10-K Item 1 - Business (business description), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
