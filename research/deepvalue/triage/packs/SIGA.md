# Triage pack — SIGA · SIGA TECHNOLOGIES INC

_Generated 2026-09-04 17:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** SIGA · **Name:** SIGA TECHNOLOGIES INC
- **CIK:** 0001010086
- **SIC:** 2834 — Pharmaceutical Preparations
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/SIGA

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** SIGA TECHNOLOGIES INC
- **CIK:** 1,010,086 · **SIC:** 2834 (Pharmaceutical Preparations) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 3.23 |
| mktcap | $232.1M |
| ev | $114.5M |
| ev_ebit | 4.8x |
| fcf | $43.5M |
| fcf_yield | 18.7% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 39.3% |
| net_debt | -$117.6M |
| net_debt_ebit | -5.0x |
| cash | $117.6M |
| ltd | $0.00 |
| equity | $165.3M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $94.6M |
| revenue_prior | $138.7M |
| rev_growth | -31.8% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $23.7M |
| net_income | $23.3M |
| cfo | $43.5M |
| capex | n/a |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 0.3% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 71,849,716 |
| shares_py | 71,606,003 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -58.6% |
| r6m | -41.5% |
| off_52w_high | -61.0% |
| adv20 | $2.2M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.87 |
| r_ev_ebit | 0.94 |
| r_roic | 0.96 |
| r_rev_growth | 0.01 |
| r_buyback | 0.60 |
| score | 0.58 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q2I |
| shares_period | CY2026Q2I |
| shares_py_period | CY2025Q2I |
| capex_missing | True |
| ltd_missing | True |

**Other screen columns**

| metric | value |
|---|---|
| rank | 172 |

**Screen rationale:** top-quartile FCF yield 18.7%; cheap at 4.8x EV/EBIT; high ROIC 39.3%; debt data missing (net cash unverified); WARNING 6m return below -40%


## 3. Share count trend

- Shares outstanding: **71,849,716** (CY2026Q2I) vs **71,606,003** prior year (CY2025Q2I)
- Change: **0.3%** — roughly flat
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-06-10** — Item 5.02 (officer / director change or comp arrangement): SIGA Technologies, Inc. (the "Company") held its 2026 annual meeting of stockholders on June 9, 2026 (the "Annual Meeting").

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 47 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 11 |
| D | 7 |
| F | 5 |
| M | 24 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'SIGA Reports Financial Results for Three and Six Months Ended June 30,'; skipped 8 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99.1 - EXHIBIT 99.1 (ef20079446_ex99-1.htm)

SIGA Reports Financial Results for Three and Six Months Ended June 30, 2026

• | $37 Million of TPOXX Sales Generated in the Second Quarter

• | Corporate Update Conference Call Today at 4:30 PM ET

NEW YORK, August 6, 2026 (GLOBENEWSWIRE) -- SIGA Technologies, Inc. (SIGA) (Nasdaq: SIGA), a
commercial-stage pharmaceutical company, today reported financial results for the three and six months ended June 30, 2026.

"In the second quarter, we delivered approximately $37 million of TPOXX to three customers: $24 million of IV TPOXX to the U.S. strategic national
stockpile and $13 million of oral TPOXX to two international customers," stated Diem Nguyen, Chief Executive Officer. "With product deliveries across the U.S., Europe, and the Asia- Pacific region, spanning multiple formulations, SIGA continues to
execute its long-term plan of selling TPOXX across a diverse range of regions and customers."

Summary Financial Results

($ in millions, except per share amounts) | Three Months Ended June 30 | Six Months Ended June 30
2026 | 2025 | 2026 | 2025
Product sales (1) | 37.9 | 79.1 | 41.4 | 84.9
Total revenues (2) | 41.0 | 81.1 | 47.2 | 88.2
Operating income (3) (4) | 13.9 | 45.7 | 8.6 | 43.4
Income before income taxes (3) | 14.9 | 47.3 | 10.8 | 46.7
Net income | 12.5 | 35.5 | 9.0 | 35.1
Diluted income per share | 0.17 | 0.49 | 0.13 | 0.49

(1) | Includes supportive services related to product sales.

(2) | Includes research and development revenues.

(3) | Operating income excludes, and income before income taxes includes, other income. Both line items exclude the impact of income taxes.

(4) | Differences in operating income margin between periods reflect different product mixes in those periods.

Key Business and Operational Activity:

• | In the second quarter of 2026, the Company delivered approximately $13 million of oral TPOXX to two international customers.

