# Triage pack — BATL · BATTALION OIL CORP

_Generated 2026-09-05 02:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** BATL · **Name:** BATTALION OIL CORP
- **CIK:** 1,282,648
- **SIC:** 1311 — Crude Petroleum & Natural Gas
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** NYSE
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** BATTALION OIL CORP
- **CIK:** 1,282,648 · **SIC:** 1311 (Crude Petroleum & Natural Gas) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

> **EARNINGS QUALITY FLAG — one-off items likely.**
> net income more than 3x operating income.
> Reported net income is not supported by the operating engine that is supposed to produce it (typical causes: gains on sale, legal settlements, deferred-tax valuation-allowance releases, bargain-purchase gains). Reconcile net income to operating income in the earnings release (section 7) before treating any earnings-based metric here as repeatable.

**Valuation**

| metric | value |
|---|---|
| price | 1.30 |
| mktcap | $74.5M |
| ev | $147.6M |
| ev_ebit | n/a |
| fcf | $39.1M |
| fcf_yield | 52.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -1.9% |
| net_debt | $73.1M |
| net_debt_ebit | n/a |
| cash | $83.1M |
| ltd | $156.2M |
| equity | $203.1M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $166.0M |
| revenue_prior | $193.9M |
| rev_growth | -14.4% |
| rev_growth_note | share count +248.1% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | net income more than 3x operating income |
| ebit | -$6.6M |
| net_income | $11.9M |
| cfo | $39.1M |
| capex | n/a |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 248.1% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 57,282,155 |
| shares_py | 16,456,563 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 14.0% |
| r6m | -93.2% |
| off_52w_high | -95.3% |
| adv20 | $5.5M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.98 |
| r_ev_ebit | 0.00 |
| r_roic | 0.26 |
| r_rev_growth | 0.07 |
| r_buyback | 0.00 |
| score | 0.21 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q2I |
| shares_period | CY2026Q2I |
| shares_py_period | CY2025Q2I |
| capex_missing | True |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 460 |

**Screen rationale:** top-quartile FCF yield 52.5%; share count +248.1% yoy — growth may be acquisition/issuance-driven, not organic; 12-1 momentum 14.0%; EARNINGS QUALITY: net income more than 3x operating income — one-off items likely; WARNING 6m return below -40%


## 3. Share count trend

- Shares outstanding: **57,282,155** (CY2026Q2I) vs **16,456,563** prior year (CY2025Q2I)
- Change: **248.1%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`
- **Flag:** share count +248.1% yoy — growth may be acquisition/issuance-driven, not organic

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
