# Triage pack — INMD · InMode Ltd.

_Generated 2026-09-04 13:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** INMD · **Name:** InMode Ltd.
- **CIK:** 0001742692
- **SIC:** 3845 — Electromedical & Electrotherapeutic Apparatus
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/INMD

**Fetcher warnings for this ticker:** 10-K 2026-02-10: heading split missed Item 1 - Business, Item 1A - Risk Factors; no 10-Q in recent filings; no proxy (DEF 14A) in recent filings

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** InMode Ltd.
- **CIK:** 1,742,692 · **SIC:** 3845 (Electromedical & Electrotherapeutic Apparatus) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 14.84 |
| mktcap | $940.2M |
| ev | $637.7M |
| ev_ebit | 7.5x |
| fcf | $84.3M |
| fcf_yield | 9.0% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 17.7% |
| net_debt | -$302.5M |
| net_debt_ebit | -3.5x |
| cash | $302.5M |
| ltd | $0.00 |
| equity | $683.2M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $370.5M |
| revenue_prior | $394.8M |
| rev_growth | -6.2% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $85.4M |
| net_income | n/a |
| cfo | $85.3M |
| capex | $972k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -8.9% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 63,358,750 |
| shares_py | 69,558,670 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 4.8% |
| r6m | 10.3% |
| off_52w_high | -10.7% |
| adv20 | $6.5M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.69 |
| r_ev_ebit | 0.85 |
| r_roic | 0.85 |
| r_rev_growth | 0.16 |
| r_buyback | 0.93 |
| score | 0.75 |

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
| rank | 34 |

**Screen rationale:** cheap at 7.5x EV/EBIT; high ROIC 17.7%; buying back stock -8.9%; debt data missing (net cash unverified); 12-1 momentum 4.8%


## 3. Share count trend

- Shares outstanding: **63,358,750** (CY2025Q4I) vs **69,558,670** prior year (CY2024Q4I)
- Change: **-8.9%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No 8-K filings fetched for this ticker._

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 4; transaction rows: 4 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 4 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release

_Not available: no 8-K with a readable release exhibit was fetched. Current-quarter results are unknown from this pack._

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-10_item7_mdna.md)

_Extraction: no Overview/Results heading found; took the start of Item 7._

ITEM 7. MAJOR SHAREHOLDERS AND RELATED PARTY TRANSACTIONS

A. Major Shareholders

The following table sets forth certain information regarding the beneficial ownership
of our outstanding ordinary shares, as of the date of this Annual Report on Form 20-F, by each person or entity who we know beneficially
owns 5% or more of the outstanding ordinary shares. For purposes of the table below, we deem ordinary shares issuable pursuant to options,
restricted share units or warrants that are currently exercisable or exercisable within 60 days of the date of this Annual Report on Form
20-F, if any, to be outstanding and to be beneficially owned by the person holding the options, restricted share units or warrants for
the purposes of computing the percentage ownership of that person, but we do not treat them as outstanding for the purpose of computing
the percentage ownership of any other person. Percentages for table below are based on 63,358,750 ordinary shares (excluding treasury
shares) outstanding as of December 31, 2025, and options to purchase ordinary shares and restricted share units in a total of 101,000
exercisable within 60 days of December 31, 2025, of our officers, directors and major shareholders (see "Item 6E. Directors, Senior
Management and Employees-Share Ownership").

As of February 2, 2026, we had approximately 39,694 shareholders of record of our
ordinary shares, approximately 32,602 of which are U.S. persons. These U.S. persons hold approximately 51% of our outstanding share capital.
The actual number of beneficial owners is substantially greater than the number of shareholders of record because a large portion of our
ordinary shares are held in street name by brokers and other nominees. This number of shareholders of record also does not include shareholders
whose shares may be held in trust by other entities.

None of our shareholders have different voting rights from other shareholders. We are
not aware of any arrangement that may, at a subsequent date, result in a change of control of the Company.

Number of Ordinary Shares | Percentage
Moshe Mirazhy | 3,499,226 | 5.51 | %

B. Related Party Transactions

Relationship with Home Skinovations Ltd. (under voluntary liquidation)

Mr. Moshe Mizrahy, our Chief Executive Officer and director, is a substantial shareholder
and board member of Home Skinovations, and Dr. Hadar Ron, one of our directors, serves on the board of directors of Home Skinovations.

Home Skinovations is involved in the development, manufacture and distribution of home-use
light-based devices for aesthetic applications, which include hair removal, anti-aging, microdermabrasion, cellulite and acne treatments.
Except as detailed below, we have no commitments to, or agreements with, Home Skinovations or any of its subsidiaries, including with
respect to any mutual research and development, indebtedness, financing, debt or credit lines, or any jointly-owned intellectual property
or like arrangements, and we do not share tangible or intangible assets with Home Skinovations or any of its subsidiaries. Any future
agreements with Home Skinovations must be reviewed and approved by our audit committee and board of directors.

Service Agreements

From time to time, we receive certain services from, and provide certain services to,
Home Skinovations. We do not consider these services to be material. The services have historically included an office sublease in Israel,
mobile phone services, use of certain computer hardware and switchboard infrastructure, certain software licenses and limited personnel
services. We did not receive any services from Home Skinovations for the year ended December 31, 2025.

Relationship with Himalaya Family Office Consulting Ltd.

Mr. Moshe Mizrahy, our Chief Executive Officer and Director, is a minor shareholder
and board member of Himalaya Family Office Consulting Ltd., a company engaged in providing global investment portfolio management and
risk management & analysis services.

We receive certain investment portfolio management services from Himalaya Family Office
Consulting Ltd., with respect to part of our investment portfolio, and recorded expenses related to those services in the amount of $62
thousand for the year ended December 31, 2025.

Agreements and Arrangements with Directors and Executive Officers

We have entered into written employment or consulting agreements with each of our executive
officers. See "Item 6. Directors, Senior Management and Employees – B. Compensation- Employment and Consulting Agreements."

Members of our board of directors are entitled to certain compensation for their services.
See "Item 6. Directors, Senior Management and Employees – C. Board Practices – Committees of the Board of Directors
– Compensation, Nominating and Governance Committee."

Options

Since our inception, we have granted options to purchase our ordinary shares to our
executive officers and certain of our directors. The options are generally subject to the further terms of the respective option plans,
which we describe under "Item 6.B. Compensation-Employee Benefit Plans."

RSUs (restricted share units)

Under the 2018 Incentive Plan, we have granted RSUs to our executive officers and certain
of our directors. The RSUs are generally subject to the further terms of the 2018 Incentive Plan, which we describe under "Item
6.B. Compensation-Employee Benefit Plans-2018 Incentive Plan."

Directors and Officers Insurance Policy and Indemnification and Exculpation Agreements

We have entered into separate indemnification agreements with each of our current directors,
office holders and other executives exculpating them from a breach of their duty of care to us to the fullest extent permitted by law
and undertaking to indemnify them to the fullest extent permitted by law. We have also obtained directors' and officers' liability
insurance for each of our executive officers and directors. See "Item 6C. Directors, Senior Management and Employees-Board Practices-Exculpation,
Indemnification and Insurance of Directors and Officers" for additional information.

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
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-10_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | **MISSING** |

**Present:** meta.json, form4_summary.md, 10-K_2026-02-10_item7_mdna.md

**Missing:** 8-K filings, 8-K earnings press release exhibit, 10-K Item 1 - Business (business description), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
