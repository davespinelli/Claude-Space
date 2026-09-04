# Triage pack — INVA · Innoviva, Inc.

_Generated 2026-09-04 14:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** INVA · **Name:** Innoviva, Inc.
- **CIK:** 0001080014
- **SIC:** 2834 — Pharmaceutical Preparations
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/INVA

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Innoviva, Inc.
- **CIK:** 1,080,014 · **SIC:** 2834 (Pharmaceutical Preparations) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 21.35 |
| mktcap | $1.5B |
| ev | $1.2B |
| ev_ebit | 7.5x |
| fcf | $195.8M |
| fcf_yield | 12.7% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 14.0% |
| net_debt | -$311.9M |
| net_debt_ebit | -1.9x |
| cash | $570.4M |
| ltd | $258.5M |
| equity | $1.2B |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $411.3M |
| revenue_prior | $358.7M |
| rev_growth | 14.7% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $163.7M |
| net_income | n/a |
| cfo | $196.9M |
| capex | $1.1M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 14.6% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 72,245,485 |
| shares_py | 63,021,014 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -1.9% |
| r6m | -3.7% |
| off_52w_high | -11.9% |
| adv20 | $13.4M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.79 |
| r_ev_ebit | 0.84 |
| r_roic | 0.79 |
| r_rev_growth | 0.76 |
| r_buyback | 0.10 |
| score | 0.66 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q2I |
| shares_period | CY2026Q2I |
| shares_py_period | CY2025Q2I |
| capex_missing | False |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 95 |

**Screen rationale:** top-quartile FCF yield 12.7%; cheap at 7.5x EV/EBIT; high ROIC 14.0%; revenue +14.7%; net cash


## 3. Share count trend

- Shares outstanding: **72,245,485** (CY2026Q2I) vs **63,021,014** prior year (CY2025Q2I)
- Change: **14.6%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-05-18** — Item 5.02 (officer / director change or comp arrangement): On May 12, 2026, Derek Small and Mark DiPaolo Esq. tendered their resignations from the Board of Directors of Innoviva, Inc. (the "Board" and the "Company"), in order to focus on the growth of Syndeio BioSciences Inc. ("Syndeio"), where Mr. Small serves as...

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 21 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 15 |
| F | 6 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-05_2-02-results.md)

_Extraction: started at the first release heading, 'Innoviva Reports Second Quarter 2026 Financial Results; Highlights Rec'; skipped 12 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (d228097dex991.htm)

Innoviva Reports Second Quarter 2026 Financial Results; Highlights Recent Company Progress

IST achieved U.S. net product sales of $36.6 million in the second quarter, representing 26% year-over-year growth

Royalties portfolio generated $59.8 million in second quarter revenue

Launch of wholly-owned Strategic Healthcare Asset, Nortiva Bio, focused on novel extended-release drug delivery technology

BURLINGAME, Calif. – Aug 5, 2026 – Innoviva, Inc. (NASDAQ: INVA) ("Innoviva" or the "Company"), a diversified
biopharmaceutical company with a core royalties portfolio, a leading critical care and infectious disease platform known as Innoviva Specialty Therapeutics ("IST"), and a portfolio of strategic investments in healthcare assets, today
reported financial results for the second quarter ended June 30, 2026, and highlighted select corporate progress and achievements.

"Innoviva
delivered another strong quarter, supported by durable cash generation from our royalty portfolio and continued excellent commercial momentum at IST, which achieved 46% year-over-year net product sales growth, including 26% growth in U.S. sales. We
remain on track to achieve at least $150 million in IST U.S. net product sales in 2026, reflecting the differentiation of our marketed critical care and infectious disease portfolio and robust execution," said Pavel Raifeld, Chief
Executive Officer of Innoviva.

"Recently, we also advanced several growth opportunities. This quarter, we announced a commercialization and
licensing agreement with Dr. Reddy's Laboratories, expanding access to our top-performing antibiotic, XACDURO, in emerging markets. Additionally, we launched Nortiva Bio, a novel platform for
long-acting oral medicine delivery, with large upside potential."

