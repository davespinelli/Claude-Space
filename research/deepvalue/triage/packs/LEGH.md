# Triage pack — LEGH · Legacy Housing Corp

_Generated 2026-09-04 19:09 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** LEGH · **Name:** Legacy Housing Corp
- **CIK:** 1,436,208
- **SIC:** 2451 — Mobile Homes
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** Nasdaq
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Legacy Housing Corp
- **CIK:** 1,436,208 · **SIC:** 2451 (Mobile Homes) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermLineOfCredit

**Valuation**

| metric | value |
|---|---|
| price | 27.89 |
| mktcap | $663.3M |
| ev | $635.2M |
| ev_ebit | 13.1x |
| fcf | $28.2M |
| fcf_yield | 4.2% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 7.2% |
| net_debt | -$28.1M |
| net_debt_ebit | -0.6x |
| cash | $29.0M |
| ltd | $899k |
| equity | $562.2M |
| ltd_tag | LongTermLineOfCredit |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $164.6M |
| revenue_prior | $184.2M |
| rev_growth | -10.7% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $48.4M |
| net_income | $41.8M |
| cfo | $37.2M |
| capex | $9.0M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -0.4% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 23,781,601 |
| shares_py | 23,868,727 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -0.0% |
| r6m | 35.1% |
| off_52w_high | -4.9% |
| adv20 | $2.8M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.44 |
| r_ev_ebit | 0.66 |
| r_roic | 0.60 |
| r_rev_growth | 0.09 |
| r_buyback | 0.70 |
| score | 0.50 |

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
| rank | 243 |

**Screen rationale:** net cash


## 3. Share count trend

- Shares outstanding: **23,781,601** (CY2026Q2I) vs **23,868,727** prior year (CY2025Q2I)
- Change: **-0.4%** — roughly flat
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
