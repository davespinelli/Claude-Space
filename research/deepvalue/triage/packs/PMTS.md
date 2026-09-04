# Triage pack — PMTS · CPI Card Group Inc.

_Generated 2026-09-04 13:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** PMTS · **Name:** CPI Card Group Inc.
- **CIK:** 1,641,614
- **SIC:** 2750 — Commercial Printing
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** Nasdaq
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** CPI Card Group Inc.
- **CIK:** 1,641,614 · **SIC:** 2750 (Commercial Printing) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 28.65 |
| mktcap | $330.4M |
| ev | $571.1M |
| ev_ebit | 10.4x |
| fcf | $41.3M |
| fcf_yield | 12.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 18.9% |
| net_debt | $240.8M |
| net_debt_ebit | 4.4x |
| cash | $21.4M |
| ltd | $262.1M |
| equity | -$11.5M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $543.5M |
| revenue_prior | $480.6M |
| rev_growth | 13.1% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $54.8M |
| net_income | $14.9M |
| cfo | $59.5M |
| capex | $18.2M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 1.7% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 11,530,669 |
| shares_py | 11,337,367 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 56.8% |
| r6m | 62.8% |
| off_52w_high | -6.1% |
| adv20 | $3.5M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.78 |
| r_ev_ebit | 0.74 |
| r_roic | 0.87 |
| r_rev_growth | 0.72 |
| r_buyback | 0.35 |
| score | 0.74 |

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
| rank | 36 |

**Screen rationale:** top-quartile FCF yield 12.5%; high ROIC 18.9%; 12-1 momentum 56.8%


## 3. Share count trend

- Shares outstanding: **11,530,669** (CY2026Q2I) vs **11,337,367** prior year (CY2025Q2I)
- Change: **1.7%** — dilution / growing count
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