• | In the second quarter of 2026, the Company delivered approximately $24 million of IV TPOXX to the U.S. strategic national stockpile under the 19C contract. These deliveries completed the last procurement order under the 19C contract.

Capital Management Activity

■ | On March 26, 2026, a special cash dividend of $0.60 per share was declared, and was paid on April 23, 2026, to shareholders of record at the close of business on April 7, 2026.

Conference Call and Webcast

SIGA will host a conference call and webcast to provide a business update today, Thursday, August 6,
2026, at 4:30 P.M. ET.

Participants may access the call by dialing 1-800-717-1738 for
domestic callers or 1-646-307-1865 for international callers. A live webcast of the call will also be available on the Company's website at www.siga.com in the Investor Relations section of the website . Please log in approximately 5-10 minutes prior to the scheduled start time.

A replay of the call will be available for
two weeks by dialing 1-844-512-2921 for domestic callers or 1-412-317-6671 for international callers and using Conference ID: 11157253 . The archived webcast will be available in the Investor Relations section of the Company's website.

ABOUT SIGA

SIGA is a commercial-stage pharmaceutical company and leader in global health focused on the development
of innovative medicines to treat and prevent infectious diseases. With a primary focus on smallpox, we are dedicated to protecting humanity against the world's most severe infectious diseases, including those that occur naturally, accidentally,
or intentionally. Through partnerships with governments and public health agencies, we work to build a healthier and safer world by providing essential countermeasures against these global health threats. For more information about SIGA, visit
www.siga.com.

