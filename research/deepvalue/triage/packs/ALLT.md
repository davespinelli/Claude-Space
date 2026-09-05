# Triage pack — ALLT · Allot Ltd.

_Generated 2026-09-05 00:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** ALLT · **Name:** Allot Ltd.
- **CIK:** 0001365767
- **SIC:** 3576 — Computer Communications Equipment
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/ALLT

**Fetcher warnings for this ticker:** 10-K 2026-03-26: heading split missed Item 1 - Business, Item 1A - Risk Factors; no 10-Q in recent filings; no proxy (DEF 14A) in recent filings

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Allot Ltd.
- **CIK:** 1,365,767 · **SIC:** 3576 (Computer Communications Equipment) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 7.57 |
| mktcap | $368.2M |
| ev | $351.1M |
| ev_ebit | 97.4x |
| fcf | $15.5M |
| fcf_yield | 4.2% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 3.0% |
| net_debt | -$17.1M |
| net_debt_ebit | -4.7x |
| cash | $17.1M |
| ltd | $0.00 |
| equity | $113.3M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $102.0M |
| revenue_prior | $92.2M |
| rev_growth | 10.6% |
| rev_growth_note | share count +23.1% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | n/a |
| ebit | $3.6M |
| net_income | $3.7M |
| cfo | $17.8M |
| capex | $2.3M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 23.1% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 48,645,282 |
| shares_py | 39,530,993 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -6.8% |
| r6m | 8.8% |
| off_52w_high | -34.2% |
| adv20 | $2.1M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.44 |
| r_ev_ebit | 0.06 |
| r_roic | 0.42 |
| r_rev_growth | 0.67 |
| r_buyback | 0.07 |
| score | 0.33 |

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
| rank | 381 |

