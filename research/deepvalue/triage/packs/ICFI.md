# Triage pack — ICFI · ICF International, Inc.

_Generated 2026-09-04 17:11 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** ICFI · **Name:** ICF International, Inc.
- **CIK:** 1,362,004
- **SIC:** 8742 — Services-Management Consulting Services
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** Nasdaq
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** ICF International, Inc.
- **CIK:** 1,362,004 · **SIC:** 8742 (Services-Management Consulting Services) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 90.00 |
| mktcap | $1.6B |
| ev | $2.0B |
| ev_ebit | 13.9x |
| fcf | $120.2M |
| fcf_yield | 7.4% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 7.9% |
| net_debt | $401.6M |
| net_debt_ebit | 2.8x |
| cash | $4.6M |
| ltd | $406.2M |
| equity | $1.0B |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $1.9B |
| revenue_prior | $2.0B |
| rev_growth | -7.3% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $145.5M |
| net_income | $92.0M |
| cfo | $141.9M |
| capex | $21.7M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -2.7% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 17,933,884 |
| shares_py | 18,428,490 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -11.2% |
| r6m | 20.7% |
| off_52w_high | -10.0% |
| adv20 | $17.8M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.61 |
| r_ev_ebit | 0.62 |
| r_roic | 0.64 |
| r_rev_growth | 0.14 |
| r_buyback | 0.82 |
| score | 0.56 |

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
| rank | 180 |

**Screen rationale:** buying back stock -2.7%


## 3. Share count trend

- Shares outstanding: **17,933,884** (CY2026Q2I) vs **18,428,490** prior year (CY2025Q2I)
- Change: **-2.7%** — buyback / shrinking count
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
