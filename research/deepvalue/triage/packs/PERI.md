# Triage pack — PERI · Perion Network Ltd.

_Generated 2026-09-04 21:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** PERI · **Name:** Perion Network Ltd.
- **CIK:** 0001338940
- **SIC:** 7371 — Services-Computer Programming Services
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/PERI

**Fetcher warnings for this ticker:** 10-K 2026-03-16: heading split missed Item 1 - Business, Item 1A - Risk Factors; no 10-Q in recent filings; no proxy (DEF 14A) in recent filings

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Perion Network Ltd.
- **CIK:** 1,338,940 · **SIC:** 7371 (Services-Computer Programming Services) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 9.23 |
| mktcap | $360.2M |
| ev | $270.2M |
| ev_ebit | n/a |
| fcf | $38.1M |
| fcf_yield | 10.6% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -2.0% |
| net_debt | -$90.0M |
| net_debt_ebit | n/a |
| cash | $90.0M |
| ltd | $0.00 |
| equity | $676.0M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $439.9M |
| revenue_prior | $498.3M |
| rev_growth | -11.7% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$14.9M |
| net_income | -$7.9M |
| cfo | $41.9M |
| capex | $3.8M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -12.9% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 39,024,964 |
| shares_py | 44,825,053 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 3.7% |
| r6m | 2.3% |
| off_52w_high | -16.5% |
| adv20 | $4.0M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.73 |
| r_ev_ebit | 0.00 |
| r_roic | 0.25 |
| r_rev_growth | 0.09 |
| r_buyback | 0.96 |
| score | 0.46 |

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
| rank | 285 |

**Screen rationale:** buying back stock -12.9%; debt data missing (net cash unverified); 12-1 momentum 3.7%


## 3. Share count trend

- Shares outstanding: **39,024,964** (CY2025Q4I) vs **44,825,053** prior year (CY2024Q4I)
- Change: **-12.9%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No 8-K filings fetched for this ticker._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 16,641 sh / $166,079 -> net $-166,079 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 7; transaction rows: 7 (open-market buys 0, sales 7).

| code | rows |
|---|---|
| S | 7 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release

_Not available: no 8-K with a readable release exhibit was fetched. Current-quarter results are unknown from this pack._

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-16_item7_mdna.md)

_Extraction: no Overview/Results heading found; took the start of Item 7._

ITEM 7. MAJOR
SHAREHOLDERS AND RELATED PARTY TRANSACTIONS

A. MAJOR
SHAREHOLDERS

The following table sets forth information with respect to
the beneficial ownership of our shares as of March 5, 2026, by each person or entity known by us to beneficially own 5% or more of our
outstanding ordinary shares.

Beneficial ownership of shares is determined in accordance with
the Exchange Act and the rules promulgated thereunder, and generally includes any shares over which a person exercises sole or shared
voting or investment power. Ordinary shares that are issuable pursuant to an outstanding right within 60 days of a specified date are
deemed to be outstanding and beneficially owned by the person holding the right for the purpose of computing the percentage ownership
of that person, but are not treated as outstanding for the purpose of computing the percentage ownership of any other person.

For the purpose of calculating the percentage of shares beneficially
owned by any shareholder, this table lists the applicable percentage ownership based on 39,330,319 ordinary shares issued and outstanding
as of March 5, 2026 (such amount excludes 115,339 ordinary shares held by the Company).

Except as indicated in the footnotes to this table, to our knowledge,
each shareholder in the table has voting and investment power for the shares shown as beneficially owned by such shareholder, except to
the extent the power is shared by spouses under community property law. Our major shareholders do not have different voting rights than
our other shareholders. The information in the table below with respect to the beneficial ownership of shareholders is based on the public
filings of such shareholders with the SEC through March 5, 2026, and information provided to us by certain shareholders.

Name of Beneficial Owner | Shares Beneficially Owned
Number | Percentage
Private Capital Management, LLC (1) | 4,215,406 | 10.72 | %
Harel Insurance Investments & Financial Services Ltd. (2) | 3,637,418 | 9.25 | %
Migdal Insurance & Financial Holdings Ltd. (3) | 2,328,988 | 5.92 | %

(1) Based solely upon, and qualified in its entirety with reference
to Amendment No. 1 to Schedule 13G filed with the SEC on February 6, 2026, regarding holdings as of November 30, 2025, by Private Capital
Management, LLC ("PCM"). Of the 4,215,406 ordinary shares beneficially owned by PCM: (i) 1,717,856 ordinary shares are beneficially
held for PCM's own account; and (ii) 2,497,550 ordinary shares, are deemed to be under shared dispositive power by virtue of
PCM clients that have delegated proxy voting authority to PCM. The address of PCM is 8889 Pelican Bay Boulevard, Suite 500, Naples, FL
34018.

