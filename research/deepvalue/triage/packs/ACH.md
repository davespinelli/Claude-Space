# Triage pack — ACH · ACCENDRA HEALTH INC/VA/

_Generated 2026-09-05 02:09 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** ACH · **Name:** ACCENDRA HEALTH INC/VA/
- **CIK:** 75,252
- **SIC:** 5047 — Wholesale-Medical, Dental & Hospital Equipment & Supplies
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** NYSE
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** ACCENDRA HEALTH INC/VA/
- **CIK:** 75,252 · **SIC:** 5047 (Wholesale-Medical, Dental & Hospital Equipment & Supplies) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtAndCapitalLeaseObligations

**Valuation**

| metric | value |
|---|---|
| price | 1.22 |
| mktcap | $93.8M |
| ev | $1.8B |
| ev_ebit | 65.7x |
| fcf | -$29.5M |
| fcf_yield | -31.4% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 1.9% |
| net_debt | $1.7B |
| net_debt_ebit | 62.3x |
| cash | $7.7M |
| ltd | $1.7B |
| equity | -$550.9M |
| ltd_tag | LongTermDebtAndCapitalLeaseObligations |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $2.8B |
| revenue_prior | $2.7B |
| rev_growth | 3.1% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $27.5M |
| net_income | -$1.1B |
| cfo | $161.5M |
| capex | $191.0M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -0.4% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 76,904,704 |
| shares_py | 77,244,161 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -46.0% |
| r6m | -48.7% |
| off_52w_high | -78.3% |
| adv20 | $2.8M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.03 |
| r_ev_ebit | 0.10 |
| r_roic | 0.38 |
| r_rev_growth | 0.45 |
| r_buyback | 0.71 |
| score | 0.23 |

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
| rank | 450 |

**Screen rationale:** WARNING 6m return below -40%


## 3. Share count trend

- Shares outstanding: **76,904,704** (CY2026Q2I) vs **77,244,161** prior year (CY2025Q2I)
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
