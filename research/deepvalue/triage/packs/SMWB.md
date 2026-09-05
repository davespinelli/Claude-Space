# Triage pack — SMWB · SIMILARWEB LTD.

_Generated 2026-09-05 00:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** SMWB · **Name:** SIMILARWEB LTD.
- **CIK:** 0001842731
- **SIC:** 7370 — Services-Computer Programming, Data Processing, Etc.
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/SMWB

**Fetcher warnings for this ticker:** 10-K 2026-03-02: heading split missed Item 1 - Business, Item 1A - Risk Factors; no 10-Q in recent filings; no proxy (DEF 14A) in recent filings

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** SIMILARWEB LTD.
- **CIK:** 1,842,731 · **SIC:** 7370 (Services-Computer Programming, Data Processing, Etc.) · **Exchange:** NYSE

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 8.89 |
| mktcap | $773.1M |
| ev | $700.7M |
| ev_ebit | n/a |
| fcf | $13.2M |
| fcf_yield | 1.7% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | -$72.4M |
| net_debt_ebit | n/a |
| cash | $72.4M |
| ltd | $0.00 |
| equity | $23.3M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $282.6M |
| revenue_prior | $249.9M |
| rev_growth | 13.1% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$23.6M |
| net_income | -$32.9M |
| cfo | $14.6M |
| capex | $1.5M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 5.3% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 86,962,202 |
| shares_py | 82,618,511 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -25.7% |
| r6m | 204.5% |
| off_52w_high | -12.0% |
| adv20 | $9.7M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.28 |
| r_ev_ebit | 0.00 |
| r_roic | 0.50 |
| r_rev_growth | 0.72 |
| r_buyback | 0.18 |
| score | 0.34 |

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
| rank | 376 |

**Screen rationale:** debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **86,962,202** (CY2025Q4I) vs **82,618,511** prior year (CY2024Q4I)
- Change: **5.3%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No 8-K filings fetched for this ticker._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 271,105 sh / $1,020,716 vs sells 1,092,724 sh / $9,704,917 -> net $-8,684,201 (SELLING).
Distinct insiders buying (code P): 4. Largest buy: Beit-On Harel Moshe bought 75,000 sh @ $3.89 ($291,750) on 2026-05-20.

Form 4 filings parsed: 7; transaction rows: 33 (open-market buys 7, sales 10).

| code | rows |
|---|---|
| M | 16 |
| P | 7 |
| S | 10 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release

_Not available: no 8-K with a readable release exhibit was fetched. Current-quarter results are unknown from this pack._

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-02_item7_mdna.md)

_Extraction: no Overview/Results heading found; took the start of Item 7._

Item 7. Major Shareholders and Related Party Transactions

A. Major Shareholders

The following table sets forth information with respect to the beneficial ownership of our shares as of the date of this Annual Report by:

• each person or entity, or group of affiliated persons, known by us to beneficially own 5% or more of our outstanding shares;

• each of our directors and executive officers individually; and

• all of our executive officers and directors as a group.

The beneficial ownership of ordinary shares is determined in accordance with the SEC rules and generally includes any ordinary shares over which a person exercises sole or shared voting or investment power. For purposes of the table below, we deem shares subject to options or RSUs that are currently exercisable or exercisable within 60

days of February 14, 2026, to be outstanding and to be beneficially owned by the person holding the options or RSUs for the purposes of computing the percentage ownership of that person but we do not treat them as outstanding for the purpose of computing the percentage ownership of any other person. The percentage of shares beneficially owned is based on 86,966,452 ordinary shares outstanding as of February 14, 2026.

All of our shareholders, including the shareholders listed below, have the same voting rights attached to their ordinary shares. See "Description of share capital and articles of association—Voting rights." Unless otherwise noted below, each shareholder's address is 33 Yitzhak Rabin Rd., Givatayim 5348303, Israel.

A description of any material relationship that our principal shareholders have had with us or any of our affiliates within the past three years is included under "Certain relationships and related party transactions."

Name of Beneficial Owner | Number | %
Greater than 5% Shareholders
Anglo-Peacock Nominees Limited (1) | 8,883,950 | 10.2%
Viola Group (2) | 10,810,778 | 12.4%
MIH E-Commerce Holdings B.V. (3) | 11,173,265 | 12.8%
Directors and Executive Officers
Joshua Alliance (4) | 8,883,950 | 10.2%
Harel Beit-On (5) | 10,810,778 | 12.4%
Or Offer (6) | 6,053,910 | 6.8%
Ran Vered | [*] | [*]
Benjamin Seror | [*] | [*]
Tamar Rapaport-Dagim | [*] | [*]
Kipp Bodnar | [*] | [*]
Barak Eilam | [*] | [*]
Lisa Campbell | [*] | [*]
Joe Del Preto | [*] | [*]
All directors and executive officers as a group (10 persons) | 26,408,344 | 29.4%

*Indicates ownership of less than 1%.

(1) Consists of 8,883,950 shares, which converted from preferred shares pre-IPO to ordinary shares post-IPO, held by Anglo-Peacock Nominees Limited, as nominee for Joshua Jacob Moshe Alliance. Mr. Alliance has sole voting and dispositive power over the shares. The principal business address of Anglo-Peacock Nominees Limited is Suite 1B Maclaren House, Lancastrian Office Centre, Talbot Road, Manchester, M32 0FP, United Kingdom, Attention Allan Pye.

