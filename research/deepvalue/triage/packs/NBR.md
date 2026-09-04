# Triage pack — NBR · NABORS INDUSTRIES LTD

_Generated 2026-09-04 17:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** NBR · **Name:** NABORS INDUSTRIES LTD
- **CIK:** 1,163,739
- **SIC:** 1381 — Drilling Oil & Gas Wells
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** NYSE
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** NABORS INDUSTRIES LTD
- **CIK:** 1,163,739 · **SIC:** 1381 (Drilling Oil & Gas Wells) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 92.97 |
| mktcap | $1.5B |
| ev | $3.1B |
| ev_ebit | 6.6x |
| fcf | -$22.7M |
| fcf_yield | -1.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 17.3% |
| net_debt | $1.6B |
| net_debt_ebit | 3.4x |
| cash | $509.8M |
| ltd | $2.1B |
| equity | $544.1M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $3.2B |
| revenue_prior | $2.9B |
| rev_growth | 8.7% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $471.1M |
| net_income | $286.6M |
| cfo | $693.3M |
| capex | $715.9M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 9.5% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 15,961,327 |
| shares_py | 14,575,667 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 122.4% |
| r6m | 19.2% |
| off_52w_high | -16.0% |
| adv20 | $19.2M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.16 |
| r_ev_ebit | 0.89 |
| r_roic | 0.85 |
| r_rev_growth | 0.62 |
| r_buyback | 0.13 |
| score | 0.58 |

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
| rank | 168 |

**Screen rationale:** cheap at 6.6x EV/EBIT; high ROIC 17.3%; 12-1 momentum 122.4%


## 3. Share count trend

- Shares outstanding: **15,961,327** (CY2026Q2I) vs **14,575,667** prior year (CY2025Q2I)
- Change: **9.5%** — dilution / growing count
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
