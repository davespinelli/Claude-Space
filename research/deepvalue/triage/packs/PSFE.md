# Triage pack — PSFE · Paysafe Ltd

_Generated 2026-09-04 16:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** PSFE · **Name:** Paysafe Ltd
- **CIK:** 0001833835
- **SIC:** 7389 — Services-Business Services, NEC
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/PSFE

**Fetcher warnings for this ticker:** 10-K 2026-03-03: heading split missed Item 1 - Business, Item 1A - Risk Factors; no 10-Q in recent filings; no proxy (DEF 14A) in recent filings

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Paysafe Ltd
- **CIK:** 1,833,835 · **SIC:** 7389 (Services-Business Services, NEC) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 6.79 |
| mktcap | $350.9M |
| ev | $2.6B |
| ev_ebit | 36.5x |
| fcf | $223.6M |
| fcf_yield | 63.7% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | $2.3B |
| net_debt_ebit | 31.6x |
| cash | $226.2M |
| ltd | $2.5B |
| equity | n/a |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $1.7B |
| revenue_prior | $1.7B |
| rev_growth | -0.2% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $71.9M |
| net_income | $22.2M |
| cfo | $236.2M |
| capex | $12.6M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -13.7% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 51,676,354 |
| shares_py | 59,888,304 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -39.9% |
| r6m | -11.9% |
| off_52w_high | -53.7% |
| adv20 | $3.0M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.99 |
| r_ev_ebit | 0.22 |
| r_roic | 0.50 |
| r_rev_growth | 0.34 |
| r_buyback | 0.96 |
| score | 0.60 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | n/a |
| shares_period | CY2025Q4I |
| shares_py_period | CY2024Q4I |
| capex_missing | False |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 142 |

**Screen rationale:** top-quartile FCF yield 63.7%; buying back stock -13.7%


## 3. Share count trend

- Shares outstanding: **51,676,354** (CY2025Q4I) vs **59,888,304** prior year (CY2024Q4I)
- Change: **-13.7%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No 8-K filings fetched for this ticker._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 20,000 sh / $142,666 -> net $-142,666 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 23 (open-market buys 0, sales 2).

| code | rows |
|---|---|
| A | 9 |
| F | 10 |
| M | 2 |
| S | 2 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release

_Not available: no 8-K with a readable release exhibit was fetched. Current-quarter results are unknown from this pack._

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-03_item7_mdna.md)

_Extraction: no Overview/Results heading found; took the start of Item 7._

ITEM 7. MAJ OR SHAREHOLDERS AND RELATED PARTY TRANSACTIONS

A. Major Shareholders

The following table sets forth information regarding the actual beneficial ownership of Company Common Shares as of February 20, 2026:

•
each person known to us to be the beneficial owner or more than 5% of Company Common Shares;

•
each of our directors and Company Officers; and

•
all our directors and Company Officers as a group.

Beneficial ownership is determined according to the rules of the SEC, which generally provide that a person has beneficial ownership of a security if he, she or it possesses sole or shared voting or investment power over that security, and includes shares underlying options and shares underlying the Company Warrants that are currently exercisable or exercisable within 60 days.

Unless otherwise indicated, we believe that all persons named in the table below have sole voting and investment power with respect to all Company Common Shares beneficially owned by them. Except as otherwise indicated, the address for each shareholder listed below is 2 Gresham Street, 1st Floor, London, United Kingdom EC2V 7AD.

Name and Address of Beneficial Owner | Number (1) of Company Common Shares | Percentage of Company Common Shares
Company Officers, Directors and 5% Holders | ﻿ | ﻿
Parties to our shareholders agreement as a group (2) | 27,802,470 | 54.4 | %
CVC (3) | 12,999,672 | 25.4 | %
Blackstone (4) | 10,914,696 | 21.4 | %
Cannae (5) | - | -
FNF Holdings (6) | 2,250,000 | 4.4 | %
William P. Foley II (7) | 1,638,102 | 3.2 | %
Bruce Lowthers | * | *
John Crawford | * | *
Roy Aston | * | *
Robert Gatto | * | *
Chi-Eun Lee | * | *
Richard Swales | * | *
Elliot Wiseman | * | *
Daniel Henson | * | *
Mark Brooker | * | *
Matthew Bryant | * | *
Anthony Jabbour | * | *
Dagmar Kollmann | * | *
Marianne Heiss | * | *
Jonathan Murphy | * | *
Eli Nagler | * | *
Peter Rutland | * | *
All Company directors and executive officers as a group | * | *

