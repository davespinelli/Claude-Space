# Triage pack — LTRX · LANTRONIX INC

_Generated 2026-09-05 02:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** LTRX · **Name:** LANTRONIX INC
- **CIK:** 1,114,925
- **SIC:** 3576 — Computer Communications Equipment
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** Nasdaq
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** LANTRONIX INC
- **CIK:** 1,114,925 · **SIC:** 3576 (Computer Communications Equipment) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 5.22 |
| mktcap | $207.8M |
| ev | $147.4M |
| ev_ebit | n/a |
| fcf | $6.8M |
| fcf_yield | 3.3% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -14.8% |
| net_debt | -$60.5M |
| net_debt_ebit | n/a |
| cash | $60.5M |
| ltd | $0.00 |
| equity | $119.3M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $122.9M |
| revenue_prior | $160.3M |
| rev_growth | -23.3% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$11.0M |
| net_income | -$11.4M |
| cfo | $7.3M |
| capex | $505k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 2.4% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 39,816,930 |
| shares_py | 38,890,328 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 28.0% |
| r6m | -11.8% |
| off_52w_high | -38.2% |
| adv20 | $6.5M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.39 |
| r_ev_ebit | 0.00 |
| r_roic | 0.08 |
| r_rev_growth | 0.02 |
| r_buyback | 0.30 |
| score | 0.21 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q2I |
| shares_period | CY2026Q1I |
| shares_py_period | CY2025Q1I |
| capex_missing | False |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 462 |

**Screen rationale:** 12-1 momentum 28.0%


## 3. Share count trend

- Shares outstanding: **39,816,930** (CY2026Q1I) vs **38,890,328** prior year (CY2025Q1I)
- Change: **2.4%** — dilution / growing count
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
