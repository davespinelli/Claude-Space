# Triage pack — TGLS · Tecnoglass Holdings Inc.

_Generated 2026-09-04 13:59 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** TGLS · **Name:** Tecnoglass Holdings Inc.
- **CIK:** 1,534,675
- **SIC:** 3211 — Flat Glass
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** NYSE
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Tecnoglass Holdings Inc.
- **CIK:** 1,534,675 · **SIC:** 3211 (Flat Glass) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 39.26 |
| mktcap | $1.7B |
| ev | $1.9B |
| ev_ebit | 8.1x |
| fcf | $34.5M |
| fcf_yield | 2.0% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 19.7% |
| net_debt | $138.4M |
| net_debt_ebit | 0.6x |
| cash | $80.8M |
| ltd | $219.2M |
| equity | $788.8M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $983.6M |
| revenue_prior | $890.2M |
| rev_growth | 10.5% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $230.7M |
| net_income | $159.6M |
| cfo | $135.8M |
| capex | $101.3M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -5.6% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 44,364,616 |
| shares_py | 46,987,148 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -31.8% |
| r6m | -10.4% |
| off_52w_high | -46.3% |
| adv20 | $9.6M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.30 |
| r_ev_ebit | 0.82 |
| r_roic | 0.87 |
| r_rev_growth | 0.67 |
| r_buyback | 0.89 |
| score | 0.71 |

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
| rank | 56 |

**Screen rationale:** cheap at 8.1x EV/EBIT; high ROIC 19.7%; buying back stock -5.6%


## 3. Share count trend

- Shares outstanding: **44,364,616** (CY2026Q2I) vs **46,987,148** prior year (CY2025Q2I)
- Change: **-5.6%** — buyback / shrinking count
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
