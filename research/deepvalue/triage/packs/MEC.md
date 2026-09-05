# Triage pack — MEC · Mayville Engineering Company, Inc.

_Generated 2026-09-05 02:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** MEC · **Name:** Mayville Engineering Company, Inc.
- **CIK:** 1,766,368
- **SIC:** 3460 — Metal Forgings & Stampings
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** NYSE
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Mayville Engineering Company, Inc.
- **CIK:** 1,766,368 · **SIC:** 3460 (Metal Forgings & Stampings) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermLineOfCredit

**Valuation**

| metric | value |
|---|---|
| price | 19.43 |
| mktcap | $495.5M |
| ev | $619.0M |
| ev_ebit | n/a |
| fcf | $26.9M |
| fcf_yield | 5.4% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -0.7% |
| net_debt | $123.5M |
| net_debt_ebit | n/a |
| cash | $2.2M |
| ltd | $125.7M |
| equity | $325.5M |
| ltd_tag | LongTermLineOfCredit |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $546.5M |
| revenue_prior | $581.6M |
| rev_growth | -6.0% |
| rev_growth_note | share count +25.5% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | n/a |
| ebit | -$3.8M |
| net_income | -$8.1M |
| cfo | $38.6M |
| capex | $11.6M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 25.5% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 25,500,331 |
| shares_py | 20,317,825 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 79.8% |
| r6m | 3.1% |
| off_52w_high | -48.2% |
| adv20 | $11.9M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.52 |
| r_ev_ebit | 0.00 |
| r_roic | 0.28 |
| r_rev_growth | 0.16 |
| r_buyback | 0.06 |
| score | 0.25 |

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
| rank | 442 |

**Screen rationale:** share count +25.5% yoy — growth may be acquisition/issuance-driven, not organic; 12-1 momentum 79.8%


## 3. Share count trend

- Shares outstanding: **25,500,331** (CY2026Q2I) vs **20,317,825** prior year (CY2025Q2I)
- Change: **25.5%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`
- **Flag:** share count +25.5% yoy — growth may be acquisition/issuance-driven, not organic

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
