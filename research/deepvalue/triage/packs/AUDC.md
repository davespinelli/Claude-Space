# Triage pack — AUDC · AUDIOCODES LTD

_Generated 2026-09-04 14:02 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** AUDC · **Name:** AUDIOCODES LTD
- **CIK:** 0001086434
- **SIC:** 3661 — Telephone & Telegraph Apparatus
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/AUDC

**Fetcher warnings for this ticker:** 10-K 2026-03-30: heading split missed Item 1 - Business, Item 1A - Risk Factors; no 10-Q in recent filings; no proxy (DEF 14A) in recent filings

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** AUDIOCODES LTD
- **CIK:** 1,086,434 · **SIC:** 3661 (Telephone & Telegraph Apparatus) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 9.99 |
| mktcap | $270.6M |
| ev | $225.3M |
| ev_ebit | 16.1x |
| fcf | $22.9M |
| fcf_yield | 8.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 8.8% |
| net_debt | -$45.3M |
| net_debt_ebit | -3.2x |
| cash | $45.3M |
| ltd | $0.00 |
| equity | $171.3M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $245.6M |
| revenue_prior | $242.2M |
| rev_growth | 1.4% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $14.0M |
| net_income | $9.0M |
| cfo | $29.4M |
| capex | $6.5M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -8.7% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 27,089,259 |
| shares_py | 29,679,755 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 7.8% |
| r6m | 27.6% |
| off_52w_high | -2.3% |
| adv20 | $1.1M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.67 |
| r_ev_ebit | 0.55 |
| r_roic | 0.67 |
| r_rev_growth | 0.39 |
| r_buyback | 0.93 |
| score | 0.69 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2025Q4I |
| shares_period | CY2025Q4I |
| shares_py_period | CY2024Q4I |
| capex_missing | False |
| ltd_missing | True |

**Other screen columns**

| metric | value |
|---|---|
| rank | 65 |

**Screen rationale:** buying back stock -8.7%; debt data missing (net cash unverified); 12-1 momentum 7.8%


## 3. Share count trend

- Shares outstanding: **27,089,259** (CY2025Q4I) vs **29,679,755** prior year (CY2024Q4I)
- Change: **-8.7%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No 8-K filings fetched for this ticker._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 63,000 sh / $602,817 -> net $-602,817 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 17 (open-market buys 0, sales 15).

| code | rows |
|---|---|
| A | 2 |
| S | 15 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release

_Not available: no 8-K with a readable release exhibit was fetched. Current-quarter results are unknown from this pack._

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-30_item7_mdna.md)

_Extraction: no Overview/Results heading found; took the start of Item 7._

ITEM
7. MAJOR SHAREHOLDERS AND RELATED PARTY TRANSACTIONS

A. | MAJOR SHAREHOLDERS

To
our knowledge, (A) we are not directly or indirectly owned or controlled (i) by another corporation or (ii) by any foreign government
and (B) there are no arrangements, the operation of which may at a subsequent date result in a change in control of AudioCodes. The following
table sets forth, as of March 10, 2026, the number of our ordinary shares, which constitute our only outstanding voting securities, beneficially
owned by (i) all shareholders known to us to own more than 5% of our outstanding ordinary shares, and (ii) all of our directors and senior
executive officers as a group.

Identity of Person or | Amount | Percent of
Group | Owned | Class(7)
Shabtai Adlersberg(1) | 4,762,253 | 18.4 | %
Value Base Ltd.(2) | 2,790,432 | 10.8 | %
Leon Bialik(3) | 2,263,019 | 8.7 | %
Copeland Capital Management, LLC(4) | 1,653,376 | 6.4 | %
William Blair Investment Management, LLC(5) | 1,536,371 | 5.9 | %
All directors and senior executive officers as a group (16 persons)(6) | 5,198,932 | 20.1 | %

(1) | The information is derived from a statement on Schedule 13G/A of Shabtai Adlersberg filed with the SEC on February 12, 2026. Includes restricted share units and options to purchase 50,000 ordinary shares exercisable within 60 days of December 31, 2025.

(2) | The information is derived from a statement on Schedule 13G/A of Value Base, Ltd., Victor Shamrich, Ido Nouberger and Value Base Fund Management Ltd. for Value Base Fund General Partner Ltd., acting as the general partner to Value Base Fund Limited Partnership ("Value Base Fund Management") filed with the SEC on February 5, 2026. Pursuant to the Schedule 13G/A, each of Value Base Ltd., Victor Shamrich, Ido Nouberger and Value Base Fund Management has shared voting power over 2,790,432 shares and shared dispositive power over 2,790,432 shares.

(3) | The information is derived from a statement on Schedule 13G/A of Leon Bialik filed with the SEC on February 10, 2026.

(4) | The information is derived from a statement on Schedule 13G of Copeland Capital Management, LLC filed with the SEC on January 26, 2022.

(5) | The information is derived from a statement on Schedule 13G/A of William Blair Investment Management, LLC filed with the SEC on February 12, 2024.

(6) | Includes 61,248 ordinary shares which may be purchased pursuant to options exercisable within 60 days following March 10, 2026, and 55,931 ordinary shares issuable pursuant to restricted share units that vest within 60 days of March 10, 2026.

(7) | This percentage calculation is rounded to the nearest tenth and based on 25,887,104 outstanding ordinary shares as of March 10, 2026 (which does not include treasury shares outstanding as of March 10, 2026).

- 78 -

Mr.
Adlersberg held approximately 17.5% of our ordinary shares as of December 31, 2025, as compared to 15.8% of our ordinary shares as of
December 31, 2024, and 15.0% of our ordinary shares as of December 31, 2023.

Value
Base Ltd. held approximately 10.3% of our ordinary shares as of December 31, 2025, as compared to 8.3% of our ordinary shares as of December
31, 2024. Value Base Ltd. did not file a statement on Schedule 13G (with respect to its ownership in the Company) for the year ended
December 31, 2023.

Mr.
Bialik held approximately 8.4% of our ordinary shares as of December 31, 2025, as compared to 7.7% of our ordinary shares as of December
31, 2024, and 7.6% of our ordinary shares as of December 31, 2023.

Copeland
Capital Management, LLC did not file a statement on Schedule 13G/A (with respect to its ownership in the Company) for the years ended
December 31, 2025, December 31, 2024, and December 31, 2023.

William
Blair Investment Management, LLC held approximately 5.7% of our ordinary shares as of December 31, 2025, as compared to 5.2% of our ordinary
shares as of December 31, 2024, and 5.0% of our ordinary shares as of December 31, 2023. William Blair did not file a statement on Schedule
13G (with respect to its ownership in the Company) for the years ended December 31, 2025 and December 31, 2024.

As
of March 10, 2026, there were approximately three holders of record of our ordinary shares in the United States, although we believe
that the number of beneficial owners of the ordinary shares is significantly greater. The number of record holders in the United States
is not representative of the number of beneficial holders nor is it representative of where such beneficial holders are resident since
many of these ordinary shares were held of record by brokers or other nominees.

The
major shareholders have the same voting rights as the other shareholders.

B. | RELATED PARTY TRANSACTIONS

None.

C. | INTERESTS OF EXPERTS AND COUNSEL

Not
applicable.

## 9. 10-K Item 1 - Business

_Not available: the fetcher did not split out this section for this filing. Describe the business from the MD&A overview above instead, and say so in the note._

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | **MISSING** |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-30_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | **MISSING** |

**Present:** meta.json, form4_summary.md, 10-K_2026-03-30_item7_mdna.md

**Missing:** 8-K filings, 8-K earnings press release exhibit, 10-K Item 1 - Business (business description), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
