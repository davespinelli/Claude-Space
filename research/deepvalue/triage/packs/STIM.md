# Triage pack — STIM · Neuronetics, Inc.

_Generated 2026-09-05 02:09 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** STIM · **Name:** Neuronetics, Inc.
- **CIK:** 1,227,636
- **SIC:** 3841 — Surgical & Medical Instruments & Apparatus
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** Nasdaq
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Neuronetics, Inc.
- **CIK:** 1,227,636 · **SIC:** 3841 (Surgical & Medical Instruments & Apparatus) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

> **EARNINGS QUALITY FLAG — one-off items likely.**
> revenue growth above 50% alongside share count growth above 15% (bought, not organic).
> Reported net income is not supported by the operating engine that is supposed to produce it (typical causes: gains on sale, legal settlements, deferred-tax valuation-allowance releases, bargain-purchase gains). Reconcile net income to operating income in the earnings release (section 7) before treating any earnings-based metric here as repeatable.

**Valuation**

| metric | value |
|---|---|
| price | 2.72 |
| mktcap | $207.3M |
| ev | $249.6M |
| ev_ebit | n/a |
| fcf | -$21.2M |
| fcf_yield | -10.2% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -41.3% |
| net_debt | $42.3M |
| net_debt_ebit | n/a |
| cash | $19.2M |
| ltd | $61.5M |
| equity | $17.9M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $149.2M |
| revenue_prior | $74.9M |
| rev_growth | 99.2% |
| rev_growth_note | share count +15.2% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | revenue growth above 50% alongside share count growth above 15% (bought, not organic) |
| ebit | -$31.4M |
| net_income | -$39.0M |
| cfo | -$20.4M |
| capex | $801k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 15.2% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 76,197,222 |
| shares_py | 66,124,820 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -28.1% |
| r6m | 92.9% |
| off_52w_high | -26.3% |
| adv20 | $8.9M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.08 |
| r_ev_ebit | 0.00 |
| r_roic | 0.01 |
| r_rev_growth | 0.97 |
| r_buyback | 0.09 |
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
| rank | 451 |

**Screen rationale:** revenue +99.2% BUT share count +15.2% yoy — growth may be acquisition/issuance-driven, not organic; EARNINGS QUALITY: revenue growth above 50% alongside share count growth above 15% (bought, not organic) — one-off items likely


## 3. Share count trend

- Shares outstanding: **76,197,222** (CY2026Q2I) vs **66,124,820** prior year (CY2025Q2I)
- Change: **15.2%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`
- **Flag:** share count +15.2% yoy — growth may be acquisition/issuance-driven, not organic

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
