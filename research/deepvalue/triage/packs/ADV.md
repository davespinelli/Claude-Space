# Triage pack — ADV · Advantage Solutions Inc.

_Generated 2026-09-04 18:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** ADV · **Name:** Advantage Solutions Inc.
- **CIK:** 1,776,661
- **SIC:** 7389 — Services-Business Services, NEC
- **Fiscal year end (MM-DD):** n/a
- **Exchange:** Nasdaq
- **Filings fetched:** none

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Advantage Solutions Inc.
- **CIK:** 1,776,661 · **SIC:** 7389 (Services-Business Services, NEC) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 31.92 |
| mktcap | $409.3M |
| ev | $1.8B |
| ev_ebit | n/a |
| fcf | $55.1M |
| fcf_yield | 13.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | $1.4B |
| net_debt_ebit | n/a |
| cash | $102.3M |
| ltd | $1.5B |
| equity | n/a |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $3.5B |
| revenue_prior | $3.6B |
| rev_growth | -0.7% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$126.5M |
| net_income | -$227.7M |
| cfo | $61.5M |
| capex | $6.5M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -96.1% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 12,822,230 |
| shares_py | 325,946,871 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -21.8% |
| r6m | 110.7% |
| off_52w_high | -34.9% |
| adv20 | $2.8M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.80 |
| r_ev_ebit | 0.00 |
| r_roic | 0.50 |
| r_rev_growth | 0.32 |
| r_buyback | 1.00 |
| score | 0.52 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | n/a |
| shares_period | CY2026Q2I |
| shares_py_period | CY2025Q2I |
| capex_missing | False |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 221 |

**Screen rationale:** top-quartile FCF yield 13.5%; buying back stock -96.1%


## 3. Share count trend

- Shares outstanding: **12,822,230** (CY2026Q2I) vs **325,946,871** prior year (CY2025Q2I)
- Change: **-96.1%** — buyback / shrinking count
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
