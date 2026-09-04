# Triage pack — RDCM · RADCOM LTD

_Generated 2026-09-04 17:11 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** RDCM · **Name:** RADCOM LTD
- **CIK:** 0001016838
- **SIC:** 3577 — Computer Peripheral Equipment, NEC
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/RDCM

**Fetcher warnings for this ticker:** 10-K 2026-03-31: heading split missed Item 1 - Business, Item 1A - Risk Factors; no 10-Q in recent filings

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** RADCOM LTD
- **CIK:** 1,016,838 · **SIC:** 3577 (Computer Peripheral Equipment, NEC) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 10.03 |
| mktcap | $166.4M |
| ev | $135.9M |
| ev_ebit | 16.4x |
| fcf | $14.2M |
| fcf_yield | 8.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 7.8% |
| net_debt | -$30.5M |
| net_debt_ebit | -3.7x |
| cash | $30.5M |
| ltd | $0.00 |
| equity | $114.1M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $71.5M |
| revenue_prior | $61.0M |
| rev_growth | 17.2% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $8.3M |
| net_income | $12.0M |
| cfo | $14.6M |
| capex | $384k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 4.3% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 16,592,725 |
| shares_py | 15,915,616 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -25.5% |
| r6m | -10.9% |
| off_52w_high | -37.9% |
| adv20 | $1.5M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.67 |
| r_ev_ebit | 0.54 |
| r_roic | 0.63 |
| r_rev_growth | 0.80 |
| r_buyback | 0.21 |
| score | 0.57 |

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
| rank | 176 |

**Screen rationale:** revenue +17.2%; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **16,592,725** (CY2025Q4I) vs **15,915,616** prior year (CY2024Q4I)
- Change: **4.3%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No 8-K filings fetched for this ticker._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 6,000 sh / $88,800 -> net $-88,800 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 7; transaction rows: 12 (open-market buys 0, sales 2).

| code | rows |
|---|---|
| A | 10 |
| S | 2 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release

_Not available: no 8-K with a readable release exhibit was fetched. Current-quarter results are unknown from this pack._

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-31_item7_mdna.md)

_Extraction: no Overview/Results heading found; took the start of Item 7._

ITEM
7. MAJOR SHAREHOLDERS AND RELATED PARTY TRANSACTIONS

A. | MAJOR SHAREHOLDERS

The
following table sets forth information with respect to the beneficial ownership of our ordinary shares as of March 23, 2026, by:

● | each person or entity known by us to own beneficially more than 5% of our outstanding ordinary shares;

● | each of our directors and executive officers individually; and

● | all of our executive officers and directors as a group.

The
beneficial ownership of ordinary shares is determined in accordance with the SEC rules and generally includes any ordinary shares over
which a person exercises sole or shared voting or investment power. For purposes of the table below, we deem shares subject to Options
that are currently exercisable or exercisable within 60 days of March 23, 2026, and RSUs, that shall vest within 60 days of March 23,
2026, to be outstanding and to be beneficially owned by the person holding the Options or RSUs for the purposes of computing the percentage
ownership of that person but we do not treat them as outstanding for the purpose of computing the percentage ownership of any other person.
The percentage of shares beneficially owned is based on 16,690,457 ordinary shares outstanding as of March 23, 2026.

The
information presented below is based on information provided to us by the directors, officers, and shareholders or disclosed in public
filings with the SEC. The voting rights of our major shareholders do not differ from the voting rights of other holders of our ordinary
shares.

None
of our executive officers or directors beneficially owns 1% or more of our outstanding ordinary shares.

As
of March 23, 2026, our ordinary shares had a total of 13 holders of record, of which 7 were registered with addresses in the United States.
We believe that the number of beneficial owners of our shares is substantially greater than the number of record holders, because a large
portion of our ordinary shares is held of record in broker "street name".

