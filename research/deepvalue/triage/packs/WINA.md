# Triage pack — WINA · WINMARK CORP

_Generated 2026-09-04 20:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** WINA · **Name:** WINMARK CORP
- **CIK:** 908,315
- **SIC:** 5900 — Retail-Miscellaneous Retail
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** Nasdaq
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** WINMARK CORP
- **CIK:** 908,315 · **SIC:** 5900 (Retail-Miscellaneous Retail) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermNotesPayable

**Valuation**

| metric | value |
|---|---|
| price | 317.40 |
| mktcap | $1.1B |
| ev | $1.1B |
| ev_ebit | 21.0x |
| fcf | $44.7M |
| fcf_yield | 3.9% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | $4.1M |
| net_debt_ebit | 0.1x |
| cash | $25.8M |
| ltd | $30.0M |
| equity | -$37.6M |
| ltd_tag | LongTermNotesPayable |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $86.1M |
| revenue_prior | $81.3M |
| rev_growth | 5.9% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $54.6M |
| net_income | $41.7M |
| cfo | $44.9M |
| capex | $192k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 1.2% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 3,592,169 |
| shares_py | 3,548,458 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -19.4% |
| r6m | -29.5% |
| off_52w_high | -36.6% |
| adv20 | $16.6M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.43 |
| r_ev_ebit | 0.43 |
| r_roic | 0.50 |
| r_rev_growth | 0.55 |
| r_buyback | 0.42 |
| score | 0.47 |

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
| rank | 275 |

**Screen rationale:** balanced across factors, no single standout


## 3. Share count trend

- Shares outstanding: **3,592,169** (CY2026Q2I) vs **3,548,458** prior year (CY2025Q2I)
- Change: **1.2%** — dilution / growing count
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