(2) Based on information available to us, represents (a) 2,134,916 ordinary shares held by Viola Growth II (A) L.P. ("Viola II (A)"); (b) 2,823,094 ordinary shares held by Viola Growth II (B) L.P. ("Viola II (B)"); (c) 5,581,225 ordinary shares held by VG SW, L.P. ("VG LP"); (d) 101,413 ordinary shares held by VG SW GP, L.P.; (e) 170,130 ordinary shares held by Viola partners Fund 4 2013 L.P. ("Viola 4 LP") (collectively "Viola Group"). The general partner of Viola II (A) and Viola II (B) is Viola Growth II, L.P. and its general partner is Viola Growth II GP Ltd. The general partner of VG L.P. is VG SW GP, L.P. and its general partners are Viola Growth II GP Ltd. and Viola Growth 3 Ltd. Harel Beit-On, a member of our board of directors, is a Co- Founder and Managing Partner of Viola Group. Mr. Beit-On disclaims any beneficial ownership of the subject shares except to the extent of any pecuniary interest therein. The address of each of these entities is c/o Viola Growth 12 Abba Eban Avenue, Ackerstein Towers, Building D, Herzeliya 4672530, Israel.

(3) Based on information available to us, represents 11,173,265 ordinary shares held by Naspers Ltd. and Prosus N.V. Prosus Ventures is a wholly-owned subsidiary of MIH e-commerce Holdings B.V., which in turn is a wholly-owned subsidiary of MIH Internet Holdings B.V., which is a wholly-owned subsidiary of Prosus, which is a majority-owned subsidiary of Naspers. Prosus Venutres is controlled by Prosus and Naspers, which share voting and dispositive control over the shares held by Prosus Venutres. Naspers owns 41.4% of the voting rights of Prosus. As a result, ordinary shares of Similarweb Ltd. owned by Naspers Ltd. and Prosus N.V. may be deemed to be beneficially owned by Prosus and Naspers. Prosus is a publicly-traded limited liability company incorporated under the laws of the Netherlands. Naspers is a publicly-traded limited liability company incorporated under the laws of the Republic of South Africa. The address of Prosus N.V. is Gustav Mahlerplein 5, 1082 MS, Amsterdam, The Netherlands and the address for Naspers Ltd. is Media24 Centre 40 Heerengracht, Cape Town 8001, South Africa.

(4) Consists of shares held by Anglo-Peacock Nominees Limited. See footnote (1) above.

(5) Consists of shares held by entities affiliated with Viola Growth. See footnote (2) above.

(6) Based on information available to us, represents 3,459,041 ordinary shares held by Mr. Offer and 2,594,869 ordinary shares issuable upon the exercise of options that vest within 60 days of February 15, 2026.

Record Holders

As of February 14, 2026, 86,966,452 of our ordinary shares were issued and outstanding. Based on the information provided to us by our transfer agent, approximately 73.3% of our total outstanding ordinary shares were held by 19 record holders in the United States, including Cede & Co., the nominee of The Depository Trust Company.

B. Related Party Transactions

The following is a description of related-party transactions we have entered into since January 1, 2022 with any of the members of the board of directors, executive officers or holders of more than 5% of any class of our voting securities at the time of such transaction.

Rights of Appointment

We are not a party to, and are not aware of, any voting agreements among our shareholders.

Agreements with Directors and Officers

Employment Agreements. We have entered into employment agreements with each of our executive officers who works for us as an employee. These agreements each contain provisions regarding non-competition, confidentiality of information and assignment of inventions. The enforceability of covenants not to compete is subject to limitations.

The provisions of certain of our executive officers' employment agreements contain termination or change of control provisions. With respect to certain executive officers, either we or the executive officer may terminate his or her employment by giving 90 calendar days' advance written notice to the other party. We may also terminate an executive officer's employment agreement for good reason (as defined the applicable employment agreement) or in the event of a merger or acquisition transaction.

Equity Awards. Since our inception, we have granted options to purchase our ordinary shares to our executive officers and certain of our directors. In November 2020, we began granting restricted share units, or RSUs, to our executive officers. Such equity agreements may contain acceleration provisions upon certain merger, acquisition or change of control transactions. We describe our equity plans under "Management—Equity incentive plans."

Exculpation, Indemnification and Insurance. Our amended and restated articles of association permits us to exculpate, indemnify and insure our office holders to the fullest extent permitted by the Companies Law. We have entered into agreements with certain office holders, exculpating them from a breach of their duty of care to us to the fullest extent permitted by law and undertaking to indemnify them to the fullest extent permitted by law, subject to certain exceptions, including with respect to liabilities resulting from our IPO to the extent that these liabilities are not covered by insurance.

Related Party Transactions

Pursuant to the Companies Law, the audit committee has the primary responsibility for reviewing and approving or disapproving related party transactions, which are transactions between us and related persons in which we or a related person has or will have a direct or indirect material interest. Our audit committee charter provides that the audit committee shall review and approve or disapprove any related party transactions. See "Board Practices—Approval of Related Party Transactions under Israeli Law."

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
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-02_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | **MISSING** |

**Present:** meta.json, form4_summary.md, 10-K_2026-03-02_item7_mdna.md

**Missing:** 8-K filings, 8-K earnings press release exhibit, 10-K Item 1 - Business (business description), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
