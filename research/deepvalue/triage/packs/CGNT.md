# Triage pack — CGNT · Cognyte Software Ltd.

_Generated 2026-09-04 17:11 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** CGNT · **Name:** Cognyte Software Ltd.
- **CIK:** 0001824814
- **SIC:** 7372 — Services-Prepackaged Software
- **Fiscal year end (MM-DD):** 01-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/CGNT

**Fetcher warnings for this ticker:** 10-K 2026-03-25: heading split missed Item 1 - Business, Item 1A - Risk Factors; no 10-Q in recent filings; no proxy (DEF 14A) in recent filings; no Form 4 filings in the last 12 months

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Cognyte Software Ltd.
- **CIK:** 1,824,814 · **SIC:** 7372 (Services-Prepackaged Software) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 8.48 |
| mktcap | $619.7M |
| ev | $502.8M |
| ev_ebit | 37.9x |
| fcf | $29.9M |
| fcf_yield | 4.8% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 11.7% |
| net_debt | -$116.9M |
| net_debt_ebit | -8.8x |
| cash | $116.9M |
| ltd | $0.00 |
| equity | $206.5M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $400.0M |
| revenue_prior | $350.6M |
| rev_growth | 14.1% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $13.3M |
| net_income | -$638k |
| cfo | $40.3M |
| capex | $10.4M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 1.4% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 73,078,376 |
| shares_py | 72,057,202 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 5.5% |
| r6m | 1.2% |
| off_52w_high | -30.7% |
| adv20 | $4.7M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.48 |
| r_ev_ebit | 0.20 |
| r_roic | 0.75 |
| r_rev_growth | 0.75 |
| r_buyback | 0.40 |
| score | 0.56 |

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
| rank | 179 |

**Screen rationale:** debt data missing (net cash unverified); 12-1 momentum 5.5%


## 3. Share count trend

- Shares outstanding: **73,078,376** (CY2025Q4I) vs **72,057,202** prior year (CY2024Q4I)
- Change: **1.4%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No 8-K filings fetched for this ticker._

## 6. Insider activity (Form 4, trailing 12 months)

No Form 4 activity in 12 months (no observation; not a signal).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 0; transaction rows: 0 (open-market buys 0, sales 0).

| code | rows |
|---|---|

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release

_Not available: no 8-K with a readable release exhibit was fetched. Current-quarter results are unknown from this pack._

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-25_item7_mdna.md)

_Extraction: no Overview/Results heading found; took the start of Item 7._

ITEM 7. MAJOR SHAREHOLDERS AND RELATED PARTY TRANSACTIONS

7.A. MAJOR SHAREHOLDERS

The following table sets forth information with respect to the beneficial ownership of our shares as of March 18, 2026 by:

• each person or entity known by us to own beneficially more than 5% of our outstanding shares;

• each of our directors and executive officers individually; and

• all of our executive officers and directors as a group.

The beneficial ownership of ordinary shares is determined in accordance with the SEC rules and generally includes any ordinary shares over which a person exercises sole or shared voting or investment power. For the purposes of the table below, we deem restricted shares units scheduled to vest within 60 days of March 18, 2026, to be outstanding and to be beneficially owned by the person holding restricted shares units for the purposes of computing the percentage ownership of that person, but we do not treat them as outstanding for the purpose of computing the percentage ownership of any other person. The percentage of shares beneficially owned is based on 72,675,955 ordinary shares outstanding as of March 18, 2026.

All of our shareholders, including the shareholders listed below, have the same voting rights attached to their ordinary shares. Unless otherwise noted below, each shareholder's address is 33 Maskit, Herzliya Pituach, 4673333, Israel.

COGNYTE SOFTWARE LTD.

Shares Beneficially Owned
Name of beneficial owner | Number | %
Directors and executive officers
Elad Sharon | 1,738,397 | 2.39%
Earl Shanks | 272,101 | 0.37%
Dafna Sharir | 105,476 | 0.15%
Avi Cohen | 76,775 | 0.11%
Ron Shvili | 51,248 | *
Matthew O'Neill | 19,048 | *
Nurit Benjamini | 19,048 | *
David Abadi | 844,118 | 1.16%
Gil Cohen | 469,371 | 0.65%
Sharon Chouli | 548,364 | 0.75%
Efi Nuri | 481,319 | 0.66%
All directors and executive officers as a group (11 persons) | 4,625,265 | 6.36%
Major Shareholders | *
Topline Capital Management, LLC (1) | 7,238,153 | 9.96%
ValueBase Ltd. and affiliates (2) | 6,852,674 | 9.43%
American Capital Management, Inc. (3) | 6,665,590 | 9.17%
Edenbrook Capital, LLC (4) | 6,075,551 | 8.36%
Neuberger Berman, LLC(5) | 5,038,357 | 6.93%

* Less than 0.1%

(1) As reported in a Schedule 13G/A filed with the SEC on February 13, 2026 by Topline Capital Management, LLC ("TCM"), Collin McBirney and Topline Capital Partners, LP ("TCP"). Each of these entities have shared voting and dispositive power over 7,238,153 Cognyte ordinary shares. The address of each of these reporting persons is 544 Euclid Street, Santa Monica, CA 90402.

