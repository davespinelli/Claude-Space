# Triage pack — TK · TEEKAY CORP LTD

_Generated 2026-09-04 17:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** TK · **Name:** TEEKAY CORP LTD
- **CIK:** 0000911971
- **SIC:** 4412 — Deep Sea Foreign Transportation of  Freight
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/TK

**Fetcher warnings for this ticker:** 10-K 2026-03-13: heading split missed Item 1 - Business, Item 1A - Risk Factors; no 10-Q in recent filings; no proxy (DEF 14A) in recent filings

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** TEEKAY CORP LTD
- **CIK:** 911,971 · **SIC:** 4412 (Deep Sea Foreign Transportation of  Freight) · **Exchange:** NYSE

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 13.47 |
| mktcap | $1.2B |
| ev | $218.5M |
| ev_ebit | 0.7x |
| fcf | $111.5M |
| fcf_yield | 9.6% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | -$940.7M |
| net_debt_ebit | -3.1x |
| cash | $940.7M |
| ltd | $0.00 |
| equity | n/a |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $949.5M |
| revenue_prior | $1.2B |
| rev_growth | -22.2% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $302.8M |
| net_income | $98.1M |
| cfo | $301.8M |
| capex | $190.3M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 2.4% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 86,056,804 |
| shares_py | 84,059,952 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 41.4% |
| r6m | 18.5% |
| off_52w_high | 0.0% |
| adv20 | $6.9M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.70 |
| r_ev_ebit | 1.00 |
| r_roic | 0.50 |
| r_rev_growth | 0.03 |
| r_buyback | 0.30 |
| score | 0.56 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | n/a |
| shares_period | CY2025Q4I |
| shares_py_period | CY2024Q4I |
| capex_missing | False |
| ltd_missing | True |

**Other screen columns**

| metric | value |
|---|---|
| rank | 188 |

**Screen rationale:** cheap at 0.7x EV/EBIT; debt data missing (net cash unverified); 12-1 momentum 41.4%


## 3. Share count trend

- Shares outstanding: **86,056,804** (CY2025Q4I) vs **84,059,952** prior year (CY2024Q4I)
- Change: **2.4%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No 8-K filings fetched for this ticker._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 454,206 sh / $5,542,861 -> net $-5,542,861 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 26 (open-market buys 0, sales 12).

| code | rows |
|---|---|
| A | 4 |
| M | 10 |
| S | 12 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release

_Not available: no 8-K with a readable release exhibit was fetched. Current-quarter results are unknown from this pack._

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-13_item7_mdna.md)

_Extraction: no Overview/Results heading found; took the start of Item 7._

Item 7. Major Shareholders and Certain Relationships and Related Party Transactions

Major Shareholders

The following table sets forth information regarding beneficial ownership, as of March 1, 2026, of Teekay's common shares by each entity or group we know to beneficially own more than 5% of the common shares. Information for certain holders is based on their latest filings with the SEC. The number of shares beneficially owned by each entity or group is determined under SEC rules and the information is not necessarily indicative of beneficial ownership for any other purpose. Under SEC rules, a person or entity beneficially owns any shares as to which the person or entity has or shares voting or investment power. In addition, a person or entity beneficially owns any shares that the person or entity has the right to acquire as of April 30, 2026 (60 days after March 1, 2026) through the exercise of any stock option or other right. Unless otherwise indicated, each entity or group listed below has sole voting and investment power with respect to the shares set forth in the following table.

Identity of Person or Group | Shares Owned | Percent of Class (3)
Resolute Investments, Ltd. (1) | 31,936,012 | 36.8%
Dimensional Fund Advisors LP (2) | 5,326,069 | 6.1%

(1) This information is based on the Schedule 13D/A (Amendment No. 14) filed by Resolute and Path with the SEC on February 20, 2025, which reports shared voting and shared dispositive power with respect to all shares. The ultimate controlling person of Resolute is Path, which is the trust protector for the trust that indirectly owns all of Resolute's outstanding equity. Resolute's beneficial ownership was 36.8% on March 1, 2026, and 38.0% on December 31, 2024. For additional information on the relationships between Resolute and certain of our directors, please see the section titled " – Relationships with Our Major Shareholder" below.

(2) This information is based on the Form 13F filed with the SEC by Dimensional Fund Advisors LP on February 13, 2026, which reports that Dimensional Fund Advisors has sole investment discretion with respect to 5,131,834 shares, shared investment discretion with respect to 194,235 shares, sole voting power with respect to 5,046,094, shared voting power with respect to 194,235 shares and no voting power with respect to 85,740 shares.

(3) Based on a total of 86,778,532 outstanding common shares as of March 1, 2026.

Our major shareholders have the same voting rights as our other shareholders. No corporation or foreign government or other natural or legal person owns more than 50% of our outstanding common shares. We are not aware of any arrangements, the operation of which may at a subsequent date result in a change in control of Teekay.