*Less than 1%.

(1)
Numbers have been updated to reflect the reverse stock split.

(2)
Shareholders Agreement means the agreement entered into by the Company, Pi Topco, PGHL, the Founder, Cannae LLC, the CVC Investors and the Blackstone Investors On November 24, 2025, a wholly owned subsidiary of Cannae Holdings, Inc. sold 2,462,237 common shares to the Company in a privately negotiated transaction (the "Repurchase Transaction"). Following the completion of the Repurchase Transaction, Cannae no longer beneficially owns any common shares and is no longer a party to the Shareholders Agreement.

(3)
Based on the most recently available Schedule 13D filed with the SEC on January 3, 2022, as of December 31, 2022. The "CVC Investors" shall refer to Pi Holdings Jersey Limited and Pi Syndication LP. Reflects 8,158,241 Company Common Shares directly held by Pi Holdings Jersey Limited and 4,841,431 Company Common Shares directly held by Pi Syndication LP. The registered address for each CVC Investor is c/o Saltgate Limited, 27 Esplanade, St Helier, Jersey, JE1 1SG, United Kingdom.

(4)
Based on the most recently available Schedule 13D filed with the SEC on January 3, 2022, as of December 31, 2022. Reflects 8,402,943 Company Common Shares directly held by BCP Pi Aggregator (Cayman) L.P., 1,490,243 Company Common Shares directly held by Blackstone Pi Co-Invest (Cayman) L.P., 378,290 Company Common Shares directly held by BCP VII Co-Invest—Star (Cayman) L.P., and 39,055 Company Common Shares directly held by Blackstone Family Investment Partnership (Cayman) VII-ESC L.P. The "Blackstone Funds" shall refer to BCP Pi Aggregator (Cayman) L.P., Blackstone Pi Co-Invest (Cayman) L.P., BCP VII Co-Invest—Star (Cayman) L.P., and Blackstone Family Investment Partnership (Cayman) VII-ESC L.P. The general partner of BCP PI Aggregator (Cayman) L.P. is BCP VII Holdings Manager (Cayman) L.L.C. Blackstone Management Associates (Cayman) VII L.P. is the managing member of BCP VII Holdings Manager (Cayman) L.L.C. and the general partner of each of Blackstone Pi Co-Invest (Cayman) L.P. and BCP VII Co-Invest-Star (Cayman) L.P. The general partners of Blackstone Management Associates (Cayman) VII L.P. and Blackstone Family Investment Partnership (Cayman) VII-ESC L.P. are BCP VII GP L.L.C. and Blackstone LR Associates (Cayman)VII Ltd.., with BCP VII GP L.L.C. controlling Blackstone Management Associates (Cayman) VII L.P. with respect to all matters other than voting of securities of underlying portfolio companies, which power is held by the Class B shareholders of Blackstone LR Associates (Cayman) VII Ltd., who are certain senior personnel of Blackstone. Blackstone Holdings III L.P. is the sole member of BCP VII GP L.L.C. and the sole Class A shareholder of Blackstone LR Associates (Cayman)VII Ltd. Blackstone Holdings III GP L.P. is the general partner of Blackstone Holdings III L.P. Blackstone Holdings III GP Management L.L.C. is the general partner of Blackstone Holdings III GP L.P. Blackstone Inc. is the sole member

of Blackstone Holdings III GP Management L.L.C. The sole holder of the Series II preferred common stock of Blackstone Inc. is Blackstone Group Management L.L.C. Blackstone Group Management L.L.C. is wholly owned by Blackstone's senior managing directors and controlled by its founder, Stephen A. Schwarzman. Each of such Blackstone entities and Mr. Schwarzman may be deemed to beneficially own the shares beneficially owned by the Blackstone Funds directly or indirectly controlled by it or him, but each (other than the Blackstone Funds to the extent of their direct holdings) disclaims beneficial ownership of such shares. The address of each of the entities listed in this footnote is c/o Blackstone Inc., 345 Park Avenue, New York, New York 10154