(2 ) Based on information available to the Company and as reported in a Schedule 13D filed on September 16, 2024, the Ordinary Shares beneficially owned by this shareholder consist of (i) 1,114,585 Ordinary Shares held directly by Harmony LP, (ii) 3,123,122 Ordinary Shares held directly by VBF LP, and (iii) 1,469,213 Ordinary Shares owned directly by Value Base. As the sole owner of Harmony GP and the controlling shareholder of VBF GP, Value Base may be deemed the indirect beneficial owner of the Ordinary Shares beneficially owned by Harmony LP and VBF LP. In total, Value Base is deemed to beneficially own 5,706,920 Ordinary Shares, representing approximately 7.94% of the number of Ordinary Shares outstanding.

Mr. Victor Shamrich, who directly owns 671,354 Ordinary Shares, and Mr. Ido Nouberger, who directly owns 472,400 Ordinary Shares, together control Value Base. They may be deemed the indirect beneficial owners of the Ordinary Shares beneficially owned by Value Base. In total, Mr. Shamrich is deemed to beneficially own 6,378,274 Ordinary Shares, representing approximately 8.87% of the number of Ordinary Shares outstanding, and Mr. Nouberger is deemed to beneficially own 6,179,320 Ordinary Shares, representing approximately 8.59% of the number of Ordinary Shares outstanding.

Mr. Tal Yaacobi owns 2,000 Ordinary Shares through a wholly-owned company, representing approximately 0.003% of the number of Ordinary Shares outstanding.

Because Mr. Shamrich, Mr. Nouberger, Mr. Yaacobi, Harmony GP, VBF GP, and Value Base may be deemed to constitute a "group" for purposes of Section 13(d) of the Exchange Act, each may share the power to vote, or direct the voting of, and share the power to dispose of, or direct the disposition of, the 6,852,674 Ordinary Shares held in the aggregate by the Reporting Persons.

COGNYTE SOFTWARE LTD.

(3) As reported on Schedule 13G/A filed with the SEC on May 15, 2025 by American Capital Management, Inc. ("ACMI"). ACMI has sole voting power over 3,070,681 Cognyte ordinary shares and sole dispositive power over 6,665,590 Cognyte ordinary shares. The address of ACMI is 575 Lexington Avenue, 30th Floor, New York, NY 10022.

(4) According to a Schedule 13D/A filed on October 13, 2022 by Edenbrook Capital, LLC ("Edenbrook Capital") and Jonathan Brolin, each had shared voting and dispositive power over 6,538,998 Cognyte ordinary shares. The number of shares set forth in the table is based on 6,075,551 shares reported in a Form 13F-HR filed with the SEC on February 13, 2024 by Edenbrook Capital and Jonathan Brolin. The address of each of the reporting persons is 116 Radio Circle, Mt. Kisco, NY 10549.

(5) As reported on Schedule 13G/A filed with the SEC on February 12, 2024 by Neuberger Berman Group, LLC ("NB Group") and Neuberger Berman Investment Advisers LLC ("NBIA"). NB Group has shared voting power over 4.098,684 shares and shared dispositive power over 5,038,357 shares. NBIA has shared voting power over 4,005,531 and shared dispositive power over 4,880,459 shares. Neuberger Berman Trust Co N.A., Neuberger Berman Trust Co of Delaware N.A., Neuberger Berman Asia Ltd., Neuberger Berman Canada ULC, and NBIA and certain affiliated persons may be deemed to beneficially these Cognyte ordinary shares in their various fiduciary capacities. NB Group, through its subsidiaries Neuberger Berman Investment Advisers Holdings LLC and Neuberger Trust Holdings LLC controls Neuberger Berman Trust Co N.A., Neuberger Berman Asia Ltd., Neuberger Berman Canada ULC, Neuberger Berman Trust Co of Delaware N.A. and NBIA and certain affiliated persons. Each of NB Group, NBIA, Neuberger Trust Holdings LLC, Neuberger Berman Trust Co N.A., Neuberger Berman Asia Ltd., Neuberger Berman Canada ULC, Neuberger Berman Trust Co of Delaware N.A. and Neuberger Berman Investment Advisers LLC and certain affiliated persons disclaim beneficial ownership of these Cognyte ordinary shares. The address of each of these reporting persons is 1290 Avenue of the Americas, New York, NY 10104.

Registered Holders

Based on a review of the information provided to us by our transfer agent, as of January 31, 2026, there were 1,462 United States registered holders of our shares, one of which (Cede & Co., the nominee of the Depository Trust Company) held approximately 96.3% of our outstanding ordinary shares.

7.B. RELATED PARTY TRANSACTIONS

The following is a description of material transactions, or series of related material transactions, since February 1, 2022, that are required to be disclosed under Item 7.B of Form 20-F. For information relating to our policies on approval of related party transactions, since "Item 6.C. Board Practices—Approval of Related Party Transactions under Israeli Law."

The summaries of the material transactions described below set forth the terms of the agreements that we believe are material. These summaries are qualified in their entireties by reference to the full text of the applicable agreements, which are incorporated by reference into this Annual Report.

Separation and Distribution and Tax Matter Agreements with Verint

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
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-25_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | **MISSING** |

**Present:** meta.json, form4_summary.md, 10-K_2026-03-25_item7_mdna.md

**Missing:** 8-K filings, 8-K earnings press release exhibit, 10-K Item 1 - Business (business description), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
