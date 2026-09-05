# Triage pack — SSYS · STRATASYS LTD.

_Generated 2026-09-05 03:09 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** SSYS · **Name:** STRATASYS LTD.
- **CIK:** 0001517396
- **SIC:** 3577 — Computer Peripheral Equipment, NEC
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/SSYS

**Fetcher warnings for this ticker:** 10-K 2026-03-05: heading split missed Item 1 - Business, Item 1A - Risk Factors; no 10-Q in recent filings; no proxy (DEF 14A) in recent filings; no Form 4 filings in the last 12 months

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** STRATASYS LTD.
- **CIK:** 1,517,396 · **SIC:** 3577 (Computer Peripheral Equipment, NEC) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 7.77 |
| mktcap | $669.1M |
| ev | $574.5M |
| ev_ebit | n/a |
| fcf | -$7.0M |
| fcf_yield | -1.0% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -7.7% |
| net_debt | -$94.5M |
| net_debt_ebit | n/a |
| cash | $94.5M |
| ltd | $0.00 |
| equity | $842.9M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $551.1M |
| revenue_prior | $572.5M |
| rev_growth | -3.7% |
| rev_growth_note | share count +20.1% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | n/a |
| ebit | -$72.5M |
| net_income | n/a |
| cfo | $15.1M |
| capex | $22.1M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 20.1% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 86,109,936 |
| shares_py | 71,716,159 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -11.6% |
| r6m | -14.6% |
| off_52w_high | -37.5% |
| adv20 | $7.0M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.18 |
| r_ev_ebit | 0.00 |
| r_roic | 0.15 |
| r_rev_growth | 0.23 |
| r_buyback | 0.07 |
| score | 0.13 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2025Q4I |
| shares_period | CY2025Q4I |
| shares_py_period | CY2024Q4I |
| capex_missing | False |
| ltd_missing | True |

**Other screen columns**

| metric | value |
|---|---|
| rank | 479 |

