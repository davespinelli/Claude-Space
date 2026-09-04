# Triage pack — XNET · Xunlei Ltd

_Generated 2026-09-04 23:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** XNET · **Name:** Xunlei Ltd
- **CIK:** 1,510,593
- **SIC:** 7372 — Services-Prepackaged Software
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** Nasdaq
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Xunlei Ltd
- **CIK:** 1,510,593 · **SIC:** 7372 (Services-Prepackaged Software) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

> **EARNINGS QUALITY FLAG — one-off items likely.**
> net income exceeds revenue; net income more than 3x operating income.
> Reported net income is not supported by the operating engine that is supposed to produce it (typical causes: gains on sale, legal settlements, deferred-tax valuation-allowance releases, bargain-purchase gains). Reconcile net income to operating income in the earnings release (section 7) before treating any earnings-based metric here as repeatable.

**Valuation**

| metric | value |
|---|---|
| price | 4.90 |
| mktcap | $1.5B |
| ev | $1.4B |
| ev_ebit | 214.4x |
| fcf | $27.1M |
| fcf_yield | 1.8% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 0.4% |
| net_debt | -$118.6M |
| net_debt_ebit | -17.9x |
| cash | $157.0M |
| ltd | $38.4M |
| equity | $1.4B |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $460.4M |
| revenue_prior | $323.1M |
| rev_growth | 42.5% |
| rev_growth_note | n/a |
| eq_flag | net income exceeds revenue; net income more than 3x operating income |
| ebit | $6.6M |
| net_income | $1.0B |
| cfo | $32.5M |
| capex | $5.3M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 2.3% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 314,277,001 |
| shares_py | 307,351,196 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -33.3% |
| r6m | -13.4% |
| off_52w_high | -54.5% |
| adv20 | $1.2M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.29 |
| r_ev_ebit | 0.03 |
| r_roic | 0.32 |
| r_rev_growth | 0.94 |
| r_buyback | 0.31 |
| score | 0.38 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2025Q4I |
| shares_period | CY2025Q4I |
| shares_py_period | CY2024Q4I |
| capex_missing | False |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 347 |

**Screen rationale:** revenue +42.5%; net cash; EARNINGS QUALITY: net income exceeds revenue; net income more than 3x operating income — one-off items likely


## 3. Share count trend

- Shares outstanding: **314,277,001** (CY2025Q4I) vs **307,351,196** prior year (CY2024Q4I)
- Change: **2.3%** — dilution / growing count
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
