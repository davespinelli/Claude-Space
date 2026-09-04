# Triage pack — PAYS · Paysign, Inc.

_Generated 2026-09-04 19:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** PAYS · **Name:** Paysign, Inc.
- **CIK:** 1,496,443
- **SIC:** 7389 — Services-Business Services, NEC
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** Nasdaq
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Paysign, Inc.
- **CIK:** 1,496,443 · **SIC:** 7389 (Services-Business Services, NEC) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 12.96 |
| mktcap | $731.7M |
| ev | $558.8M |
| ev_ebit | 75.9x |
| fcf | $51.2M |
| fcf_yield | 7.0% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | -$172.9M |
| net_debt_ebit | -23.5x |
| cash | $176.5M |
| ltd | $3.6M |
| equity | $60.2M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $82.0M |
| revenue_prior | $58.4M |
| rev_growth | 40.5% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $7.4M |
| net_income | $7.6M |
| cfo | $52.5M |
| capex | $1.2M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 3.7% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 56,462,156 |
| shares_py | 54,451,888 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 81.3% |
| r6m | 236.6% |
| off_52w_high | -8.3% |
| adv20 | $9.3M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.59 |
| r_ev_ebit | 0.08 |
| r_roic | 0.50 |
| r_rev_growth | 0.93 |
| r_buyback | 0.23 |
| score | 0.52 |

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
| rank | 230 |

**Screen rationale:** revenue +40.5%; net cash; 12-1 momentum 81.3%


## 3. Share count trend

- Shares outstanding: **56,462,156** (CY2026Q2I) vs **54,451,888** prior year (CY2025Q2I)
- Change: **3.7%** — dilution / growing count
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
