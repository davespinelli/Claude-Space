# Triage pack — TUYA · Tuya Inc.

_Generated 2026-09-04 21:09 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** TUYA · **Name:** Tuya Inc.
- **CIK:** 1,829,118
- **SIC:** 7372 — Services-Prepackaged Software
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** NYSE
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Tuya Inc.
- **CIK:** 1,829,118 · **SIC:** 7372 (Services-Prepackaged Software) · **Exchange:** NYSE

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

> **EARNINGS QUALITY FLAG — one-off items likely.**
> net income more than 3x operating income.
> Reported net income is not supported by the operating engine that is supposed to produce it (typical causes: gains on sale, legal settlements, deferred-tax valuation-allowance releases, bargain-purchase gains). Reconcile net income to operating income in the earnings release (section 7) before treating any earnings-based metric here as repeatable.

**Valuation**

| metric | value |
|---|---|
| price | 1.90 |
| mktcap | $1.2B |
| ev | $271.2M |
| ev_ebit | 23.6x |
| fcf | $73.9M |
| fcf_yield | 6.4% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 6.9% |
| net_debt | -$890.7M |
| net_debt_ebit | -77.6x |
| cash | $890.7M |
| ltd | $0.00 |
| equity | $1.0B |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $321.8M |
| revenue_prior | $298.6M |
| rev_growth | 7.8% |
| rev_growth_note | n/a |
| eq_flag | net income more than 3x operating income |
| ebit | $11.5M |
| net_income | $57.9M |
| cfo | $81.0M |
| capex | $7.1M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 6.6% |
| share_chg_src | us-gaap:WeightedAverageNumberOfSharesOutstandingBasic CY2025 vs CY2024 |
| shares | 611,528,176 |
| shares_py | n/a |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -29.4% |
| r6m | -21.4% |
| off_52w_high | -27.5% |
| adv20 | $1.1M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.56 |
| r_ev_ebit | 0.37 |
| r_roic | 0.59 |
| r_rev_growth | 0.59 |
| r_buyback | 0.16 |
| score | 0.45 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2025Q4I |
| shares_period | CY2025Q4I |
| shares_py_period | n/a |
| capex_missing | False |
| ltd_missing | True |

**Other screen columns**

| metric | value |
|---|---|
| rank | 289 |

**Screen rationale:** debt data missing (net cash unverified); EARNINGS QUALITY: net income more than 3x operating income — one-off items likely


## 3. Share count trend

- Change: **6.6%** — dilution / growing count
- Source concept: `us-gaap:WeightedAverageNumberOfSharesOutstandingBasic CY2025 vs CY2024`

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
