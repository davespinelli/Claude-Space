# Triage pack — BORR · Borr Drilling Ltd

_Generated 2026-09-04 17:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** BORR · **Name:** Borr Drilling Ltd
- **CIK:** 0001715497
- **SIC:** 1381 — Drilling Oil & Gas Wells
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/BORR

**Fetcher warnings for this ticker:** 10-K 2026-03-26: heading split missed Item 1 - Business, Item 1A - Risk Factors; no 10-Q in recent filings; no proxy (DEF 14A) in recent filings

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Borr Drilling Ltd
- **CIK:** 1,715,497 · **SIC:** 1381 (Drilling Oil & Gas Wells) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 4.61 |
| mktcap | $1.4B |
| ev | $3.7B |
| ev_ebit | 11.4x |
| fcf | $251.9M |
| fcf_yield | 17.8% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 7.9% |
| net_debt | $2.3B |
| net_debt_ebit | 7.0x |
| cash | $223.6M |
| ltd | $2.5B |
| equity | $961.6M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $1.0B |
| revenue_prior | $1.0B |
| rev_growth | 1.0% |
| rev_growth_note | share count +25.4% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | n/a |
| ebit | $322.1M |
| net_income | $45.0M |
| cfo | $251.9M |
| capex | n/a |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 25.4% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 307,215,419 |
| shares_py | 244,926,821 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 40.4% |
| r6m | -20.5% |
| off_52w_high | -30.3% |
| adv20 | $26.9M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.86 |
| r_ev_ebit | 0.70 |
| r_roic | 0.64 |
| r_rev_growth | 0.38 |
| r_buyback | 0.06 |
| score | 0.58 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q2I |
| shares_period | CY2025Q4I |
| shares_py_period | CY2024Q4I |
| capex_missing | True |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 169 |

**Screen rationale:** top-quartile FCF yield 17.8%; share count +25.4% yoy — growth may be acquisition/issuance-driven, not organic; 12-1 momentum 40.4%


## 3. Share count trend

- Shares outstanding: **307,215,419** (CY2025Q4I) vs **244,926,821** prior year (CY2024Q4I)
- Change: **25.4%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`
- **Flag:** share count +25.4% yoy — growth may be acquisition/issuance-driven, not organic

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No 8-K filings fetched for this ticker._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 200,000 sh / $874,620 vs sells 83,438 sh / $396,514 -> net $478,106 (BUYING).
Distinct insiders buying (code P): 1. Largest buy: Troim Tor Olav bought 200,000 sh @ $4.37 ($874,620) on 2026-08-25.

Form 4 filings parsed: 12; transaction rows: 6 (open-market buys 1, sales 5).

| code | rows |
|---|---|
| P | 1 |
| S | 5 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release

_Not available: no 8-K with a readable release exhibit was fetched. Current-quarter results are unknown from this pack._

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-26_item7_mdna.md)

_Extraction: no Overview/Results heading found; took the start of Item 7._

ITEM 7. MAJOR SHAREHOLDERS AND RELATED PARTY TRANSACTIONS

A. MAJOR SHAREHOLDERS

The foll owing table sets forth beneficial ownership of our common shares, by each person known to us to own beneficially more than 5% of our total common shares as of March 17, 2026:

Common Shares
Owner | Number | Percentage (1)
Thiago Mordehachvili (2) | 46,145,132 | 15.0 | %
Azvalor Asset Management SGIIC SA (3) | 28,606,167 | 9.3 | %
Tor Olav Trøim (4) | 25,150,263 | 8.2 | %

(1) The calculations in the table above are based on 307,701,075 common shares outstanding as of March 17, 2026.

(2) Represents shares held by Granular Capital Ltd, which is a fund managed and founded by Thiago Mordehachvili. This does not include 2,000,000 Contract for Difference derivative shares with no maturity date held by Granular Capital Ltd.

(3) Based solely on information contained in the Schedule 13G filed by Azvalor Asset Management SGIIC SA on November 25, 2025.

(4) Includes 25,122,941 shares held by Drew Holding Ltd., which is wholly owned by Drew Trust, a non-discretionary trust in which Tor Olav Trøim is the beneficiary.

To our knowledge, as of March 17, 2026, a total of 307,701,075 shares are held by 2 holders of record in the U.S., including Cede & Co., as nominee for the Depository Trust Company, which is the holder of record of our shares that are traded on the NYSE.

We are not aware of any arrangement that may, at a subsequent date, result in a change of control of our company. See the section entitled "Item 10.B. Memorandum and Articles of Association—Our Memorandum of Association and Bye-Laws" for historical changes in our shareholding structure.

B. RELATED PARTY TRANSACTIONS

For a description of our related party transactions, see "Part III, Item 17. Financial Statements—Notes to the Audited Consolidated Financial Statements —Note 22 - Related Party Transactions".

Certain Directors and executive officers have participated in public equity offerings of the Company's common shares at terms identical to that of third-party participants. For information on shareholdings held by all Directors and executive officers of the Company see the section entitled "Item 6.E. Share Ownership".

For details of our shares issued as compensation to Directors and executive officers, see "Part III, Item 17. Financial Statements—Notes to the Audited Consolidated Financial Statements —Note 19 - Share-Based Compensation".

C. INTERESTS OF EXPERTS AND COUNSEL

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
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-26_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | **MISSING** |

**Present:** meta.json, form4_summary.md, 10-K_2026-03-26_item7_mdna.md

**Missing:** 8-K filings, 8-K earnings press release exhibit, 10-K Item 1 - Business (business description), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