Name | Number of Ordinary Shares beneficially owned (1) | Percentage of Outstanding Ordinary Shares beneficially owned (2)
Principal Shareholders
Lynrock Lake LP | 3,166,666 | (3) | 19.0 | %
Michael Zisapel and Klil Zisapel | 2,294,738 | (4) | 13.7 | %
Barclays PLC | 1,114,430 | (5) | 6.7 | %
AWM Investment Company, Inc. | 991,261 | (6) | 5.9 | %
Value Base Ltd. | 865,009 | (7) | 5.2 | %
Directors and Officers
Rami Schwartz | * | *
Rachel (Heli) Bennun | * | *
Andre Fuetsch | * | *
Oren Most | * | *
Yaron Ravkaie | * | *
David (Dudi) Ripstein | * | *
Sami Totah | * | *
Benjamin (Benny) Eppstein | * | *
Hod Cohen | * | *
Hilik Itman | * | *
Rami Amit | * | *
All directors and executive officers as a group (11 persons) | 298,333 | (8) | 1.8 | %

* | Less than 1%

(1) | Except as otherwise noted and subject to applicable community property laws, each person named in the table has sole voting and investment power with respect to all ordinary shares listed as owned by such person. Shares beneficially owned include shares that may be acquired pursuant to options to purchase ordinary shares that are exercisable within 60 days of March 23, 2026.

(2) | The percentage of outstanding ordinary shares is based on 16,690,457 ordinary shares outstanding as of March 23, 2026. In determining the percentage owned by each person, ordinary shares for each person includes ordinary shares that may be acquired by such person pursuant to options to purchase ordinary shares that are exercisable within 60 days of March 23, 2026. The number of outstanding ordinary shares does not include 5,189 ordinary shares held by RADCOM US, a wholly owned subsidiary and 30,843 ordinary shares that were repurchased by us.
(3) | Based on a Schedule 13D filed with the SEC on February 24, 2026. Includes 3,166,666 ordinary shares held by Lynrock Lake Master Fund LP, or Lynrock Lake Master. Lynrock Lake LP, or Investment Manager, is the investment manager of Lynrock Lake Master. Pursuant to an investment management agreement, the Investment Manager has been delegated full voting and investment power over securities of the Company held by Lynrock Lake Master. Cynthia Paul, the Chief Investment Officer of the Investment Manager and So l e Member of Lynrock Lake Partners LLC, the general partner of the Investment Manager, may be deemed to exercise voting and investment power over securities of the Company held by Lynrock Lake Master. The address of each of Cynthia Paul, Lynrock Lake Partners LLC, and Lynrock Lake LP is 2 International Drive, Suite 130 Rye Brook, NY 10573.
(4) | Based on a Schedule 13D/A filed with the SEC on February 24, 2026, Mr. Michael Zisapel and Ms. Klil Zisapel beneficially own, in aggregate, 2,294,738 ordinary shares. Ms. Klil Zisapel beneficially owns 1,147,369 ordinary shares, consisting of (i) 874,047 ordinary shares held directly by Ms. Klil Zisapel and (ii) 271,074 ordinary shares that are held indirectly by Ms. Klil Zisapel through her 50% ownership in each of Lomsha Ltd., an Israeli company, and Michael & Klil Holdings (93) Ltd., an Israeli company and (iii) Options to acquire 2,249 ordinary shares exercisable within 60 days. Mr. Michael Zisapel beneficially owns 1,147,369 ordinary shares, consisting of (i) 874,047 ordinary shares held directly by him, (ii) 271,074 ordinary shares held indirectly through his 50% ownership in each of Lomsha Ltd. and Michael & Klil Holdings (93) Ltd., and (iii) Options to acquire 2,248 ordinary shares exercisable within 60 days. The address of Mr. Zisapel and Ms. Z i sapel is 24 Raoul Wallenberg Street, Building C, Tel-Aviv 69719, Israel.
(5) | Based on a Schedule 13G/A filed on February 11, 2026, Barclays PLC beneficially owns an aggregate amount of 1,114,430 ordinary shares; Barclays PLC reported sole voting power and sole dispositive power with respect to 1,111,314 ordinary shares, and shared voting power and shared dispositive power with respect to 3,116 ordinary shares. The securities being reported on by Barclays PLC, as a parent holding company, are owned, or may be deemed to be beneficially owned, by Barclays Bank PLC. Barclays Bank PLC is a non-US banking institution registered with the Financial Conduct Authority authorised by the Prudential Regulation Authority and regulated by the Financial Conduct Authority and the Prudential Regulation Authority in the United Kingdom. Barclays Bank PLC is a wholly-owned subsidiary of Barclays PLC. Barclays Capital Inc., is a Connecticut business entity. The address of the principal office of Barclays PLC and Barclays Bank PLC is 1 Churchill Place, London, E14 5HP, England. The address of the principal office of Barclays Capital Inc. is 745 Seventh Ave, New York, NY 10019.
(6) | Based on a Schedule 13G filed with the SEC on February 14, 2025 by AWM Investment Company, Inc., or AWM, reporting that AWM is the investment adviser to Special Situations Fund III QP, L.P., or SSFQP, Special Situations Cayman Fund, L.P., or Cayman, Special Situations Technology Fund, L.P., or TECH and Special Situations Technology Fund II, L.P., or TECH II and referred to together with SSFQP, Cayman, and TECH as the Funds. As the investment adviser to the Funds, AWM holds sole voting and investment power over 380,185 ordinary shares held by SSFQP, 106,530 ordinary shares held by Cayman, 84,821 ordinary shares held by TECH and 419,725 ordinary shares held by TECH II. David M. Greenhouse and Adam C. Stettner are members of SSCayman, L.L.C., a Delaware limited liability company, or SSCAY, the general partner of Cayman. David M. Greenhouse and Adam C. Stettner are members of MGP Advisers Limited Partnership, a Delaware limited partnership, the general partner of SSFQP and SST Advisers, L.L.C., a Delaware limite d liability company, the general partner of TECH and TECH II. David M. Greenhouse and Adam C. Stettner are also controlling principals of AWM. The business address AWM Investment Company, Inc.is c/o Special Situations Funds, 527 Madison Avenue, Suite 2600, New York, NY 10022.

