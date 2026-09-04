# Triage pack — XTNT · Xtant Medical Holdings, Inc.

_Generated 2026-09-04 14:02 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** XTNT · **Name:** Xtant Medical Holdings, Inc.
- **CIK:** 1,453,593
- **SIC:** 3841 — Surgical & Medical Instruments & Apparatus
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** NYSE
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Xtant Medical Holdings, Inc.
- **CIK:** 1,453,593 · **SIC:** 3841 (Surgical & Medical Instruments & Apparatus) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 0.40 |
| mktcap | $56.1M |
| ev | $53.5M |
| ev_ebit | 7.3x |
| fcf | $10.2M |
| fcf_yield | 18.1% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 15.4% |
| net_debt | -$2.6M |
| net_debt_ebit | -0.4x |
| cash | $9.9M |
| ltd | $7.3M |
| equity | $40.0M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $133.9M |
| revenue_prior | $117.3M |
| rev_growth | 14.2% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $7.3M |
| net_income | $5k |
| cfo | $12.5M |
| capex | $2.4M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 7.7% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 140,287,960 |
| shares_py | 130,315,722 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -30.2% |
| r6m | -36.5% |
| off_52w_high | -56.5% |
| adv20 | $1.9M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.87 |
| r_ev_ebit | 0.86 |
| r_roic | 0.81 |
| r_rev_growth | 0.75 |
| r_buyback | 0.15 |
| score | 0.69 |

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
| rank | 69 |

**Screen rationale:** top-quartile FCF yield 18.1%; cheap at 7.3x EV/EBIT; high ROIC 15.4%; revenue +14.2%; net cash


## 3. Share count trend

- Shares outstanding: **140,287,960** (CY2026Q2I) vs **130,315,722** prior year (CY2025Q2I)
- Change: **7.7%** — dilution / growing count
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
