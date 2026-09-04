# Triage pack — LFS · LEIFRAS Co., Ltd.

_Generated 2026-09-04 20:12 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** LFS · **Name:** LEIFRAS Co., Ltd.
- **CIK:** 0002030277
- **SIC:** 8200 — Services-Educational Services
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/LFS

**Fetcher warnings for this ticker:** 10-K 2026-04-08: heading split missed Item 1 - Business, Item 1A - Risk Factors, Item 7 - MD&A; no 10-Q in recent filings; no proxy (DEF 14A) in recent filings; no Form 4 filings in the last 12 months

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** LEIFRAS Co., Ltd.
- **CIK:** 2,030,277 · **SIC:** 8200 (Services-Educational Services) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 2.23 |
| mktcap | $58.3M |
| ev | $42.4M |
| ev_ebit | 10.6x |
| fcf | $2.7M |
| fcf_yield | 4.7% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | -$15.9M |
| net_debt_ebit | -4.0x |
| cash | $16.1M |
| ltd | $156k |
| equity | $11.8M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $74.8M |
| revenue_prior | n/a |
| rev_growth | n/a |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $4.0M |
| net_income | $2.8M |
| cfo | $3.0M |
| capex | $272k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 5.0% |
| share_chg_src | us-gaap:CommonStockSharesOutstanding |
| shares | 26,160,619 |
| shares_py | 24,910,619 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | n/a |
| r6m | -5.1% |
| off_52w_high | -80.4% |
| adv20 | $4.1M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.47 |
| r_ev_ebit | 0.73 |
| r_roic | 0.50 |
| r_rev_growth | 0.50 |
| r_buyback | 0.19 |
| score | 0.48 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2025Q4I |
| shares_period | CY2025Q4I |
| shares_py_period | CY2024Q4I (CommonStockSharesOutstanding) |
| capex_missing | False |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 267 |

**Screen rationale:** net cash


## 3. Share count trend

- Shares outstanding: **26,160,619** (CY2025Q4I) vs **24,910,619** prior year (CY2024Q4I (CommonStockSharesOutstanding))
- Change: **5.0%** — dilution / growing count
- Source concept: `us-gaap:CommonStockSharesOutstanding`

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

## 8. 10-K Item 7 MD&A

_Not available: no 10-K Item 7 MD&A and no 10-Q MD&A was fetched. No management commentary in this pack._

## 9. 10-K Item 1 - Business

_Not available: the fetcher did not split out this section for this filing. Describe the business from the MD&A overview above instead, and say so in the note._

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | **MISSING** |
| MD&A / management commentary | 10-K Item 7 MD&A | **MISSING** |
| Risk factors | 10-K Item 1A - Risk Factors | **MISSING** |

**Present:** meta.json, form4_summary.md

**Missing:** 8-K filings, 8-K earnings press release exhibit, 10-K Item 7 MD&A (management commentary), 10-K Item 1 - Business (business description), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