June 30, 2026 | December 31, 2025
ASSETS
Current assets
Cash and cash equivalents | 117,584,444 | 154,966,414
Accounts receivable | 7,170,229 | 3,263,736
Inventory | 41,110,808 | 49,054,873
Prepaid expenses and other current assets | 4,512,301 | 5,571,841
Total current assets | 170,377,782 | 212,856,864
Property, plant and equipment, net | 1,530,954 | 1,090,824
Deferred tax asset, net | 2,789,666 | 4,428,519
Goodwill | 898,334 | 898,334
Other assets | 140,050 | 192,893
Total assets | 175,736,786 | 219,467,434
LIABILITIES AND STOCKHOLDERS' EQUITY
Current liabilities
Accounts payable | 909,834 | 824,522
Accrued expenses and other current liabilities | 6,907,137 | 6,520,057
Deferred IV TPOXX® revenue | — | 10,240,000
Income tax payable | 28,335 | 408,000
Total current liabilities | 7,845,306 | 17,992,579
Other liabilities | 2,600,845 | 2,653,283
Total liabilities | 10,446,151 | 20,645,862
Commitments and contingencies
Stockholders' equity
Common stock ($.0001 par value, 600,000,000 shares authorized, 71,844,042 and 71,611,302, issued and outstanding at June 30, 2026 and December 31, 2025, respectively) | 7,184 | 7,161
Additional paid-in capital | 243,262,409 | 241,885,214
Accumulated deficit | (77,978,958 | (43,070,803
Total stockholders' equity | 165,290,635 | 198,821,572
Total liabilities and stockholders' equity | 175,736,786 | 219,467,434

SIGA TECHNOLOGIES, INC.

CONDENSED CONSOLIDATED STATEMENTS OF OPERATIONS AND COMPREHENSIVE INCOME (UNAUDITED)

Three Months Ended June 30, | Six Months Ended June 30,
2026 | 2025 | 2026 | 2025
Revenues
Product sales and supportive services | 37,870,335 | 79,124,860 | 41,408,212 | 84,946,107
Research and development | 3,131,918 | 1,995,144 | 5,836,622 | 3,214,711
Total revenues | 41,002,253 | 81,120,004 | 47,244,834 | 88,160,818
Operating expenses
Cost of sales and supportive services | 17,561,185 | 25,554,462 | 20,502,069 | 25,712,200
Selling, general and administrative | 5,148,992 | 5,487,576 | 9,822,005 | 11,163,238
Research and development | 4,386,498 | 4,398,097 | 8,336,344 | 7,860,910
Total operating expenses | 27,096,675 | 35,440,135 | 38,660,418 | 44,736,348
Operating income | 13,905,578 | 45,679,869 | 8,584,416 | 43,424,470
Other income, net | 946,898 | 1,592,304 | 2,224,378 | 3,277,288
Income before income taxes | 14,852,476 | 47,272,173 | 10,808,794 | 46,701,758
Provision for income taxes | (2,389,042 | (11,789,070 | (1,799,610 | (11,626,878
Net and comprehensive income | 12,463,434 | 35,483,103 | 9,009,184 | 35,074,880
Basic income per share | 0.17 | 0.50 | 0.13 | 0.49
Diluted income per share | 0.17 | 0.49 | 0.13 | 0.49
Weighted average shares outstanding: basic | 71,752,539 | 71,465,521 | 71,701,531 | 71,446,629
Weighted average shares outstanding: diluted | 71,883,798 | 71,748,888 | 71,998,573 | 71,678,838

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-10_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

SIGA Technologies, Inc. ("SIGA" or the "Company") is a commercial-stage pharmaceutical company. The Company sells its lead product, TPOXX® ("oral TPOXX®," also known as "tecovirimat," "Tecovirimat SIGA," or "TEPOXX (tecovirimat)" in certain international markets), to the U.S. Government and international governments (including government affiliated entities). In certain international markets, the Company may sell TPOXX® through a distributor. Additionally, the Company sells the intravenous formulation of TPOXX® ("IV TPOXX®") to the U.S. Government.

TPOXX® is an antiviral drug for the treatment of human smallpox disease caused by variola virus. On July 13, 2018, the United States Food & Drug Administration ("FDA") approved oral TPOXX® for the treatment of smallpox. The Company has been delivering oral TPOXX® to the U.S. Strategic National Stockpile ("Strategic Stockpile") since 2013.

On May 18, 2022 the FDA approved IV TPOXX® for the treatment of smallpox.

In addition to being approved by the FDA, oral TPOXX® (tecovirimat) has received regulatory approval from the European Medicines Agency ("EMA"), Health Canada, the Medicines and Healthcare Products Regulatory Agency ("MHRA") of the United Kingdom, and the Japanese Pharmaceuticals and Medical Devices Agency ("PMDA"). The EMA, MHRA and PMDA approved oral TPOXX® for the treatment of smallpox, monkeypox ("mpox"), cowpox, and vaccinia complications following vaccination against smallpox. Health Canada approved TPOXX® for the treatment of smallpox.

TPOXX® was authorized under "exceptional circumstances" by the EMA and the MHRA, under the brand name Tecovirimat-SIGA. These regulators granted marketing authorizations under "exceptional circumstances" because it was not possible to obtain complete efficacy and safety information about the product due to the rarity of smallpox and other orthopoxviruses and because ethical considerations prevented conducting the necessary clinical studies. The Tecovirimat-SIGA marketing authorizations under "exceptional circumstances" are subject to certain specific obligations to gather additional data post-approval to help confirm the product's safety and efficacy. All "exceptional circumstances" marketing authorizations are subject to annual reassessments that consider whether data generated pursuant to the specific obligations continue to confirm its positive benefit-risk profile. These annual reassessments determine whether the product's marketing authorization should be maintained, changed, suspended, or withdrawn based on its benefit-risk profile.

On July 24, 2025, the EMA's Committee for Medicinal Products for Human Use (CHMP) closed its third annual reassessment for Tecovirimat-SIGA and initiated a referral procedure for the product following questions over its effectiveness in the treatment of mpox. These questions were raised following receipt of results from certain non-SIGA sponsored clinical trials evaluating tecovirimat as a potential mpox treatment including the PALM007 and STOMP clinical trials. In the referral procedure, CHMP reviewed all available data on the safety and efficacy of Tecovirimat-SIGA for all its authorized indications in order to make a recommendation to the European Commission whether the marketing authorization should be maintained, modified, suspended or withdrawn. The CHMP is expected to meet in March to issue its recommendation. We expect the CHMP will confirm the positive benefit-risk balance of Tecovirimat-SIGA as a treatment for smallpox, cowpox, and vaccinia complications, and maintain those indications in the product label. Regarding mpox, based on the results of the mpox clinical trials, we expect the CHMP will recommend withdrawal of the mpox indication. In the UK, Tecovirimat-SIGA is undergoing an annual reassessment by the MHRA. This reassessment, which is ongoing, is substantially similar to the EMA's annual reassessment process and could result in a similar outcome.

With respect to the regulatory approvals by the EMA, PMDA, MHRA and Health Canada, oral tecovirimat represents the same formulation approved by the FDA in July 2018 under the brand name TPOXX®.

In connection with a potential FDA label expansion of oral TPOXX® for an indication covering smallpox post-exposure prophylaxis ("PEP"), the Company has completed an immunogenicity trial and an expanded safety trial. The timing of a potential submission of a supplemental New Drug Application to the FDA ("Supplemental NDA") for a smallpox PEP indication for oral TPOXX® will be based on the results of ongoing sample analyses from the immunogenicity trial; the Company is currently targeting a Supplemental NDA submission within the next twelve months.

Macroeconomic Environment

Future macroeconomic volatility, including changes to and uncertainty regarding tariffs and trade policies, could cause cost increases resulting in an adverse effect on the Company's operating results. The Company's supply chain was designed to lessen the impact of macroeconomic volatility such as through development of a U.S. domestic supply chain including U.S. production of API and finished product, and minimal reliance on ex-U.S. components for API and oral TPOXX®.

With respect to IV TPOXX®, tariff activity or other trading restrictions involving the U.S. and Europe may materially increase raw material costs for IV TPOXX® and, in turn, may materially increase IV TPOXX® overall manufacturing costs.

Procurement Contracts with the U.S. Government

19C BARDA Contract

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations for the Years ended December 31, 2025 and 2024

Revenues from product sales and supportive services for the years ended December 31, 2025 and 2024 were $88.0 million and $133.3 million, respectively. Such revenues for the year ended December 31, 2025 include $53.3 million of oral TPOXX® sales and $25.8 million of IV TPOXX® sales to the U.S. Government under the 19C BARDA Contract; $5.8 million of oral TPOXX® sales to one international country and $3.1 million of supportive services. Such revenues for the year ended December 31, 2024 include $73.9 million of oral TPOXX® sales and $26.2 million of IV TPOXX® sales to the U.S. Government under the 19C BARDA Contract; $23.0 million related to international sales of oral TPOXX®; and approximately $10.1 million of oral TPOXX® sales to the DoD.

Revenues from research and development activities for the years ended December 31, 2025 and 2024, were $6.5 million and $5.4 million, respectively. The revenues for the years ended December 31, 2025 and 2024, were mostly earned in connection with performance of research and development activities under the 19C BARDA Contract. The increase of $1.1 million of revenue is primarily related to an increase in reimbursable activities under the 19C BARDA Contract.

Cost of sales and supportive services for the years ended December 31, 2025 and 2024 were $29.7 million and $31.3 million, respectively. Such costs in 2025 were primarily associated with the manufacture and delivery of courses of oral and IV TPOXX® to the U.S. Government under the 19C BARDA Contract. Such costs in 2024 were primarily associated with the manufacture and delivery of oral TPOXX® courses to the U.S. Government, DoD and various international customers as well as the manufacture and delivery of IV TPOXX® courses to the U.S. Government.

Selling, general and administrative expenses for the years ended December 31, 2025 and 2024 were $21.2 million and $25.1 million, respectively. The net decrease of approximately $3.9 million primarily reflects a decrease in international promotion fees related to a combination of the amendment to the International Promotion Agreement with Meridian and lower international activity in 2025, as well as lower professional service and consulting costs, in addition to lower compensation expense associated with the nonrecurrence in 2025 of certain one-time payments and equity grants that occurred in 2024 in connection with new hires. Such decreases are partially offset by an increase in business development costs.

Research and development expenses were $20.0 million for the year ended December 31, 2025, an increase of approximately $7.7 million from the $12.3 million incurred during the year ended December 31, 2024. The expense increase is primarily attributable to an increase in self-funded research and development activity, as well as higher expenses for the implementation of information technology enhancements, higher compensation expense in connection with an increase in headcount, and an increase in the usage of regulatory and related consultants.

Other income, net for the years ended December 31, 2025 and 2024 was $6.7 million and $6.1 million, respectively. These amounts reflect interest income earned on cash and cash equivalents.

For the year ended December 31, 2025, we recognized a tax provision of $7.1 million on pre-tax income of $30.4 million. Our effective tax rate for the year ended December 31, 2025 was 23.4% and differs from the statutory rate of 21% primarily as a result of non-deductible executive compensation under IRC Section 162(m), and state and local taxes.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-10_item1_business.md)

Item 1. Business

Overview

SIGA Technologies, Inc. is referred to throughout this report as "SIGA," "the Company," "we" or "us."

We are a commercial-stage pharmaceutical company. The Company sells its lead product, TPOXX® ("oral TPOXX®," also known as "tecovirimat," "Tecovirimat-SIGA," or "TEPOXX (tecovirimat)" in certain international markets), to the U.S. Government and international governments (including government affiliated entities). In certain international markets, the Company may sell TPOXX® through a distributor. Additionally, the Company sells the intravenous formulation of TPOXX® ("IV TPOXX®") to the U.S. Government.

TPOXX® is an antiviral drug for the treatment of human smallpox disease caused by variola virus. On July 13, 2018, the United States Food & Drug Administration ("FDA") approved the oral formulation of TPOXX® for the treatment of smallpox. The Company has been delivering oral TPOXX® to the U.S. Strategic National Stockpile ("Strategic Stockpile") since 2013.

On May 18, 2022, the FDA approved IV TPOXX® for the treatment of smallpox.

In addition to being approved by the FDA, oral TPOXX® (tecovirimat) has received regulatory approval from the European Medicines Agency ("EMA"), Health Canada, the Medicines and Healthcare Products Regulatory Agency ("MHRA") of the United Kingdom, and the Japanese Pharmaceuticals and Medical Devices Agency ("PMDA"). The EMA, MHRA and PMDA approved oral TPOXX® for the treatment of smallpox, monkeypox ("mpox"), cowpox, and vaccinia complications following vaccination against smallpox. Health Canada approved TPOXX® for the treatment of smallpox.

TPOXX® was authorized under "exceptional circumstances" by the EMA and the MHRA, under the brand name Tecovirimat-SIGA. These regulators granted marketing authorizations under "exceptional circumstances" because it was not possible to obtain complete efficacy and safety information about the product due to the rarity of smallpox and other orthopoxviruses and because ethical considerations prevented conducting the necessary clinical studies. The Tecovirimat-SIGA marketing authorizations under "exceptional circumstances" are subject to certain specific obligations to gather additional data post-approval to help confirm the product's safety and efficacy. All "exceptional circumstances" marketing authorizations are subject to annual reassessments that consider whether data generated pursuant to the specific obligations continue to confirm its positive benefit-risk profile. These annual reassessments determine whether the product's marketing authorization should be maintained, changed, suspended, or withdrawn based on its benefit-risk profile.

On July 24, 2025, the EMA's Committee for Medicinal Products for Human Use (CHMP) closed its third annual reassessment for Tecovirimat-SIGA and initiated a referral procedure for the product following questions over its effectiveness in the treatment of mpox. These questions were raised following receipt of results from certain non-SIGA sponsored clinical trials evaluating tecovirimat as a potential mpox treatment including the PALM007 and STOMP clinical trials. In the referral procedure, CHMP reviewed all available data on the safety and efficacy of Tecovirimat-SIGA for all its authorized indications in order to make a recommendation to the European Commission whether the marketing authorization should be maintained, modified, suspended or withdrawn. The CHMP is expected to meet in March to issue its recommendation. We expect the CHMP will confirm the positive benefit-risk balance of Tecovirimat-SIGA as a treatment for smallpox, cowpox, and vaccinia complications, and maintain those indications in the product label. Regarding mpox, based on the results of the mpox clinical trials, we expect the CHMP will recommend withdrawal of the mpox indication. In the UK, Tecovirimat-SIGA is undergoing an annual reassessment by the MHRA. This reassessment, which is ongoing, is substantially similar to the EMA's annual reassessment process and could result in a similar outcome.

With respect to the regulatory approvals by the EMA, PMDA, MHRA and Health Canada, oral tecovirimat represents the same formulation approved by the FDA in July 2018 under the brand name TPOXX®.

In connection with a potential FDA label expansion of oral TPOXX® for an indication covering smallpox post-exposure prophylaxis ("PEP"), the Company has completed an immunogenicity trial and an expanded safety trial. The timing of a potential submission of a supplemental New Drug Application to the FDA ("Supplemental NDA") for a smallpox PEP indication for oral TPOXX® will be based on the results of ongoing sample analyses from the immunogenicity trial; the Company is currently targeting a Supplemental NDA submission within the next twelve months.

Macroeconomic Environment

Future macroeconomic volatility, including changes to and uncertainty regarding tariffs and trade policies, could cause cost increases resulting in an adverse effect on the Company's operating results. The Company's supply chain was designed to lessen the impact of macroeconomic volatility such as through development of a U.S. domestic supply chain including U.S. production of API and finished product, and minimal reliance on ex-U.S. components for API and oral TPOXX®.

With respect to IV TPOXX®, tariff activity or other trading restrictions involving the U.S. and Europe may materially increase raw material costs for IV TPOXX® and, in turn, may materially increase IV TPOXX® overall manufacturing costs.

Procurement Contracts with the U.S. Government

19C BARDA Contract

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-10_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-10_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-10_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-03-10_item7_mdna.md, 10-K_2026-03-10_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