(7) | Based on a Schedule 13D filed with the SEC on February 17, 2026. Includes (i) 400,563 Ordinary Shares owned directly by Value Base Ltd., an Israeli company which is controlled by Messrs. Victor Shamrich and Ido Nouberger and which wholly owns Value Base Hedge Fund Ltd., an Israeli company, and is the general partner of Harmony Base L.P., and (ii) 464,446 ordinary shares owned directly by Harmony Base L.P., an Israeli limited partnership. The address of each of Value Base Ltd. and Harmony Base L.P. is 23 Yehuda Halevi St., Tel-Aviv 6513601, Israel.

(8) | Each of the directors and executive officers not separately identified in the above table beneficially owns less than 1% of our outstanding ordinary shares, including options that are currently exercisable or exercisable within 60 days of March 23, 2026, and RSUs that vest within 60 days of March 23, 2026 held by each such party, and have, therefore, not been separately disclosed. The number of shares is comprised of 261,007 ordinary shares and 26,599 Ordinary Shares issuable upon the settlement of RSUs and 10,727 Ordinary Shares issuable upon the exercise of Options that are currently exercisable or exercisable within 60 days of March 23, 2026

Significant Changes
in Percentage Ownership by Major Shareholders

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business

_Not available: the fetcher did not split out this section for this filing. Describe the business from the MD&A overview above instead, and say so in the note._

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | **MISSING** |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-31_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | **MISSING** |

**Present:** meta.json, form4_summary.md, 10-K_2026-03-31_item7_mdna.md

**Missing:** 8-K filings, 8-K earnings press release exhibit, 10-K Item 1 - Business (business description), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
