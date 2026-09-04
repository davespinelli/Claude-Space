# Triage pack — HSHP · Himalaya Shipping Ltd.

_Generated 2026-09-04 19:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** HSHP · **Name:** Himalaya Shipping Ltd.
- **CIK:** 0001959455
- **SIC:** 4412 — Deep Sea Foreign Transportation of  Freight
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/HSHP

**Fetcher warnings for this ticker:** 10-K 2026-03-12: heading split missed Item 1 - Business, Item 1A - Risk Factors, Item 7 - MD&A; no 10-Q in recent filings; no proxy (DEF 14A) in recent filings

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Himalaya Shipping Ltd.
- **CIK:** 1,959,455 · **SIC:** 4412 (Deep Sea Foreign Transportation of  Freight) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 17.93 |
| mktcap | $836.4M |
| ev | $1.5B |
| ev_ebit | 21.3x |
| fcf | $51.7M |
| fcf_yield | 6.2% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 6.9% |
| net_debt | $618.6M |
| net_debt_ebit | 9.1x |
| cash | $34.8M |
| ltd | $653.4M |
| equity | $161.7M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $131.9M |
| revenue_prior | $123.6M |
| rev_growth | 6.7% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $68.2M |
| net_income | $17.7M |
| cfo | $51.7M |
| capex | n/a |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 6.3% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 46,650,000 |
| shares_py | 43,900,000 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 109.0% |
| r6m | 36.4% |
| off_52w_high | 0.0% |
| adv20 | $5.3M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.55 |
| r_ev_ebit | 0.42 |
| r_roic | 0.59 |
| r_rev_growth | 0.57 |
| r_buyback | 0.17 |
| score | 0.51 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2025Q4I |
| shares_period | CY2025Q4I |
| shares_py_period | CY2024Q4I |
| capex_missing | True |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 233 |

**Screen rationale:** 12-1 momentum 109.0%


## 3. Share count trend

- Shares outstanding: **46,650,000** (CY2025Q4I) vs **43,900,000** prior year (CY2024Q4I)
- Change: **6.3%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No 8-K filings fetched for this ticker._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 4,000 sh / $56,800 vs sells 400,000 sh / $5,605,000 -> net $-5,548,200 (SELLING).
Distinct insiders buying (code P): 1. Largest buy: Svensen Lars-Christian bought 4,000 sh @ $14.20 ($56,800) on 2026-05-22.

Form 4 filings parsed: 6; transaction rows: 11 (open-market buys 1, sales 2).

| code | rows |
|---|---|
| A | 1 |
| M | 7 |
| P | 1 |
| S | 2 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

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

**Present:** meta.json, form4_summary.md

**Missing:** 8-K filings, 8-K earnings press release exhibit, 10-K Item 7 MD&A (management commentary), 10-K Item 1 - Business (business description), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
