# Triage pack — GEVO · Gevo, Inc.

_Generated 2026-09-05 00:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** GEVO · **Name:** Gevo, Inc.
- **CIK:** 1,392,380
- **SIC:** 2860 — Industrial Organic Chemicals
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** Nasdaq
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Gevo, Inc.
- **CIK:** 1,392,380 · **SIC:** 2860 (Industrial Organic Chemicals) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 1.64 |
| mktcap | $405.5M |
| ev | $514.6M |
| ev_ebit | n/a |
| fcf | -$43.5M |
| fcf_yield | -10.7% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -4.2% |
| net_debt | $109.1M |
| net_debt_ebit | n/a |
| cash | $58.1M |
| ltd | $167.2M |
| equity | $273.2M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $160.6M |
| revenue_prior | $16.9M |
| rev_growth | 849.3% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$20.2M |
| net_income | -$33.8M |
| cfo | -$13.4M |
| capex | $30.1M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 2.2% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 247,237,104 |
| shares_py | 241,839,083 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -6.1% |
| r6m | -13.2% |
| off_52w_high | -41.0% |
| adv20 | $4.1M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.08 |
| r_ev_ebit | 0.00 |
| r_roic | 0.20 |
| r_rev_growth | 1.00 |
| r_buyback | 0.31 |
| score | 0.32 |

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
| rank | 389 |

**Screen rationale:** revenue +849.3%


## 3. Share count trend

- Shares outstanding: **247,237,104** (CY2026Q2I) vs **241,839,083** prior year (CY2025Q2I)
- Change: **2.2%** — dilution / growing count
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
