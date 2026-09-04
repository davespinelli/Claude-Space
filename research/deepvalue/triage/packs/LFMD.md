# Triage pack — LFMD · LifeMD, Inc.

_Generated 2026-09-04 21:11 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** LFMD · **Name:** LifeMD, Inc.
- **CIK:** 948,320
- **SIC:** 8011 — Services-Offices & Clinics of  Doctors of  Medicine
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** Nasdaq,Nasdaq
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** LifeMD, Inc.
- **CIK:** 948,320 · **SIC:** 8011 (Services-Offices & Clinics of  Doctors of  Medicine) · **Exchange:** Nasdaq,Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 3.05 |
| mktcap | $147.0M |
| ev | $121.9M |
| ev_ebit | n/a |
| fcf | $6.4M |
| fcf_yield | 4.4% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | -$25.1M |
| net_debt_ebit | n/a |
| cash | $25.1M |
| ltd | $0.00 |
| equity | $8.0M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $194.1M |
| revenue_prior | $154.8M |
| rev_growth | 25.3% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$7.7M |
| net_income | -$11.2M |
| cfo | $8.3M |
| capex | $1.9M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 1.7% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 48,200,837 |
| shares_py | 47,417,393 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -39.7% |
| r6m | 1.7% |
| off_52w_high | -56.2% |
| adv20 | $2.4M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.44 |
| r_ev_ebit | 0.00 |
| r_roic | 0.50 |
| r_rev_growth | 0.88 |
| r_buyback | 0.36 |
| score | 0.44 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q2I |
| shares_period | CY2026Q2I |
| shares_py_period | CY2025Q2I |
| capex_missing | False |
| ltd_missing | True |

**Other screen columns**

| metric | value |
|---|---|
| rank | 303 |

**Screen rationale:** revenue +25.3%; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **48,200,837** (CY2026Q2I) vs **47,417,393** prior year (CY2025Q2I)
- Change: **1.7%** — dilution / growing count
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