"Overall, we have been pleased with progress across our healthcare asset
portfolio, despite market volatility. Our continued activity under the share repurchase program reflects our sustained conviction in the long-term prospects of our diversified business model — one that combines durable cash generation, strong
operating revenue growth, and value creation in high-potential strategic opportunities."

Financial Highlights for the Second Quarter of 2026

• | Total revenue: $119.6 million, representing 19% year-on-year growth compared to $100.3 million for the second quarter of 2025.

• | Royalty revenue: gross royalty revenue from Glaxo Group Limited ("GSK") remains stable at $59.8 million in the second quarter of 2026, a 2% increase compared to $58.6 million in the first quarter of 2026.

• | Net product sales: $51.8 million ($36.6 million U.S. and $15.2 million ex-U.S.), representing 46% growth compared to $35.5 million in the second quarter of 2025. U.S. net product sales primarily consisted of $21.0 million from GIAPREZA ® , $12.0 million from XACDURO ® , and $3.3 million from XERAVA ® .

• | Income from operations: $50.9 million, compared to $48.8 million for the second quarter of 2025, reflecting higher net product sales and continued operating discipline.

• | Equity and long-term investments: net unfavorable changes in fair value of equity and long-term investments totaled $161.0 million, primarily attributable to a lower share price of Armata Pharmaceuticals. Innoviva's strategic healthcare investments were valued at $669.5 million as of June 30, 2026, and consisted of $457.7 million in Armata Pharmaceuticals, $177.3 million in other strategic equity and convertible debt, and $34.5 million held by ISP Fund.

• | Net income: net loss of $83.4 million, or $1.14 basic loss per share, driven primarily by decrease in fair value of equity and long-term investments.

• | Cash and cash equivalents: Totaled $570.4 million. Royalty and net product sales receivables totaled $110.6 million as of June 30, 2026, a 25% year-on-year increase compared to $88.3 million for the second quarter of 2025.

Key Business and R&D Highlights

• | XACDURO ® (sulbactam for injection; durlobactam for injection) , co-packaged for intravenous use: a targeted antibacterial treatment for patients with hospital-acquired bacterial pneumonia and ventilator-associated bacterial pneumonia (HABP/VABP) caused by susceptible isolates of Acinetobacter baumannii-calcoaceticus complex.

• | During the second quarter, IST entered into an exclusive distribution and licensing agreement with Dr. Reddy's Laboratories Ltd., a global pharmaceutical company, for the development and commercialization of XACDURO ® in South and Central America, the Caribbean, Russia and Commonwealth of Independent States countries.

• | Strategic Healthcare Assets

• | During the second quarter, Innoviva launched Nortiva Bio (a wholly owned subsidiary), to advance the proprietary LYNX ™ long-acting oral drug delivery platform. The LYNX platform is designed to transform daily oral medicines into less frequent dosing regimens, including once-weekly or once-monthly therapies. The platform is designed to improve patient adherence, stabilize drug exposure, and enhance clinical and commercial value by enabling less frequent oral dosing.

• | Nortiva is advancing a lead once-monthly oral drug therapy development program (via support from the Gates Foundation) and building an external partnering pipeline to enable the development of long-acting oral versions of branded and generic therapies.

• | Capital Allocation

• | During the second quarter of 2026, Innoviva repurchased 1,403,247 shares for $31.4 million under its $125 million share repurchase program. Since inception, and through the end of the second quarter, the Company has repurchased 2,602,168 shares for $56.4 million, reflecting the Company's continued confidence in its intrinsic value and long-term outlook.

• | During the second quarter of 2026, Innoviva continued to support companies in its strategic healthcare asset portfolio with $55.0 million aggregate capital commitment.

- 2 -

About Innoviva

