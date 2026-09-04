# Triage pack — CTRN · Citi Trends Inc

_Generated 2026-09-04 20:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** CTRN · **Name:** Citi Trends Inc
- **CIK:** 1,318,484
- **SIC:** 5600 — Retail-Apparel & Accessory Stores
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** Nasdaq
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Citi Trends Inc
- **CIK:** 1,318,484 · **SIC:** 5600 (Retail-Apparel & Accessory Stores) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 69.14 |
| mktcap | $575.9M |
| ev | $494.8M |
| ev_ebit | 128.5x |
| fcf | $624k |
| fcf_yield | 0.1% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 6.9% |
| net_debt | -$81.1M |
| net_debt_ebit | -21.1x |
| cash | $81.1M |
| ltd | $0.00 |
| equity | $125.3M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $820.0M |
| revenue_prior | $753.1M |
| rev_growth | 8.9% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $3.9M |
| net_income | $5.2M |
| cfo | $21.0M |
| capex | $20.3M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 0.4% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 8,329,848 |
| shares_py | 8,294,051 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 97.9% |
| r6m | 43.7% |
| off_52w_high | -9.2% |
| adv20 | $11.8M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.21 |
| r_ev_ebit | 0.05 |
| r_roic | 0.59 |
| r_rev_growth | 0.62 |
| r_buyback | 0.58 |
| score | 0.46 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q1I |
| shares_period | CY2026Q2I |
| shares_py_period | CY2025Q2I |
| capex_missing | False |
| ltd_missing | True |

**Other screen columns**

| metric | value |
|---|---|
| rank | 280 |

**Screen rationale:** debt data missing (net cash unverified); 12-1 momentum 97.9%


## 3. Share count trend

- Shares outstanding: **8,329,848** (CY2026Q2I) vs **8,294,051** prior year (CY2025Q2I)
- Change: **0.4%** — roughly flat
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
