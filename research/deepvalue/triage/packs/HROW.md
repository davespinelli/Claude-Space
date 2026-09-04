# Triage pack — HROW · HARROW, INC.

_Generated 2026-09-04 17:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** HROW · **Name:** HARROW, INC.
- **CIK:** 1,360,214
- **SIC:** 2834 — Pharmaceutical Preparations
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** Nasdaq
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** HARROW, INC.
- **CIK:** 1,360,214 · **SIC:** 2834 (Pharmaceutical Preparations) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermNotesPayable

**Valuation**

| metric | value |
|---|---|
| price | 38.26 |
| mktcap | $1.4B |
| ev | $1.6B |
| ev_ebit | 53.8x |
| fcf | $43.0M |
| fcf_yield | 3.0% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 10.8% |
| net_debt | $208.5M |
| net_debt_ebit | 6.8x |
| cash | $83.9M |
| ltd | $292.4M |
| equity | $15.2M |
| ltd_tag | LongTermNotesPayable |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $272.3M |
| revenue_prior | $199.6M |
| rev_growth | 36.4% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $30.5M |
| net_income | -$5.1M |
| cfo | $43.9M |
| capex | $887k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 1.3% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 37,487,850 |
| shares_py | 37,002,136 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 5.5% |
| r6m | 5.8% |
| off_52w_high | -30.2% |
| adv20 | $23.1M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.37 |
| r_ev_ebit | 0.12 |
| r_roic | 0.73 |
| r_rev_growth | 0.91 |
| r_buyback | 0.41 |
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
| rank | 184 |

**Screen rationale:** revenue +36.4%; 12-1 momentum 5.5%


## 3. Share count trend

- Shares outstanding: **37,487,850** (CY2026Q2I) vs **37,002,136** prior year (CY2025Q2I)
- Change: **1.3%** — dilution / growing count
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