Innoviva is a diversified biopharmaceutical company with a core royalties portfolio, a leading critical care and infectious disease platform known as Innoviva
Specialty Therapeutics ("IST"), and a portfolio of strategic investments in healthcare assets. Innoviva's royalty portfolio includes respiratory assets partnered with Glaxo Group Limited ("GSK"). Innoviva is entitled to
receive royalties from GSK on sales of RELVAR ® /BREO ® ELLIPTA ® and ANORO ® ELLIPTA ® . Innoviva's critical care and infectious disease assets under the IST platform include GIAPREZA ® (angiotensin II) for increasing blood pressure in adults with septic or other distributive shock, XACDURO ® (sulbactam for injection;
durlobactam for injection), co-packaged for intravenous use for the treatment of adults with hospital-acquired and ventilator-associated bacterial pneumonia caused by susceptible strains of
Acinetobacter baumannii-calcoaceticus , XERAVA ® (eravacycline) for the treatment of complicated intra-abdominal infections in adults, ZEVTERA (ceftobiprole), an
advanced-generation cephalosporin antibiotic licensed from Basilea Pharmaceutica International Ltd, Allschwil, and NUZOLVENCE ® (zoliflodacin), approved by the FDA for the oral treatment of
uncomplicated urogenital gonorrhea in adults and pediatric patients 12 years of age and older weighing at least 35 kg. For more information about Innoviva, go to www.inva.com . For information about Innoviva Specialty Therapeutics, go to
www.innovivaspecialtytherapeutics.com .

ANORO ® , RELVAR ® and BREO ® are trademarks of the GSK group of companies. ZEVTERA is a trademark of Basilea Pharmaceutica Ltd, Allschwil.

Condensed Consolidated Balance Sheets

(in thousands)

(unaudited)

June 30, 2026 | December 31, 2025
Assets
Cash and cash equivalents | 570,388 | 550,941
Royalty and product sale receivables | 110,616 | 93,317
Inventory | 38,968 | 39,172
Prepaid expense and other current assets | 24,726 | 28,358
Current portion of ISP Fund investments | 8,668 | 15,727
Property and equipment, net | 2,133 | 1,555
Equity method and equity and long-term investments | 660,850 | 598,223
Capitalized fees | 49,226 | 56,138
Right-of-use assets | 10,377 | 10,929
Goodwill | 17,905 | 17,905
Intangible assets | 168,976 | 182,156
Other assets | 39,894 | 40,744
Total assets | 1,702,727 | 1,635,165
Liabilities and stockholders' equity
Other current liabilities | 39,431 | 43,808
Accrued interest payable | 1,618 | 1,618
Deferred revenue | 6,015 | 4,270
Convertible senior notes, due 2028, net | 258,454 | 257,731
Deferred tax liabilities, net | 36,739 | 31,793
Income tax payable, long term | 59,932 | 57,013
Other long term liabilities | 67,276 | 66,091
Stockholders' equity | 1,233,262 | 1,172,841
Total liabilities and stockholders' equity | 1,702,727 | 1,635,165

- 6 -

INNOVIVA, INC.

Cash Flows Summary

(in thousands)

(unaudited)

