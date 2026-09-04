# Triage pack — MUX · McEwen Inc.

_Generated 2026-09-04 23:11 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** MUX · **Name:** McEwen Inc.
- **CIK:** 314,203
- **SIC:** 1040 — Gold and Silver Ores
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** NYSE
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** McEwen Inc.
- **CIK:** 314,203 · **SIC:** 1040 (Gold and Silver Ores) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 20.54 |
| mktcap | $1.3B |
| ev | $1.3B |
| ev_ebit | 490.8x |
| fcf | $6.9M |
| fcf_yield | 0.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | $41.7M |
| net_debt_ebit | 15.7x |
| cash | $78.9M |
| ltd | $120.6M |
| equity | n/a |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $197.6M |
| revenue_prior | $174.5M |
| rev_growth | 13.2% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $2.7M |
| net_income | -$1.3M |
| cfo | $6.9M |
| capex | n/a |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 13.4% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 61,358,566 |
| shares_py | 54,106,415 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 41.7% |
| r6m | -15.1% |
| off_52w_high | -29.3% |
| adv20 | $22.5M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.24 |
| r_ev_ebit | 0.01 |
| r_roic | 0.50 |
| r_rev_growth | 0.73 |
| r_buyback | 0.10 |
| score | 0.36 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | n/a |
| shares_period | CY2026Q2I |
| shares_py_period | CY2025Q2I |
| capex_missing | True |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 355 |

**Screen rationale:** 12-1 momentum 41.7%


## 3. Share count trend

- Shares outstanding: **61,358,566** (CY2026Q2I) vs **54,106,415** prior year (CY2025Q2I)
- Change: **13.4%** — dilution / growing count
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
