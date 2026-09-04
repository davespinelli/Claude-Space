# Triage pack — GENI · Genius Sports Ltd

_Generated 2026-09-04 16:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** GENI · **Name:** Genius Sports Ltd
- **CIK:** 0001834489
- **SIC:** 7990 — Services-Miscellaneous Amusement & Recreation
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/GENI

**Fetcher warnings for this ticker:** 10-K 2026-03-17: heading split missed Item 1 - Business, Item 1A - Risk Factors, Item 7 - MD&A; no 10-Q in recent filings; no proxy (DEF 14A) in recent filings

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Genius Sports Ltd
- **CIK:** 1,834,489 · **SIC:** 7990 (Services-Miscellaneous Amusement & Recreation) · **Exchange:** NYSE

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 7.63 |
| mktcap | $76.3M |
| ev | -$204.3M |
| ev_ebit | n/a |
| fcf | $64.5M |
| fcf_yield | 84.6% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -26.9% |
| net_debt | -$280.6M |
| net_debt_ebit | n/a |
| cash | $280.6M |
| ltd | $0.00 |
| equity | $724.5M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $669.5M |
| revenue_prior | $510.9M |
| rev_growth | 31.0% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$151.3M |
| net_income | -$111.6M |
| cfo | $86.4M |
| capex | $21.9M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -45.9% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 10,000,000 |
| shares_py | 18,500,000 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -36.2% |
| r6m | 30.2% |
| off_52w_high | -43.7% |
| adv20 | $38.0M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 1.00 |
| r_ev_ebit | 0.00 |
| r_roic | 0.04 |
| r_rev_growth | 0.90 |
| r_buyback | 0.98 |
| score | 0.58 |

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
| rank | 163 |

**Screen rationale:** top-quartile FCF yield 84.6%; revenue +31.0%; buying back stock -45.9%; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **10,000,000** (CY2025Q4I) vs **18,500,000** prior year (CY2024Q4I)
- Change: **-45.9%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No 8-K filings fetched for this ticker._

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 3; transaction rows: 9 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| F | 3 |
| M | 6 |

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
