# Triage pack — IRWD · IRONWOOD PHARMACEUTICALS INC

_Generated 2026-09-04 15:08 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** IRWD · **Name:** IRONWOOD PHARMACEUTICALS INC
- **CIK:** 1,446,847
- **SIC:** 2834 — Pharmaceutical Preparations
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** Nasdaq
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** IRONWOOD PHARMACEUTICALS INC
- **CIK:** 1,446,847 · **SIC:** 2834 (Pharmaceutical Preparations) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermLineOfCredit

**Valuation**

| metric | value |
|---|---|
| price | 4.29 |
| mktcap | $708.9M |
| ev | $1.0B |
| ev_ebit | 10.3x |
| fcf | $127.0M |
| fcf_yield | 17.9% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 54.0% |
| net_debt | $305.9M |
| net_debt_ebit | 3.1x |
| cash | $79.1M |
| ltd | $385.0M |
| equity | -$161.8M |
| ltd_tag | LongTermLineOfCredit |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $296.2M |
| revenue_prior | $351.4M |
| rev_growth | -15.7% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $98.5M |
| net_income | $24.0M |
| cfo | $127.0M |
| capex | $34k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 1.7% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 165,239,947 |
| shares_py | 162,434,130 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 234.7% |
| r6m | 18.5% |
| off_52w_high | -20.4% |
| adv20 | $7.4M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.86 |
| r_ev_ebit | 0.75 |
| r_roic | 0.97 |
| r_rev_growth | 0.06 |
| r_buyback | 0.34 |
| score | 0.65 |

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
| rank | 105 |

**Screen rationale:** top-quartile FCF yield 17.9%; high ROIC 54.0%; 12-1 momentum 234.7%


## 3. Share count trend

- Shares outstanding: **165,239,947** (CY2026Q2I) vs **162,434,130** prior year (CY2025Q2I)
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
