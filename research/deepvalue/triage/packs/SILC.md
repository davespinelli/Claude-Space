# Triage pack — SILC · SILICOM LTD.

_Generated 2026-09-04 23:11 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** SILC · **Name:** SILICOM LTD.
- **CIK:** 0000916793
- **SIC:** 3576 — Computer Communications Equipment
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/SILC

**Fetcher warnings for this ticker:** 10-K 2026-04-28: heading split missed Item 1 - Business, Item 1A - Risk Factors; no 10-Q in recent filings; no proxy (DEF 14A) in recent filings

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** SILICOM LTD.
- **CIK:** 916,793 · **SIC:** 3576 (Computer Communications Equipment) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 40.07 |
| mktcap | $228.6M |
| ev | $193.5M |
| ev_ebit | n/a |
| fcf | -$3.3M |
| fcf_yield | -1.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -11.8% |
| net_debt | -$35.2M |
| net_debt_ebit | n/a |
| cash | $35.2M |
| ltd | $0.00 |
| equity | $117.5M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $61.9M |
| revenue_prior | $58.1M |
| rev_growth | 6.6% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$12.3M |
| net_income | -$11.5M |
| cfo | -$2.2M |
| capex | $1.2M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -1.0% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 5,706,142 |
| shares_py | 5,766,286 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 172.3% |
| r6m | 112.2% |
| off_52w_high | -21.4% |
| adv20 | $9.7M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.16 |
| r_ev_ebit | 0.00 |
| r_roic | 0.11 |
| r_rev_growth | 0.56 |
| r_buyback | 0.75 |
| score | 0.37 |

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
| rank | 354 |

**Screen rationale:** buying back stock -1.0%; debt data missing (net cash unverified); 12-1 momentum 172.3%


## 3. Share count trend

- Shares outstanding: **5,706,142** (CY2025Q4I) vs **5,766,286** prior year (CY2024Q4I)
- Change: **-1.0%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No 8-K filings fetched for this ticker._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 48,041 sh / $2,331,772 -> net $-2,331,772 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 15 (open-market buys 0, sales 5).

| code | rows |
|---|---|
| M | 10 |
| S | 5 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release

_Not available: no 8-K with a readable release exhibit was fetched. Current-quarter results are unknown from this pack._

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-04-28_item7_mdna.md)

_Extraction: no Overview/Results heading found; took the start of Item 7._

Item 7 .
MAJOR SHAREHOLDERS AND RELATED PARTY TRANSACTIONS

A. Major
Shareholders

The following table sets forth, as of March 31, 2026, the number
of Ordinary Shares, including options and warrants to purchase Ordinary Shares exercisable within 60 days, owned by all shareholders known
to the Company to own more than five percent (5%) of the Company's Ordinary Shares (based on 5,706,142 Ordinary Shares outstanding
on that date). Each of our shareholders has identical voting rights with respect to its shares. All of the information with respect to
beneficial ownership of the Ordinary Shares is given to the best of our knowledge. Except where otherwise indicated, and subject to applicable
community property laws, we believe, based on information furnished to us by such owners or otherwise disclosed in any public filings,
that the beneficial owners of the Ordinary Shares listed below have sole dispositive and voting power with respect to such Ordinary Shares.

Name of Shareholder | Number of Shares and Options Owned (1) | Percentage of Outstanding Shares
Systematic Financial Management, LP (2) | 553,619 | 9.70%
First Wilshire Securities Management, Inc. (3) | 304,808 | 5.34%

(1) | The table above includes the number of shares and options that are exercisable within 60 days of March 31, 2026. Ordinary shares subject to these options are deemed beneficially owned for the purpose of computing the ownership percentage of the person or group holding these options, but are not deemed outstanding for purposes of computing the ownership percentage of any other person. Except where otherwise indicated, and subject to applicable community property laws, based on information furnished to us by such owners or otherwise disclosed in any public filings, to our knowledge, the persons and entities named in the table have sole voting and dispositive power with respect to all shares shown as beneficially owned by them. All the information detailed in this table is as set forth in major shareholders' public filings, unless stated otherwise.

(2) | As reported on Schedule 13G/A filed by Systematic Financial Management, LP with the SEC on February 10, 2026.

(3) | As reported on Schedules 13G/A filed by First Wilshire Securities Management, Inc. with the SEC on February 11, 2026.

The Company's major shareholders do not have different voting rights.

As of March 31, 2026, there were five record holders of ordinary
shares, including three record holders in the United States. Collectively, these three record holders in the United States held less than
1% of the outstanding ordinary shares.

B. Related
Party Transactions

All related party transactions and arrangements (or modifications
of existing ones) with our related parties, transactions in which office holders of the Company have a personal interest, or transactions
which raise issues of such office holders' fiduciary duties, are subject to the applicable corporate approvals under the Companies Law.
Without giving effect to the buyback purchases described at Item 16E, the following transactions are considered "related party transactions"
for this Item 7B:

In January 2004, Our shareholders approved an Indemnification Agreement
with our directors and office holders, which has since been amended on a number of occasions.

