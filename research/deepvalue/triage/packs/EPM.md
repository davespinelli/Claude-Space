# Triage pack — EPM · EVOLUTION PETROLEUM CORP

_Generated 2026-09-04 22:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** EPM · **Name:** EVOLUTION PETROLEUM CORP
- **CIK:** 1,006,655
- **SIC:** 1311 — Crude Petroleum & Natural Gas
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** NYSE
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** EVOLUTION PETROLEUM CORP
- **CIK:** 1,006,655 · **SIC:** 1311 (Crude Petroleum & Natural Gas) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermLineOfCredit

**Valuation**

| metric | value |
|---|---|
| price | 3.70 |
| mktcap | $132.7M |
| ev | $186.6M |
| ev_ebit | 44.7x |
| fcf | $33.1M |
| fcf_yield | 24.9% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 2.9% |
| net_debt | $53.9M |
| net_debt_ebit | 12.9x |
| cash | $2.6M |
| ltd | $56.5M |
| equity | $58.4M |
| ltd_tag | LongTermLineOfCredit |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $85.8M |
| revenue_prior | $85.9M |
| rev_growth | -0.0% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $4.2M |
| net_income | $1.5M |
| cfo | $33.1M |
| capex | n/a |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 4.6% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 35,872,725 |
| shares_py | 34,307,640 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -21.7% |
| r6m | -13.3% |
| off_52w_high | -25.1% |
| adv20 | $2.4M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.92 |
| r_ev_ebit | 0.15 |
| r_roic | 0.42 |
| r_rev_growth | 0.34 |
| r_buyback | 0.20 |
| score | 0.41 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q1I |
| shares_period | CY2026Q1I |
| shares_py_period | CY2025Q1I |
| capex_missing | True |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 317 |

**Screen rationale:** top-quartile FCF yield 24.9%


## 3. Share count trend

- Shares outstanding: **35,872,725** (CY2026Q1I) vs **34,307,640** prior year (CY2025Q1I)
- Change: **4.6%** — dilution / growing count
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