**Screen rationale:** share count +20.1% yoy — growth may be acquisition/issuance-driven, not organic; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **86,109,936** (CY2025Q4I) vs **71,716,159** prior year (CY2024Q4I)
- Change: **20.1%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`
- **Flag:** share count +20.1% yoy — growth may be acquisition/issuance-driven, not organic

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

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-05_item7_mdna.md)

_Extraction: no Overview/Results heading found; took the start of Item 7._

ITEM 7. MAJOR SHAREHOLDERS AND RELATED PARTY TRANSACTIONS.

A. Major Shareholders

Ownership by Major Shareholders

The following table presents the beneficial ownership of our ordinary shares by each person who is known by us to be the beneficial owner of 5% or more of our outstanding ordinary shares (to whom we refer as our major shareholders), based on the most recent beneficial ownership reports filed with the SEC by such persons on or before February 17, 2026. The data presented is based on information provided to us, or disclosed in public filings with the SEC, by the major shareholders.

Beneficial ownership of shares is determined under rules of the SEC and generally includes any shares for which a person exercises sole or shared voting or investment power, or for which a person has or shares the right to receive the economic benefit of ownership of the shares. To the extent applicable, the table below also includes as beneficially owned by any major shareholder shares underlying options, warrants or other convertible securities that are exercisable or convertible within 60 days after February 17, 2026. Shares issuable upon the exercise or conversion of such convertible securities are deemed to be outstanding for the purpose of computing the ownership percentage of the person, entity or group holding such securities, but are not deemed to be outstanding for the purpose of computing the ownership percentage of any other person, entity or group. The ownership percentages reflected below are based on 86,172,539 ordinary shares outstanding (which excludes 266,018 Treasury shares) as of February 17, 2026.

Except where otherwise indicated, and except pursuant to community property laws, we believe, based on information furnished by such owners, that the beneficial owners of the shares listed below have sole investment and voting power with respect to, and the sole right to receive the economic benefit of ownership of, such shares. The shareholders listed below do not have any different voting rights from any of our other shareholders. We know of no arrangements that would, at a subsequent date, result in a change of control of our company.

Beneficial Owner | Ordinary Shares | Percentage Ownership
FF6-SSYS, Limited Partnership | 12,825,885 1 | 14.9%
Nano Dimension Ltd. | 9,695,115 2 | 11.3%
Rubric Capital Management LP | 7,340,026 3 | 8.5%
Neuberger Berman Group LLC | 4,292,998 4 | 5.0%

Changes in Percentage Ownership by Major Shareholders

1 Represents shares beneficially owned as of April 8, 2025, as indicated in a statement of beneficial ownership on Schedule 13D filed by FF6-SSYS, Limited Partnership, or FF6-SSYS, and affiliated entities with the SEC on April 10, 2025. The total beneficial ownership of 12,825,885 ordinary shares is comprised of: (i) 11,650,485 shares held by FF6-SSYS, over which it has sole voting and dispositive power, and (ii) 1,175,400 shares held by Fortissimo Capital Fund V, L.P., or FF V. FF6-SSYS is an Israeli limited partnership, for which Fortissimo Capital 6 Management (GP) Ltd., or FF 6 serves as its sole general partner. FF V is a Cayman Islands limited partnership, for which Fortissimo Capital Fund V GP, L.P., or FF V GP, serves as its sole general partner. Fortissimo Capital 5 Management (GP) Ltd., an Israeli company, or FF 5, serves as sole general partner of FF V GP. Yuval Cohen serves as the sole director and shareholder of each of FF 6 and FF 5 and may therefore be deemed to possess ultimate shared beneficial ownership over all of the subject shares.

2 Represents shares beneficially owned as of December 23, 2023, as indicated in Amendment No. 12 to the statement of beneficial ownership on Schedule 13D filed by Nano Dimension Ltd. with the SEC on December 26, 2023. As indicated in that statement, Nano Dimension Ltd. possesses sole voting and investment power with respect to 9,695,015 of those ordinary shares beneficially owned by it.

3 Represents shares beneficially owned as of December 31, 2025, as indicated in a report of institutional investment manager on Form 13F filed by Rubric Capital Management LP, or Rubric Capital, with the SEC on February 13, 2026. As indicated in that report and in reports of beneficial ownership on Schedule 13G that it has filed, Rubric Capital possesses shared investment discretion and shared voting authority with David Rosen with respect to all such ordinary shares. Rubric Capital serves as investment adviser to certain investment funds and/or accounts that hold the subject ordinary shares, while David Rosen serves as Managing Member of Rubric Capital Management GP LLC, the general partner of Rubric Capital.

4 Represents shares beneficially owned as of December 31, 2025, as indicated in a report of institutional investment manager on Form 13F filed by Neuberger Berman Group LLC, or Neuberger Berman, with the SEC on February 13, 2026. As indicated in that report, Neuberger Berman possesses: sole investment discretion and sole voting authority with respect to 137,984 ordinary shares, and shared investment discretion with respect to 4,155,014 ordinary shares, of which 3,278,152 are subject to its sole voting authority and 876,862 are not subject to its voting authority.

On April 8, 2025, FF6-SSYS, Limited Partnership, an affiliate of Fortissimo Capital, an Israeli private equity fund (together with its affiliates, collectively referred to as Fortissimo) became a major shareholder of ours, acquiring 11,650,485 newly-issued ordinary shares via a PIPE investment in our company (besides additional ordinary shares acquired by it). As of the end of 2025, the 12,825,885 ordinary shares held by Fortissimo constituted approximately 14.9% of our outstanding ordinary shares.

Nano Dimension Ltd., or Nano, filed its initial statement of beneficial ownership on Schedule 13G on July 18, 2022, disclosing an ownership of 8,049,186 ordinary shares, making it one of our major shareholders. Its holdings of our ordinary shares increased during 2023. As of its last amended filing on Schedule 13D, filed on December 26, 2023, Nano owned 9,695,115 ordinary shares, which then constituted approximately 13.9% of our ordinary shares, making it the largest shareholder of the Company at the time. Nano has not reported any changes in its beneficial ownership since that time, but its percentage ownership has dropped to 11. 3% as of the end of 2025.

As of the end of 2022, a new significant shareholder, Phoenix Financial Ltd. (formerly Phoenix Holdings Ltd.), reported that together with its subsidiaries, it had acquired a 5.9% ownership stake in the Company. During 2023, 2024 and 2025, its percentage ownership of our ordinary shares decreased to 5.2%, 5.0% and below 5%, respectively.

During 2023, and 2024, several new major shareholders acquired ownership of over 5% of our ordinary shares, including Rubric Capital Management, Neuberger Berman Group LLC, The Goldman Sachs Group, Inc., and Farhad Fred Ebrahimi and Mary Wilkie Ebrahimi.

During 2024, the percentage ownership of our ordinary shares by Rubric Capital Management increased from 6.1% to 8.6%, and during 2025 that percentage dropped slightly to 8.5%.

During 2024, the percentage ownership of our ordinary shares by Neuberger Berman Group LLC increased from 5.6% to 6.2%, and during 2025 that percentage dropped to 5.0%.

During 2024, the percentage ownership of our ordinary shares by The Goldman Sachs Group, Inc. decreased to below 5.0% and it thereby ceased to be a major shareholder of ours.

In 2024, Farhad Fred Ebrahimi and Mary Wilkie Ebrahimi sold ordinary shares in the open market and reduced their holdings to 4.98%, thereby ceasing to be a major shareholder of ours.

Record Holders

Based upon a review of the information provided to us by our transfer agent, as of February 17, 2026, there were 75 holders of record of our shares, of which 50 record holders holding approximately 86.8% of our outstanding ordinary shares, had registered addresses in the United States. These numbers are not representative of the number of beneficial holders of our shares nor is it representative of where such beneficial holders reside, since many of these shares were held of record by brokers or other nominees. As of the said date, CEDE & Co, the nominee company of the Depository Trust Company (with a registered address in the United States), held of record approximately 86.2% of our outstanding ordinary shares on behalf of hundreds of firms of brokers and banks in the United States, who in turn held such shares on behalf of several thousand clients and customers.

Potential Change in Control Transactions

As of the date of this annual report, we are not aware of any arrangements the operation of which may at a subsequent date result in a change in control of our company.

B. Related Party Transactions.

Except as described below or elsewhere in this annual report, since January 1, 2025, we have had no transaction or loan, nor do we have any presently proposed transaction or loan, involving any related party described in Item 7.B of Form 20-F promulgated by the SEC.

Investment and Distribution Agreements with Tritone Technologies Ltd.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business

_Not available: the fetcher did not split out this section for this filing. Describe the business from the MD&A overview above instead, and say so in the note._

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | **MISSING** |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-05_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | **MISSING** |

**Present:** meta.json, form4_summary.md, 10-K_2026-03-05_item7_mdna.md

**Missing:** 8-K filings, 8-K earnings press release exhibit, 10-K Item 1 - Business (business description), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
