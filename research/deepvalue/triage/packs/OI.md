# Triage pack — OI · O-I Glass, Inc. /DE/

_Generated 2026-09-05 00:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** OI · **Name:** O-I Glass, Inc. /DE/
- **CIK:** 812,074
- **SIC:** 3221 — Glass Containers
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** NYSE
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** O-I Glass, Inc. /DE/
- **CIK:** 812,074 · **SIC:** 3221 (Glass Containers) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 7.03 |
| mktcap | $1.1B |
| ev | $5.5B |
| ev_ebit | 145.6x |
| fcf | $168.0M |
| fcf_yield | 15.6% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 0.5% |
| net_debt | $4.5B |
| net_debt_ebit | 117.2x |
| cash | $339.0M |
| ltd | $4.8B |
| equity | $1.3B |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $6.4B |
| revenue_prior | $6.5B |
| rev_growth | -1.6% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $38.0M |
| net_income | -$129.0M |
| cfo | $600.0M |
| capex | $432.0M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -0.3% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 153,659,747 |
| shares_py | 154,073,257 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -40.1% |
| r6m | -41.3% |
| off_52w_high | -57.7% |
| adv20 | $19.3M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.83 |
| r_ev_ebit | 0.05 |
| r_roic | 0.33 |
| r_rev_growth | 0.29 |
| r_buyback | 0.70 |
| score | 0.34 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2024 |
| equity_period | CY2025Q4I |
| shares_period | CY2026Q2I |
| shares_py_period | CY2025Q2I |
| capex_missing | False |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 374 |

**Screen rationale:** top-quartile FCF yield 15.6%; WARNING 6m return below -40%


## 3. Share count trend

- Shares outstanding: **153,659,747** (CY2026Q2I) vs **154,073,257** prior year (CY2025Q2I)
- Change: **-0.3%** — roughly flat
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
