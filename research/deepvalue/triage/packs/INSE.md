# Triage pack — INSE · Inspired Entertainment, Inc.

_Generated 2026-09-04 15:08 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** INSE · **Name:** Inspired Entertainment, Inc.
- **CIK:** 1,615,063
- **SIC:** 7372 — Services-Prepackaged Software
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** Nasdaq
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Inspired Entertainment, Inc.
- **CIK:** 1,615,063 · **SIC:** 7372 (Services-Prepackaged Software) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 5.59 |
| mktcap | $147.3M |
| ev | $443.5M |
| ev_ebit | 14.5x |
| fcf | $16.3M |
| fcf_yield | 11.1% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 8.6% |
| net_debt | $296.2M |
| net_debt_ebit | 9.7x |
| cash | $23.2M |
| ltd | $319.4M |
| equity | -$15.6M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $304.1M |
| revenue_prior | $297.1M |
| rev_growth | 2.4% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $30.5M |
| net_income | -$17.0M |
| cfo | $52.0M |
| capex | $35.7M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -2.1% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 26,358,372 |
| shares_py | 26,920,506 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -23.2% |
| r6m | -30.6% |
| off_52w_high | -43.1% |
| adv20 | $1.2M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.74 |
| r_ev_ebit | 0.61 |
| r_roic | 0.67 |
| r_rev_growth | 0.42 |
| r_buyback | 0.79 |
| score | 0.65 |

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
| rank | 106 |

**Screen rationale:** buying back stock -2.1%


## 3. Share count trend

- Shares outstanding: **26,358,372** (CY2026Q2I) vs **26,920,506** prior year (CY2025Q2I)
- Change: **-2.1%** — buyback / shrinking count
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