(2) The information is based upon the shareholder notification
provided to the Company by Harel Insurance Investments & Financial Services Ltd. ("Harel") on January 4, 2026, regarding
holdings as of December 31, 2025. Prior to that Harel filed an Amendment No. 4 to Schedule 13G with the SEC on August 5, 2025, which set
forth that its holdings in the Company were 3,961,645 ordinary shares The reported ordinary shares are held for members of the public
through, among others, provident funds and/or mutual funds and/or pension funds and/or insurance policies and/or exchange traded funds,
which are managed by subsidiaries of Harel, each of which operates under independent management and makes independent voting and investment
decisions. The address of Harel is Harel House; 3 Aba Hillel Street; Ramat Gan 52118, Israel.

(3) Based solely upon, and qualified in its entirety with reference
to Schedule 13G filed with the SEC on November 13, 2025, regarding holdings as of September 30, 2025, by Migdal Insurance & Financial
Holdings Ltd. ("Migdal"). According to such Schedule 13G, Migdal and certain of its direct or indirect, majority or wholly-owned
subsidiaries reported beneficial ownership of 2,328,988 ordinary shares. The reported ordinary shares are held for members of the public
through, among others, mutual funds, provident funds, pension funds and insurance policies managed by Migdal and its subsidiaries, each
of which operates under independent management and makes independent voting and investment decisions. The address of Migdal is 4 Efal
Street; P.O. Box 3063, Petach Tikva 49512, Israel.

To our knowledge, the significant changes in the percentage of
ownership held by our major shareholders during the past three years preceding the date of this annual report on Form 20-F have been:
(i) the increase in the percentage of ownership by PCM, above 5% during 2024, and a further increase in the percentage of ownership by
PCM and its client accounts, above 10% during 2025; (ii) the increase in the percentage of ownership by Harel Insurance Investments &
Financial Services Ltd. held for members of the public through various direct or indirect, majority or wholly-owned subsidiaries, above
5% during 2023, a further increase above 10% in 2024, and a decrease below 10% in 2025; (iii) the increase in the percentage of ownership
by Migdal Insurance & Financial Holdings Ltd. and certain of its direct or indirect, majority or wholly-owned subsidiaries, above
5% during 2025; and (iv) the decrease in the percentage of ownership by Phoenix Holdings Ltd. and its various direct or indirect, majority
or wholly-owned subsidiaries, below 5% during 2023, which later increased above 5% during 2023 and 2024, and a further decrease below
5% during 2025; (v) the increase in the percentage of ownership by Clal Insurance Enterprises Holdings Ltd. and its third-party client
accounts and various direct or indirect, majority or wholly-owned subsidiaries, above 5% during 2023, and a subsequent decrease below
5% during 2024; and (vi) the increase in the percentage of ownership by Value Base Ltd. and its third-party client accounts and various
direct or indirect, majority or wholly-owned subsidiaries, above 5% during 2025, followed by a subsequent decrease below 5% in that same
year.

To our knowledge, as of March 5, 2026, we had five (5) shareholders
of record (excluding the Depository Trust Company), all of whom were registered with addresses in the United States. These U.S. holders
were, as of such date, the holders of record of approximately 0.02% of our outstanding shares. The number of record holders in the United
States is not representative of the number of beneficial holders, nor is it representative of where such beneficial holders are resident,
since many of these ordinary shares were held of record by brokers or other nominees.

B. RELATED
PARTY TRANSACTIONS

It is our policy that transactions with office holders or transactions
in which an office holder has a personal interest will be on terms that, on the whole, are no less favorable to us than could be obtained
from independent parties.

See Exhibit 2.1 to this annual report on Form 20-F, which is incorporated
by reference into this annual report on Form 20-F, for a discussion of the requirements of Israeli law regarding special approvals for
transactions involving directors, officers or controlling shareholders.

The following is a description of some of the transactions with
related parties to which we are party and which were in effect within the past three fiscal years. The descriptions provided below are
summaries of the terms of such agreements and do not purport to be complete and are qualified in their entirety by the complete agreements.

Indemnification Agreements

Our articles of association permit us to exculpate, indemnify and
insure our directors and officeholders to the fullest extent permitted by the Companies Law. We have obtained directors' and officers'
insurance for each of our officers and directors and have entered into indemnification agreements with all of our current officers and
directors.

We have entered into indemnification and exculpation agreements
with each of our current office holders and directors exculpating them to the fullest extent permitted by the law and our articles of
association and undertaking to indemnify them to the fullest extent permitted by the law and our articles of association, including with
respect to liabilities resulting from this annual report, to the extent such liabilities are not covered by insurance. See also Item 10.B.
"Related Party Transactions—Indemnification Agreements."

Employment and Consulting Agreements

We have or have had employment, consulting or related agreements
with each member of our senior management. For more information on employment and consulting agreements see Item 6.B. "Compensation."

C. INTERESTS
OF EXPERTS AND COUNSEL

Not applicable.

## 9. 10-K Item 1 - Business

_Not available: the fetcher did not split out this section for this filing. Describe the business from the MD&A overview above instead, and say so in the note._

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | **MISSING** |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-16_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | **MISSING** |

**Present:** meta.json, form4_summary.md, 10-K_2026-03-16_item7_mdna.md

**Missing:** 8-K filings, 8-K earnings press release exhibit, 10-K Item 1 - Business (business description), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