(5)
Based on the most recently available Schedule 13D/A filed with the SEC on November 25, 2025, On November 24, 2025, Cannae Holdings, LLC sold 2,462,237 Common Shares to the Company in connection with Repurchase Transaction. Following the completion of the Repurchase Transaction, Cannae no longer beneficially owns any Common Shares and is no longer a party to the Shareholders Agreement. "Cannae" shall refer to Cannae Holdings, Inc., a Delaware corporation ("CHI"); and Cannae Holdings, LLC, a Delaware limited liability company and wholly-owned subsidiary of CHI ("CHL"). The address of each of the entities listed in this footnote is 1701 Village Center Circle, Las Vegas, Nevada 89134.

(6)
Based on the most recently available Schedule 13G/A filed with the SEC on December 1, 2025. "Fidelity" shall refer to (i) Fidelity National Financial, Inc. ("FNF"), a Delaware corporation, (ii) Commonwealth Land Title Insurance Company ("CLTIC"), a Florida corporation, (iii) Fidelity National Title Insurance Company ("FNTIC"), a Florida corporation, (iv) Chicago Title Insurance Company ("CTIC"), a Florida corporation, and (v) Fidelity & Guaranty Life Insurance Company ("FGLIC", and collectively with FNF, CLTIC, FNTIC and CTIC, the "FNF Investors"), an Iowa corporation. Reflects 651,725 Company Common Shares directly held by Chicago Title Insurance Company, 831,608 Company Common Shares directly held by Fidelity National Title Insurance Company, 350,000 Company Common Shares directly held by Commonwealth Land Title Insurance Company, and 416,667 Company Common Shares directly held by Fidelity & Guaranty Life Insurance Company. Each of the FNF Holders shares the power to vote and the power to dispose of the Company Common Shares held by it with FNF, and as such, FNF may be deemed to beneficially own the securities held by each of the FNF Investors. The address of FNF, CLTIC, FNTIC, and CTIC is 601 Riverside Ave, Jacksonville, Florida 32204. The address of FGLIC is 801 Grand Ave., Suite 2600, Des Moines, Iowa 50309.

(7)
Based on the most recently available Schedule 13D/A filed with the SEC on November 25, 2025. Reflects 1,638,101 Company Common Shares. Trasimene Capital FT, LLC II has sole voting and dispositive power over the Company Common Shares owned by Trasimene Capital FT, LP II. William P. Foley, II is the sole member of Trasimene Capital FT, LLC II, and therefore may be deemed to beneficially own the Company Common Shares described in this footnote, and ultimately exercises voting and dispositive power over such shares held by Trasimene Capital FT, LP II. Mr. Foley disclaims beneficial ownership of these shares except to the extent of any pecuniary interest therein. The address of William Foley, II and each entity listed in this footnote is 1701 Village Center Circle, Las Vegas, Nevada 89134

Please refer to "B. Related Party Transactions" and the Paysafe Consolidated Financial Statements for further information related to the Transaction. Other than the various rights set forth in such sections, the major shareholders set forth in the table above do not have different voting rights on their Company Common Shares.

B. Related Party Transactions

Policies and Procedures for Related Person transactions

The Company Board has adopted a written related person transaction policy that sets forth the following policies and procedures for the review and approval or ratification of related person transactions. A "Related Person Transaction" is a transaction, arrangement or relationship in which the post-combination company or any of its subsidiaries was, is or will be a participant, the amount of which involved exceeds $120,000, and in which any related person had, has or will have a direct or indirect material interest. A "Related Person" means:

•
any person who is, or at any time during the applicable period was, one of the post-combination company's executive officers or one of the post-combination company's directors;

•
any person who is known by the post-combination company to be the beneficial owner of more than 5% of Paysafe's voting stock;

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
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-03_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | **MISSING** |

**Present:** meta.json, form4_summary.md, 10-K_2026-03-03_item7_mdna.md

**Missing:** 8-K filings, 8-K earnings press release exhibit, 10-K Item 1 - Business (business description), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