Six Months Ended June 30,
2026 | 2025
Net cash provided by operating activities | 87,254 | 92,690
Net cash used in investing activities | (18,256 | (1,552
Net cash provided by (used in) financing activities | (49,551 | 1,430
Net change | 19,447 | 92,568
Cash and cash equivalents at beginning of period | 550,941 | 304,964
Cash and cash equivalents at end of period | 570,388 | 397,532

- 7 -

Investors and media contact

Irwin Tendler

Head of Investor Relations

Executive Director, Corporate Development

investors.relations@inva.com

- 8 -

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-25_item7_mdna.md)

_Extraction: started at 'Results of Operations'._

Results of Operations

Net Revenue

Royalty Revenue

Total royalty revenue, net, as compared to the prior years, was as follows:

Change
Year Ended December 31, | 2025 | 2024
(In thousands) | 2025 | 2024 | 2023 | % | %
Royalties – RELVAR/BREO | 204,021 | 207,925 | 208,042 | (3,904 | (2 | )% | (117 | (0 | )%
Royalties – ANORO | 46,281 | 47,631 | 44,627 | (1,350 | (3 | )% | 3,004 | 7 | %
Total royalties | 250,302 | 255,556 | 252,669 | (5,254 | (2 | )% | 2,887 | 1 | %
Less: amortization of capitalized fees paid | (13,823 | (13,823 | (13,823 | — | * | — | *
Total net royalty revenue | 236,479 | 241,733 | 238,846 | (5,254 | (2 | )% | 2,887 | 1 | %

* Not Meaningful

Total royalty revenue, net, decreased to $236.5 million for the year ended December 31, 2025, compared to $241.7 million for the year ended December 31, 2024. The decrease in total net royalty revenue was primarily due to lower net sales driven by pricing pressures in the United States.

Total royalty revenue, net, increased to $241.7 million for the year ended December 31, 2024, compared to $238.8 million for the year ended December 31, 2023. The increase in total net royalty revenue was primarily due to the sales growth in ANORO ® ELLIPTA ® .

Net Product Sales

Total product sales, net, as compared to the prior years, was as follows:

Change
Year Ended December 31, | 2025 | 2024
(In thousands) | 2025 | 2024 | 2023 | % | %
U.S.
GIAPREZA ® | 71,831 | 53,410 | 40,761 | 18,421 | 34 | % | 12,649 | 31 | %
XERAVA ® | 13,341 | 12,777 | 12,441 | 564 | 4 | % | 336 | 3 | %
XACDURO ® | 33,448 | 14,668 | 2,003 | 18,780 | 128 | % | 12,665 | *
ZEVTERA ® | 610 | — | — | 610 | * | — | *
Total U.S. | 119,230 | 80,855 | 55,205 | 38,375 | 47 | % | 25,650 | 46 | %
Rest of the world
GIAPREZA ® | 1,780 | 1,627 | 533 | 153 | 9 | % | 1,094 | 205 | %
XERAVA ® | 10,175 | 8,608 | 4,879 | 1,567 | 18 | % | 3,729 | 76 | %
XACDURO ® | 40,945 | 6,402 | — | 34,543 | * | 6,402 | *
Total rest of the world | 52,900 | 16,637 | 5,412 | 36,263 | 218 | % | 11,225 | 207 | %
Total net product sales | 172,130 | 97,492 | 60,617 | 74,638 | 77 | % | 36,875 | 61 | %

* Not Meaningful

Our net product sales increased during the periods presented, driven by higher sales volume resulting from our strategic commercialization efforts and dedication to delivering our critical care products to healthcare systems. The increase in XACDURO ® ex-U.S. product sales is attributable mainly to product sales under an interim supply agreement with Zai Lab, which is billed at cost.

License and Other Revenue

License and other revenue, as compared to the prior years, were as follows:

Change
Twelve Months Ended December 31, | 2025 | 2024
(In thousands) | 2025 | 2024 | 2023 | % | %
License and other revenue | 2,719 | 19,486 | 11,000 | (16,767 | (86 | )% | 8,486 | 77 | %

License revenue for the year ended December 31, 2025 was derived primarily from the continuing activities related to the Amended Zai Agreement and the Zai Manufacturing Stage Transfer Agreement, which both commenced in 2024.

We recognized $8.0 million in license and other revenue for the year ended December 31, 2024 as a result of the achievement of a regulatory milestone under our license agreement with Zai Lab. We also recognized $8.1 million and $3.4 million in license and other revenue under the aforementioned Amended Zai Agreement and Zai Manufacturing Stage Transfer Agreement, respectively.

We recognized license and other revenue of $8.0 million and $3.0 million for the year ended December 31, 2023 as a result of achievement of regulatory milestones under our license agreements with Everest and Zai Lab, respectively.

Cost of Products Sold

Cost of products sold, as compared to the prior years, were as follows:

Change
Year Ended December 31, | 2025 | 2024
(In thousands) | 2025 | 2024 | 2023 | % | %
Cost of product sold | 77,384 | 36,598 | 41,040 | 40,786 | 111 | % | (4,442 | (11 | )%

The cost of products sold also includes the inventory step-up value from the acquisition of La Jolla, which is recorded upon the sale of such inventory. The step-up value included above amounted to $4.8 million, $13.8 million and $27.2 million for the years ended December 31, 2025, 2024 and 2023, respectively. Our cost of products sold increased during the year ended December 31, 2025 presented, driven by higher product sales volume. As of December 31, 2025, our total inventory included the remaining net fair value adjustments resulting from the acquisition of La Jolla of approximately $3.4 million, which will be recognized as cost of products sold when sales occur in future periods.

Research & Development

Research and development expenses, as compared to the prior years, were as follows:

Change
Year Ended December 31, | 2025 | 2024
(In thousands) | 2025 | 2024 | 2023 | % | %
Research and development | 30,604 | 13,654 | 33,922 | 16,950 | 124 | % | (20,268 | (60 | )%

Research and development expenses consisted of the following:

Change
Year Ended December 31, | 2025 | 2024
(In thousands) | 2025 | 2024 | 2023 | % | %
External services | 15,704 | 7,408 | 20,051 | 8,296 | 112 | % | (12,643 | (63 | )%
Compensation and related personnel costs | 5,284 | 4,948 | 10,081 | 336 | 7 | % | (5,133 | (51 | )%
Acquired IPR&D | 9,368 | — | — | 9,368 | * | — | *
Facilities related | 53 | 733 | 2,483 | (680 | (93 | )% | (1,750 | (70 | )%
Other | 195 | 565 | 1,307 | (370 | (65 | )% | (742 | (57 | )%
Total research and development expenses | 30,604 | 13,654 | 33,922 | 16,950 | 124 | % | (20,268 | (60 | )%

Research and development expenses for the year ended December 31, 2025 included $9.4 million of allocated cost for acquired in-process research and development ("IPR&D") related to the Lynx™ long-acting drug delivery platform as discussed in Note 14, "Asset Acquisition", in the Consolidated Financial Statements. During the year ended December 31, 2025, we also incurred costs related to the continued advancement of NUZOLVENCE ® . Research and development expenses for the year ended December 31, 2024 were mainly attributable to post marketing commitments required by the FDA and ongoing product development. Research and development expenses for the year ended December 31, 2023 were mainly attributable to our product development efforts for XACDURO ® .

Selling, General & Administrative

Selling, general and administrative expenses, as compared to the prior years, were as follows:

Change
Year Ended December 31, | 2025 | 2024
(In thousands) | 2025 | 2024 | 2023 | % | %
Selling, general and administrative | 113,318 | 115,690 | 98,232 | (2,372 | (2 | )% | 17,458 | 18 | %

Our selling, general and administrative expenses are primarily attributable to efforts to promote our marketed critical care products and drive revenue, maintain regulatory compliance, and support essential administrative functions. Selling, general and administrative expenses decreased by $2.4 million for the year ended December 31, 2025, compared to the year ended December 31, 2024, during which included incremental expenditures related to the September 2023 commercial launch of XACDURO ® .

Selling, general and administrative expenses increased by $17.5 million for the year ended December 31, 2024, compared to the year ended December 31, 2023. The increase was mainly due to the reallocation of resources from the research and development function, focusing on regulatory compliance since May 2023 after the FDA approval of XACDURO ® , and enhanced commercial strategies resulting from our ongoing efforts to promote and deliver our marketed critical care products.

Interest and Dividend Income and Other Expense, Net

Interest and dividend income and other expense, net, as compared to the prior years, were as follows:

Change
Year Ended December 31, | 2025 | 2024
(In thousands) | 2025 | 2024 | 2023 | % | %
Interest and dividend income | 21,086 | 19,141 | 15,818 | 1,945 | 10 | % | 3,323 | 21 | %
Other expense, net | (2,864 | (2,997 | (4,969 | 133 | (4 | )% | 1,972 | (40 | )%

Interest and dividend income increased for the years ended December 31, 2025 and 2024, due to higher average balances of our cash equivalents, money market funds and other interest-bearing investments.

Other expense, net, primarily consisted of expenses incurred by ISP Fund LP.

Interest Expense

Interest expense, as compared to the prior years, was as follows:

Change
Year Ended December 31, | 2025 | 2024
(In thousands) | 2025 | 2024 | 2023 | % | %
Interest expense | (16,698 | (22,209 | (19,157 | 5,511 | (25 | )% | (3,052 | 16 | %

The interest expense for the periods presented included the contractual interest expense and the amortization of debt issuance costs for our 2025 Notes and 2028 Notes, as well as effective interest expense on our deferred royalty obligation related to GIAPREZA ® . The decrease for the year ended December 31, 2025 compared to the year ended December 31, 2024 was mainly due to lower interest expense on our deferred royalty obligation as a result of higher sales performance of GIAPREZA ® , as well as the settlement of our 2025 Notes in August 2025. The year-over-year increase from 2023 to 2024 was primarily due to a higher effective interest rate on our deferred royalty obligation.

Changes in Fair Values of Equity Method Investments and Equity and Long-Term Investments

Changes in fair values of equity method investments and equity and long-term investments, net, as compared to the prior years, were as follows:

Change
Year Ended December 31, | 2025 | 2024
(In thousands) | 2025 | 2024 | 2023 | % | %
Changes in fair values of equity method investments, net | 141,433 | (64,253 | 77,392 | 205,686 | * | (141,645 | *
Changes in fair values of equity and long-term investments, net | 20,160 | (59,161 | 11,129 | 79,321 | * | (70,290 | *

* Not Meaningful

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-25_item1_business.md)

ITEM 1. BUSINESS

Overview

Innoviva, Inc. ("Innoviva", the "Company", the "Registrant" or "we" and other similar pronouns) is a diversified biopharmaceutical company with a core royalties portfolio, a leading critical care and infectious disease platform known as Innoviva Specialty Therapeutics ("IST"), and a portfolio of strategic healthcare assets.

Our royalty portfolio contains respiratory assets partnered with Glaxo Group Limited ("GSK"), including RELVAR ® /BREO ® ELLIPTA ® (fluticasone furoate/vilanterol, "FF/VI") and ANORO ® ELLIPTA ® (umeclidinium bromide/vilanterol, "UMEC/VI"). Under the Long-Acting Beta-2 Agonist ("LABA") Collaboration Agreement, Innoviva is entitled to receive royalties from GSK on sales of RELVAR ® /BREO ® ELLIPTA ® as follows: 15% on the first $3.0 billion of annual global net sales and 5% for all annual global net sales above $3.0 billion; and royalties from the sales of ANORO ® ELLIPTA ® , which tier upward at a range from 6.5% to 10%.

Our wholly owned, robust critical care and infectious disease operating platform with a hospital focus, is anchored by five differentiated approved, commercial and marketed products:

•
GIAPREZA ® (angiotensin II) for increasing blood pressure in adults with septic or other distributive shock;

•
XACDURO ® (sulbactam for injection; durlobactam for injection), co-packaged for intravenous use for the treatment of hospital-acquired and ventilator-associated bacterial pneumonia caused by Acinetobacter , commercially launched in 2023 ;

•
XERAVA ® (eravacycline) for the treatment of complicated intra-abdominal infections in adults;

•
ZEVTERA ® (ceftobiprole), an advanced-generation cephalosporin antibiotic for the treatment of staphylococcus aureus bacteremia , including those with right-sided endocarditis, acute bacterial skin and skin structure infections, and community-acquired bacterial pneumonia, licensed from Basilea Pharmaceutica Ltd, Allschwil (SIX: BSLN) ("Basilea") for U.S. commercialization and commercially launched in the third quarter of 2025; and

•
NUZOLVENCE ® (formerly known as zoliflodacin), approved by the FDA on December 12, 2025, for the treatment of uncomplicated urogenital gonorrhea in adults and adolescents.

In addition, we own other strategic healthcare assets, such as a significant stake in Armata Pharmaceuticals, Inc., a leader in development of bacteriophages with potential use across a range of infectious and other serious diseases. We also have economic interests in other healthcare companies through our portfolio approach.

Our disciplined focus on deploying capital in areas of significant unmet medical need with high value creation potential has driven a meaningful transformation of our company over the years from a pure-play royalty business to a diversified biopharmaceutical company with a strong, fast-growing, differentiated operating platform and multiple other assets with significant promise. We believe we are well-positioned to deliver significant long-term shareholder value.

Our headquarters are located at 1350 Old Bayshore Highway, Suite 400, Burlingame, CA 94010. The Company was incorporated in Delaware in November 1996 and commenced operations in May 1997 under Advanced Medicine, Inc. The Company changed its name to Theravance, Inc. in April 2002 and to Innoviva, Inc. in January 2016.

Our Strategy

Our corporate strategy is currently focused on increasing shareholder value by, among other things, maximizing the potential value of our respiratory assets partnered with GSK, growing our critical care and infectious disease platform, efficiently allocating capital, and optimizing our operations. We continue to diversify our royalty management business by actively pursuing opportunistic investments in, and acquisitions of, promising assets in the healthcare industry to enhance the returns on our capital.

Our Royalty Product Portfolio

Our Relationship with GSK

LABA Collaboration

In November 2002, we entered into our LABA Collaboration Agreement with GSK to develop and commercialize once‑daily products for the treatment of chronic obstructive pulmonary disease ("COPD") and asthma. The collaboration has developed three combination products, two of which we still retain rights in. Those two are as follows:

•
RELVAR ® /BREO ® ELLIPTA ® ("FF/VI") (BREO ® ELLIPTA ® is the proprietary name in the U.S. and Canada and RELVAR ® ELLIPTA ® is the proprietary name outside the U.S. and Canada), a once-daily combination medicine consisting of a LABA, vilanterol ("VI"), and an inhaled corticosteroid ("ICS"), fluticasone furoate ("FF"), and,

•
ANORO ® ELLIPTA ® ("UMEC/VI"), a once-daily medicine combining a long-acting muscarinic antagonist ("LAMA"), umeclidinium bromide ("UMEC"), with a LABA, VI.

As a result of the launch and approval of RELVAR ® /BREO ® ELLIPTA ® and ANORO ® ELLIPTA ® in the U.S., Japan and Europe, in accordance with the LABA Collaboration Agreement, we paid milestone fees to GSK totaling $220.0 million during the year ended December 31, 2014. The milestone fees paid to GSK were recognized as capitalized fees paid, which are being amortized over their estimated useful lives commencing upon the commercial launch of the products.

Competition

We anticipate that RELVAR ® /BREO ® ELLIPTA ® (FF/VI) and ANORO ® ELLIPTA ® (UMEC/VI) will compete with a number of approved bronchodilator drugs alone or in combination, including each other and drug candidates under development that are designed to treat asthma and COPD. These include but are not limited to:

•
Advair ® /Seretide™ Diskus ® /HFA ® (salmeterol and fluticasone propionate as a combination) marketed by GSK

•
Symbicort ® (formoterol and budesonide as a combination) marketed by AstraZeneca

•
AirDuo Respiclick ® (salmeterol and fluticasone propionate), a non-substitutable generic version of Advair, marketed by TEVA

•
Spiriva ® Handihaler ® and Spiriva ® Respimat ® (tiotropium) marketed by Boehringer Ingelheim

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-25_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-25_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-25_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-05_2-02-results.md, 10-K_2026-02-25_item7_mdna.md, 10-K_2026-02-25_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
