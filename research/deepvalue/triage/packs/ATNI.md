# Triage pack — ATNI · ATN International, Inc.

_Generated 2026-09-04 19:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** ATNI · **Name:** ATN International, Inc.
- **CIK:** 879,585
- **SIC:** 4813 — Telephone Communications (No Radiotelephone)
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** Nasdaq
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** ATN International, Inc.
- **CIK:** 879,585 · **SIC:** 4813 (Telephone Communications (No Radiotelephone)) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 31.07 |
| mktcap | $478.6M |
| ev | $650.6M |
| ev_ebit | 22.9x |
| fcf | $43.9M |
| fcf_yield | 9.2% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 2.9% |
| net_debt | $172.0M |
| net_debt_ebit | 6.0x |
| cash | $317.6M |
| ltd | $489.6M |
| equity | $598.8M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $728.0M |
| revenue_prior | $729.1M |
| rev_growth | -0.2% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $28.4M |
| net_income | -$23.5M |
| cfo | $133.9M |
| capex | $90.0M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 1.0% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 15,403,357 |
| shares_py | 15,257,391 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 59.6% |
| r6m | 26.6% |
| off_52w_high | -3.2% |
| adv20 | $2.8M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.70 |
| r_ev_ebit | 0.39 |
| r_roic | 0.42 |
| r_rev_growth | 0.34 |
| r_buyback | 0.46 |
| score | 0.51 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q2I |
| shares_period | CY2026Q2I |
| shares_py_period | CY2025Q2I |
| capex_missing | False |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 231 |

**Screen rationale:** 12-1 momentum 59.6%


## 3. Share count trend

- Shares outstanding: **15,403,357** (CY2026Q2I) vs **15,257,391** prior year (CY2025Q2I)
- Change: **1.0%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No 8-K filings fetched for this ticker._

## 6. Insider activity (Form 4, trailing 12 months)

_Not available: form4_summary.md was not fetched. Treat insider activity as unknown, not as absent._

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

**Present:** none

**Missing:** meta.json, 8-K filings, form4_summary.md, 8-K earnings press release exhibit, 10-K Item 7 MD&A (management commentary), 10-K Item 1 - Business (business description), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
