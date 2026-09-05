# Triage pack — CURR · Currenc Group Inc.

_Generated 2026-09-05 02:09 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** CURR · **Name:** Currenc Group Inc.
- **CIK:** 1,862,935
- **SIC:** 7389 — Services-Business Services, NEC
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** Nasdaq
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Currenc Group Inc.
- **CIK:** 1,862,935 · **SIC:** 7389 (Services-Business Services, NEC) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebt

**Valuation**

| metric | value |
|---|---|
| price | 3.00 |
| mktcap | $229.8M |
| ev | $155.7M |
| ev_ebit | n/a |
| fcf | $7.4M |
| fcf_yield | 3.2% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | -$74.1M |
| net_debt_ebit | n/a |
| cash | $75.2M |
| ltd | $1.2M |
| equity | -$5.7M |
| ltd_tag | LongTermDebt |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $37.8M |
| revenue_prior | $46.4M |
| rev_growth | -18.6% |
| rev_growth_note | share count +64.7% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | n/a |
| ebit | -$7.9M |
| net_income | -$18.4M |
| cfo | $7.9M |
| capex | $479k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 64.7% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 76,611,444 |
| shares_py | 46,527,999 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 92.4% |
| r6m | 33.3% |
| off_52w_high | -33.2% |
| adv20 | $2.4M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.39 |
| r_ev_ebit | 0.00 |
| r_roic | 0.50 |
| r_rev_growth | 0.04 |
| r_buyback | 0.03 |
| score | 0.24 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2025Q4I |
| shares_period | CY2025Q4I |
| shares_py_period | CY2025Q2I |
| capex_missing | False |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 447 |

**Screen rationale:** share count +64.7% yoy — growth may be acquisition/issuance-driven, not organic; 12-1 momentum 92.4%


## 3. Share count trend

- Shares outstanding: **76,611,444** (CY2025Q4I) vs **46,527,999** prior year (CY2025Q2I)
- Change: **64.7%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`
- **Flag:** share count +64.7% yoy — growth may be acquisition/issuance-driven, not organic

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