**Screen rationale:** share count +23.1% yoy — growth may be acquisition/issuance-driven, not organic; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **48,645,282** (CY2025Q4I) vs **39,530,993** prior year (CY2024Q4I)
- Change: **23.1%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`
- **Flag:** share count +23.1% yoy — growth may be acquisition/issuance-driven, not organic

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No 8-K filings fetched for this ticker._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 113,333 sh / $882,511 -> net $-882,511 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 13 (open-market buys 0, sales 12).

| code | rows |
|---|---|
| A | 1 |
| S | 12 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release

_Not available: no 8-K with a readable release exhibit was fetched. Current-quarter results are unknown from this pack._

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-26_item7_mdna.md)

_Extraction: no Overview/Results heading found; took the start of Item 7._

ITEM 7 : Major Shareholders and Related Party Transactions

A. Major Shareholders

The following table sets forth certain information regarding the beneficial ownership
of our outstanding ordinary shares as of March 6, 2026, by each person who we know beneficially owns 5.0% or more of the outstanding ordinary
shares. Each of our shareholders has identical voting rights with respect to its shares. All of the information with respect to beneficial
ownership of the ordinary shares is given to the best of our knowledge.

Ordinary Shares Beneficially Owned(1) | Percentage of Ordinary Shares Beneficially Owned
Lynrock Lake Master Fund LP (2) | 10,011,295 | 20.5 | %
QVT Family Office Fund LP (3) | 5,062,523 | 10.3 | %
David Kanen (4) | 4,163,573 | 8.5 | %

(1) | As used in this table, "beneficial ownership" means the sole or shared power to vote or direct the voting or to dispose or direct the disposition of any security. For purposes of this table, a person is deemed to be the beneficial owner of securities that can be acquired within 60 days from March 6, 2026 through the exercise of any option or warrant. Ordinary shares subject to options or warrants that are currently exercisable or exercisable within 60 days are deemed outstanding for computing the ownership percentage of the person holding such options or warrants, but are not deemed outstanding for computing the ownership percentage of any other person. The amounts and percentages are based upon 48,923,099 ordinary shares outstanding as of March 6, 2026.

(2) | Based on a Schedule 13D/A filed on November 14, 2025, Lynrock Lake Master Fund LP directly holds 10,011,295 of our ordinary shares. Cynthia Paul, the Chief Investment Officer of Lynrock Lake LP ("Lynrock Lake") and sole member of Lynrock Lake Partners LLC, the general partner of Lynrock Lake, may be deemed to exercise voting and investment power over securities of the Issuer held by Lynrock Lake Master Fund LP. The principal executive offices for Lynrock Lake Master Fund LP is 2 International Drive, Suite 130, Rye Brook, NY, 10573.

(3) | Based on a Schedule 13D/A filed on November 20, 2025, QVT Family Office Fund LP ("QVT Fund") had shared voting and dispositive power over 5,062,523 of our ordinary shares. QVT Financial LP ("QVT Financial"), as the investment manager for QVT Fund, and QVT Associates GP LLC ("QVT Fund GP"), was the general partner of the QVT Fund, has voting and dispositive power over these shares. The principal executive offices of QVT Fund, QVT Financial and QVT Fund GP is 888 Seventh Avenue, 43rd Floor, New York, New York 10106.

(4) | Based on a Schedule 13G/A filed on June 12, 2025 by Philotimo Fund, LP, a Delaware limited partnership ("Philotimo"), Philotimo Focused Growth & Income Fund, a series of World Funds Trust and a Delaware statutory trust ("PHLOX"), Kanen Wealth Management LLC, a Florida limited liability company ("KWM") and David L. Kanen, Philotomo beneficially owned 2,325,000 of our ordinary shares, PHLOX beneficially owned 1,200,000 of our ordinary shares, KWM and David L. Kanen had each shared voting and dispositive power over 4,103,882of our ordinary shares, and David L. Kanen had sole voting and dispositive power over 59,691 of our ordinary shares. David L. Kanen is the managing member of KWM and has voting and dispositive power over these shares. The business address of such holders is 6810 Lyons Technology Circle, Suite 160, Coconut Creek, Florida 33073.

Significant Changes in the Ownership of Major Shareholders

To our knowledge, other than as disclosed in the table above, our other filings with the SEC and this annual
report, there has been no significant change in the percentage ownership held by any major shareholder since January 1, 2023.

Record Holders

As of March 6, 2026, there were 15 record holders of ordinary shares, of which seven
consisted of U.S. record holders holding approximately 99.99% of our outstanding ordinary shares. The actual number of shareholders is
greater than this number of record holders, and includes shareholders who are beneficial owners, but whose shares are held in street name
by brokers and other nominees. The U.S. record holders included Cede & Co., the nominee of the Depositary Trust Company.

B. Related Party Transactions

Our policy is to enter into transactions with related parties on terms that, on the
whole, are no less favorable, than those available from unaffiliated third parties. Based on our experience in the business sectors in
which we operate and the terms of our transactions with unaffiliated third parties, we believe that all of the transactions described
below met this policy standard at the time they occurred.

Repayment of Lynrock Note

In June 2025, pursuant to an agreement reached with Lynrock Lake Master Fund LP ("Lynrock"),
$31.41 million of the outstanding principal amount under the senior unsecured convertible promissory note with a face value of $40.0 million
issued by us to Lynrock on February 18, 2022 (the "Lynrock Note") was repaid and cancelled in exchange for $31.41 million
in cash and the remaining $8.59 million principal amount outstanding under the Lynrock Note was converted into 1,249,995 ordinary shares,
representing a conversion rate per $1,000 principal amount equal to 145.5175 shares representing $1,164.14 divided by the $8.00 public
offering price in our June 2025 public offering. As a result, the Company recognized a loss from extinguishment in the amount of $1,410.

Agreements with Directors, Officers and Suppliers

Engagement of Officers. We have entered into
employment agreements with each of our officers, who work for us as employees or as consultants. These agreements all contain provisions
standard for a company in our industry regarding noncompetition, confidentiality of information and assignment of inventions. The enforceability
of covenants not to compete in Israel may be limited. In connection with the engagement of our officers, we have granted them options
pursuant to our 2016 Plan.

Exculpation, Indemnification and Insurance.
Our articles of association permit us to exculpate, indemnify and insure our office holders, in accordance with the provisions of the
Companies Law. We have entered into agreements with each of our directors and certain office holders, exculpating them from a breach of
their duty of care to us to the fullest extent permitted by law and undertaking to indemnify them to the fullest extent permitted by law,
to the extent that these liabilities are not covered by insurance. See "ITEM 6: Directors, Senior Management and Employees-Board
Practices-Exculpation, Insurance and Indemnification of Office Holders."

C. Interests of Experts and Counsel

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
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-26_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | **MISSING** |

**Present:** meta.json, form4_summary.md, 10-K_2026-03-26_item7_mdna.md

**Missing:** 8-K filings, 8-K earnings press release exhibit, 10-K Item 1 - Business (business description), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