Teekay and certain of its subsidiaries have relationships or are parties to transactions with other Teekay subsidiaries, including Teekay's publicly-traded subsidiary, Teekay Tankers. Certain of these relationships and transactions are described below.

Relationships with Our Major Shareholder

As of March 1, 2026, Resolute owned approximately 36.8% of our outstanding common shares. The ultimate controlling person of Resolute is Path, which is the trust protector for The Kattegat Trust, which owns Kattegat Limited, which owns all of Resolute's outstanding equity. One of our directors, Rudolph Krediet, is a partner at Anholt Services (USA) Inc., a wholly-owned subsidiary of Kattegat Limited. Another director, Poul Karlshoej, is a consultant at Anholt Services (USA) Inc. and serves on its Investment Committee, and is also a shareholder and director of Path. Director Peter Antturi serves as an executive officer and director of Resolute and other Kattegat Limited subsidiaries and affiliates.

Our Directors and Executive Officers

Our directors, other than Brody Speers, also serve as directors of Teekay Tankers, including Ms. Locke Simon who serves as Chair of Teekay and Teekay Tankers. Our executive officers Kenneth Hvid and Brody Speers also serve as the President and Chief Executive Officer and Chief Financial Officer, respectively, of Teekay Tankers.

The Chief Executive Officer and Chief Financial Officer of Teekay Tankers are employed by a Teekay subsidiary that qualified as a related party to Teekay Tankers until Teekay Tankers acquired the subsidiary on December 31, 2024. Prior to the acquisition, the executive officers' compensation (other than any awards under the long-term incentive plan of Teekay Tankers) was paid by Teekay through its subsidiary. Pursuant to agreements with Teekay, Teekay Tankers agreed to reimburse Teekay or its applicable subsidiaries for time spent by the executive officers in providing services to Teekay Tankers and its subsidiaries. For 2024 and 2023, these reimbursement obligations totaled approximately $4.1 million and $2.1 million, respectively.

Relationship and Management Agreements with Teekay Tankers

Please see "Item 4C – Information on the Company – Organizational Structure" for information about our ownership interests in Teekay Tankers.

Teekay Tankers' organizational documents provide that Teekay may pursue business opportunities attractive to both parties and of which either party becomes aware. These business opportunities may include, among other things, opportunities to charter-out, charter-in or acquire oil tankers or to acquire tanker businesses.

Management Agreement. In connection with its initial public offering, Teekay Tankers entered into a comprehensive management agreement (the Management Agreement ) with a Teekay subsidiary as manager. The current manager under the Management Agreement is Teekay Services Limited (or the Manager ), which remained a Teekay subsidiary until its acquisition by Teekay Tankers on December 31, 2024.

Pursuant to the Management Agreement, the Manager agreed to provide to Teekay Tankers technical, administrative and strategic services. During 2024 and 2023, Teekay Tankers incurred fees of $37.0 million and $35.9 million, respectively, for all of these services.

Following Teekay Tankers' acquisition of certain subsidiaries from Teekay (including the Manager) effective December 31, 2024, Teekay Tankers no longer receives services from Teekay under the Management Agreement.

Management Agreements with Teekay Tankers . Effective December 31, 2024, Teekay entered into management services agreements with Teekay Tankers and its subsidiaries pursuant to which Teekay Tankers and its subsidiaries provide services to Teekay for a management fee. Effective December 31, 2024, Teekay's executive officers are employed by one of Teekay Tankers' subsidiaries and they provide services to Teekay pursuant to these agreements, with the compensation of those executive officers (other than any awards under Teekay's long-term incentive plan) being set and paid by Teekay Tankers' subsidiary. Teekay reimburses Teekay Tankers for time spent by the executive officers on Teekay Parent's management matters. This reimbursement forms part of the management fee Teekay pays to Teekay Tankers pursuant to the management services agreements.

In connection with Teekay Tankers' acquisition of Tanker Investments Ltd. (or TIL ) in November 2017, the Manager waived certain management fees payable under the existing TIL management agreement, but did not waive the transaction fee that is payable in the event of any sale of vessels owned by TIL subsidiaries as of the date of the TIL merger, which fee is equal to 1.0% of the aggregate consideration payable to Teekay Tankers, TIL or its subsidiaries pursuant to a sale contract. Pursuant to the transfer of the Manager to Teekay Tankers effective December 31, 2024, any transaction fees payable under this arrangement will be paid to Teekay or its affiliates.

## 9. 10-K Item 1 - Business

_Not available: the fetcher did not split out this section for this filing. Describe the business from the MD&A overview above instead, and say so in the note._

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | **MISSING** |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-13_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | **MISSING** |

**Present:** meta.json, form4_summary.md, 10-K_2026-03-13_item7_mdna.md

**Missing:** 8-K filings, 8-K earnings press release exhibit, 10-K Item 1 - Business (business description), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
