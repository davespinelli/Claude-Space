# Triage pack — AMPY · Amplify Energy Corp.

_Generated 2026-09-04 15:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** AMPY · **Name:** Amplify Energy Corp.
- **CIK:** 1,533,924
- **SIC:** 1311 — Crude Petroleum & Natural Gas
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** NYSE
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Amplify Energy Corp.
- **CIK:** 1,533,924 · **SIC:** 1311 (Crude Petroleum & Natural Gas) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 4.90 |
| mktcap | $203.1M |
| ev | $181.9M |
| ev_ebit | 2.4x |
| fcf | $49.2M |
| fcf_yield | 24.2% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 14.5% |
| net_debt | -$21.2M |
| net_debt_ebit | -0.3x |
| cash | $21.2M |
| ltd | $0.00 |
| equity | $439.1M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $263.4M |
| revenue_prior | $294.7M |
| rev_growth | -10.6% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $76.9M |
| net_income | $44.0M |
| cfo | $49.2M |
| capex | n/a |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 2.4% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 41,456,450 |
| shares_py | 40,466,053 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -1.3% |
| r6m | -18.3% |
| off_52w_high | -26.1% |
| adv20 | $4.6M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.92 |
| r_ev_ebit | 0.99 |
| r_roic | 0.79 |
| r_rev_growth | 0.10 |
| r_buyback | 0.29 |
| score | 0.62 |

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
| rank | 124 |

**Screen rationale:** top-quartile FCF yield 24.2%; cheap at 2.4x EV/EBIT; high ROIC 14.5%; net cash


## 3. Share count trend

- Shares outstanding: **41,456,450** (CY2026Q2I) vs **40,466,053** prior year (CY2025Q2I)
- Change: **2.4%** — dilution / growing count
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