The Indemnification Agreement provides that our directors and office
holders will be exempt from liability in certain circumstances. The Indemnification Agreement also provides for the indemnification by
the Company for certain obligations and expenses imposed on the office holder in connection with acts performed in his or her capacity
as an office holder of the Company. This right to indemnification is limited, and does not cover, among other things, a breach of an office
holder's duty of loyalty, a willful breach of an office holder's duty of care, or a reckless disregard for the circumstances or consequences
of a breach of a duty of care. The right to indemnification also does not cover acts that are taken intentionally to unlawfully realize
personal gain. The maximum amount of our liability under these Indemnification Agreements for any monetary obligation imposed on an office
holder or a director in favor of another person by a judgment is currently US$ 3,000,000 for each instance of a covered scenario. In addition,
we would be liable to indemnify the office holder or director for all reasonable litigation expenses with respect to certain proceedings.
We have maintained liability insurance for our directors and office holders. On September 23, 2007, our shareholders approved the procurement
of a policy, which provides for total coverage of up to US$ 4,000,000. All of our directors are parties to our Indemnification Agreements
and are covered by our directors and office holders' insurance policy.

Under our Executive Compensation Policy, any change to the Indemnification
Agreement or the insurance policy, including the cost and/or any changes which materially depart from the key terms of the current agreement
and/or insurance policy (provided that such changes apply equally to all executives of the Company, including directors) will be submitted
to the Company's compensation committee and the Board of Directors for their approval but shall not, unless required by law or the Company's
Articles of Association, be presented at a General Meeting of the Shareholders.

Compensation Package for Liron Eizenman, the
Company's President and Chief Executive Officer

In June 2022, following the approval of the Company's Compensation
Committee and Board of Directors, the Company's shareholders approved a compensation package for Liron Eizenman. The approved Compensation
Package consists of (i) an amendment to Liron Eizenman's compensation structure and (ii) a severance agreement, identical to the previous
CEO severance agreement. The principal terms of the compensation package, which commenced on July 1, 2022, are as follows:

• | Gross monthly base salary of NIS 70,000. In January 2026, our compensation committee and board of directors, respectively, approved an increase in Liron Eizenman's monthly base salary to NIS 73,850, effective January 1, 2026. This increase is subject to the approval of annual general meeting, which is expected to be held in June 2026.

• | Entitlement to the Chief Executive Officer annual bonus upon the terms and in accordance with the formula approved by the Company's shareholders at the Annual General Meeting held on June 8, 2016 (the " CEO Bonus "),

• | Standard social benefits package applicable to all full-time employees of the Company.

• | Severance/Termination provisions.

In addition, at the June 2022 General Meeting, our shareholders
approved a grant to Liron Eizenman of 50,000 options to purchase Ordinary Shares of the Company, pursuant to the Plan. Pursuant to the
terms of their grant, all of these options expired following the closing price of our shares falling below US$ 17.45 and remaining at
or below such price for a period of at least 30 days.

In light of the automatic expiration of all of the options granted
to Mr. Liron Eizenman, in March 2024, our Compensation Committee and Board of Directors approved the grant of 100,000 options under the
Plan as extended, to purchase our Ordinary Shares at an exercise price equal to the average closing price of our Ordinary Shares on the
thirty (30) trading days preceding the date of the approval of such grant by our shareholders. 50% of the options will vest on the second
anniversary of the date of shareholder approval (the "Grant Date"), and 50% will vest on the third anniversary of the Grant
Date, and which Plan Options (vested and unvested) shall expire, by their terms, upon the eighth anniversary of the Grant Date. Following
the rejection by our shareholders of the option grant at their meeting in June 2024, our compensation committee and board of directors
reconsidered the grant, and pursuant to Israeli law, based on detailed reasoning overrode the rejection and approved the grant.

At the Annual General Meeting held on June 18, 2025, our shareholders
approved an additional grant to Liron Eizenman of 13,333 options to purchase Ordinary Shares of the Company, pursuant to the Plan. The
exercise price of the options equals the average closing price of our Ordinary Shares on the 30 trading days preceding the date of the
meeting, with 50% vesting on the second anniversary of the grant date and 50% vesting on the third anniversary of the grant date. The
options (vested and unvested) will expire on the eighth anniversary of the grant date.

Additionally, on January 26, 2026 the Compensation Committee and
Board of Directors approved the grant of 38,333 RSUs to Liron Eizenman. One third of which will vest on the first anniversary following
the date of approval by the Board of Directors, or the Grant Date, one third will vest on the second anniversary of the Grant Date, and
one third will vest on the third anniversary of the Grant Date. The grant is subject to the approval of our annual general meeting, which
is expected to be held in June 2026.

Grants of Options and RSUs to Avi Eizenman

In light of the automatic expiration of all of the options granted
to Mr. Avi Eizenman, in March 2024, our Compensation Committee and Board of Directors approved the grant of 60,000 options under the Plan,
as extended to purchase our Ordinary Shares at an exercise price equal to the average closing price of our Ordinary Shares on the thirty
(30) trading days preceding the date of the approval of such grant by our shareholders. 50% of the options will vest on the second anniversary
of the date of shareholder approval (the "Grant Date"), and 50% will vest on the third anniversary of the Grant Date, and
which Plan Options (vested and unvested) shall expire, by their terms, upon the eighth anniversary of the Grant Date.

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
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-04-28_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | **MISSING** |

**Present:** meta.json, form4_summary.md, 10-K_2026-04-28_item7_mdna.md

**Missing:** 8-K filings, 8-K earnings press release exhibit, 10-K Item 1 - Business (business description), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
