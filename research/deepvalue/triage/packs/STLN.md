# Triage pack — STLN · Starling Oncology, Inc.

_Generated 2026-09-05 01:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** STLN · **Name:** Starling Oncology, Inc.
- **CIK:** 0001799191
- **SIC:** 8011 — Services-Offices & Clinics of  Doctors of  Medicine
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq, OTC, Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/STLN

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Starling Oncology, Inc.
- **CIK:** 1,799,191 · **SIC:** 8011 (Services-Offices & Clinics of  Doctors of  Medicine) · **Exchange:** Nasdaq,OTC,Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

> **EARNINGS QUALITY FLAG — one-off items likely.**
> net income exceeds revenue; net income more than 3x operating income.
> Reported net income is not supported by the operating engine that is supposed to produce it (typical causes: gains on sale, legal settlements, deferred-tax valuation-allowance releases, bargain-purchase gains). Reconcile net income to operating income in the earnings release (section 7) before treating any earnings-based metric here as repeatable.

**Valuation**

| metric | value |
|---|---|
| price | 5.97 |
| mktcap | $608.4M |
| ev | $647.2M |
| ev_ebit | n/a |
| fcf | -$27.8M |
| fcf_yield | -4.6% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -205.7% |
| net_debt | $38.8M |
| net_debt_ebit | n/a |
| cash | $41.1M |
| ltd | $79.9M |
| equity | -$24.9M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $502.7M |
| revenue_prior | $393.4M |
| rev_growth | 27.8% |
| rev_growth_note | n/a |
| eq_flag | net income exceeds revenue; net income more than 3x operating income |
| ebit | -$36.1M |
| net_income | $60.6B |
| cfo | -$24.6M |
| capex | $3.2M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 9.0% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 101,916,115 |
| shares_py | 93,504,767 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 55.7% |
| r6m | 109.5% |
| off_52w_high | -10.4% |
| adv20 | $9.6M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.12 |
| r_ev_ebit | 0.00 |
| r_roic | 0.00 |
| r_rev_growth | 0.88 |
| r_buyback | 0.14 |
| score | 0.28 |

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
| rank | 426 |

**Screen rationale:** revenue +27.8%; 12-1 momentum 55.7%; EARNINGS QUALITY: net income exceeds revenue; net income more than 3x operating income — one-off items likely


## 3. Share count trend

- Shares outstanding: **101,916,115** (CY2026Q2I) vs **93,504,767** prior year (CY2025Q2I)
- Change: **9.0%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-07** — Item 1.01 (Entry into a Material Definitive Agreement): On July 1, 2026, The Oncology Institute, Inc. (the "Company")

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 45,000 sh / $261,090 vs sells 322,305 sh / $2,096,650 -> net $-1,835,560 (SELLING).
Distinct insiders buying (code P): 1. Largest buy: Chernett Jorey bought 18,000 sh @ $5.27 ($94,860) on 2026-07-21.

Form 4 filings parsed: 12; transaction rows: 18 (open-market buys 3, sales 3).

| code | rows |
|---|---|
| A | 7 |
| M | 4 |
| P | 3 |
| S | 4 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'Starling Oncology Reports Second Quarter'; skipped 14 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EXHIBIT 99.1 (ex99x1.htm)

Starling Oncology Reports Second Quarter
2026 Financial Results and Updates Full-Year 2026 Guidance

CERRITOS,
Calif., August 6, 2026 -- Starling Oncology, Inc. (NASDAQ: STLN) ("STLN" or the "Company"), one of the largest
value-based community oncology groups in the United States, today reported financial results for its quarter ended June 30, 2026
and updated it's full-year 2026 guidance.

Recent
Operational Highlights

• | Specialty Pharmacy had record Part D fills driving Specialty Pharmacy revenue up 58% in the quarter as compared to prior year same quarter, driven by continued strength in prescription fill volumes as we bring new capitated lives onto the platform, along with the ongoing ramp of our Florida delegated arrangements.

• | Results in the first half of the year have given us the opportunity to raise guidance for revenue and gross profit.

• | Preparing to launch our proprietary provider portal, Starling Nexus, in mid-August which is designed to strengthen provider engagement and drive continued adherence to our clinical pathways, particularly for our network physicians.

• | Achieved exclusivity in California with one of our largest partners across all of their delegated medical groups, a relationship that was previously split with another entity. This added approximately 230,000 capitated lives.

Second Quarter 2026 Financial Highlights

All comparisons are to the quarter ended
June 30, 2025 unless otherwise noted

• | Consolidated revenue of $161.3 million increased 34.6% from $119.8 million

• | Gross profit of $27.2 million, increased 55.2%

• | Net loss of $9.8 million compared to net loss of $17.0 million

• | Basic and diluted (loss) earnings per share of $(0.08) compared to $(0.15)

• | Adjusted EBITDA * of positive $229 thousand compared to $(4.1) million

• | Cash and cash equivalents of $41.1 million as of June 30, 2026

*Adjusted EBITDA is a non-GAAP measure
and the reconciliation is included in the Financial Information; Non-GAAP Financial Measures section below.

Management
Commentary

Daniel Virnich, CEO of Starling,
commented, "The second quarter of 2026 was a milestone quarter for our company, with revenue up 35% year over year and Adjusted EBITDA
turning positive in Q2. We signed our first delegated contracts outside of Florida, in Nevada and Oregon, and reached an exclusivity agreement
with one of our largest partners across California. Both of these achievements will drive robust capitated revenue growth going forward.
In mid-August, we are launching our new provider portal, Starling Oncology NexusTM, which we expect will deepen provider engagement and
further support adherence to our clinical pathways. Given this momentum, we are raising our full-year outlook, and remain confident in
our path to sustained positive Adjusted EBITDA as we move forward as Starling Oncology."

Updated Outlook for
Fiscal Year 2026

2026 Guidance - Previous | 2026 Guidance - Updated
Revenue | $630 to $650 million | $650 to $670 million
Gross Profit | $97 to $107 million | $105 to $110 million
Adjusted EBITDA | $0 to $9 million | $2 to $7 million
Free Cash Flow | $5 to $15 million | Unchanged

* The Company uses Adjusted EBITDA, Medical
Loss Ratio (MLR), and Free Cash flow, each a non-GAAP measure, as an additional tool to assess its operational and financial performance.
See "Financial Information: Non-GAAP Financial Measures" below. In reliance on the unreasonable efforts exception provided under
Regulation S-K, STLN is not reasonably able to provide a quantitative reconciliation for forward-looking information of Adjusted EBITDA,
MLR and Free Cash flow to net (loss) income and net cash provided by operations, respectively, the most directly comparable GAAP financial
measures, without unreasonable efforts due to uncertainties regarding capitated lives, direct costs, taxes, capital expenditures, share-based
compensation, change in fair value of liabilities, unrealized (gains) losses on investments, consulting and legal fees, transaction costs
and other non-cash items. The variability of these items could have an unpredictable, and potentially significant, impact on STLN's
future GAAP financial results.

The Company expects approximately $150 million
in capitated revenue in 2026. The Company also anticipates that Medical Loss Ratio, discussed under "Financial Information; Non-GAAP
Financial Measures" below, will be in the range of 80% to 90% in the next twelve months.

Third Quarter of 2026 Outlook

For the third quarter of 2026, we anticipate
Adjusted EBITDA of $500 thousand to $1.5 million, as the Company onboards and ramps our Florida delegated lives.

Founded in 2007, Starling Oncology, Inc. (NASDAQ: STLN) is advancing
oncology by delivering highly specialized, value-based cancer care in the community setting. Formerly known as The Oncology Institute,
Starling Oncology offers cutting-edge, evidence-based cancer care to a population of approximately 2.1 million patients including clinical
trials, transfusions, and other care delivery models traditionally associated with the most advanced care delivery organizations. With
over 400 employed and network clinicians and over 100 clinics and network locations of care across five states and growing, Starling Oncology
is coordinating cancer care for the better. For more information visit www.starlingoncology.com. Please follow us on LinkedIn, X (formerly
Twitter), or Bluesky.

STLN believes that the use of Adjusted EBITDA provides management
with an additional tool to assess our operations and results of our performance, to plan and forecast future periods, and factors and
trends. We believe that Adjusted EBITDA is helpful to investors in measuring our financial performance and comparing our performance to
our peers. Adjusted EBITDA has important limitations as an analytical tool, and should not be considered in isolation, or as a substitute
for analysis of our results as reported under GAAP.

A reconciliation of total direct costs and
revenue related to capitated contracts to MLR, net cash flow provided by (used in) operations to Free Cash Flow, and net loss to Adjusted
EBITDA, the most comparable GAAP metrics, is set forth below:

Medical Loss Ratio (MLR)
Three Months Ended June 30, | Change
(dollars in thousands) | 2026 | 2025 | %
Direct costs - patient services | 56,771 | 51,150 | 5,621 | 11.0 | %
Direct costs - fee-for-service | (32,860 | (37,769 | 4,909 | (13.0 | )%
Direct costs - capitated | 23,911 | 13,381 | 10,530 | 78.7 | %
Patient services revenue | 58,827 | 55,891 | 2,936 | 5.3 | %
Fee-for-service revenue | (30,853 | (37,048 | 6,195 | (16.7 | )%
Capitated revenue | 27,974 | 18,843 | 9,131 | 48.5 | %
Medical loss ratio related to capitated contracts | 85.5 | % | 71.0 | % | 1,399 | 14.5 | %

Free Cash Flow Reconciliation
Six Months Ended June 30, | Change
(dollars in thousands) | 2026 | 2025 | %
Net cash and cash equivalents provided by (used in) operating activities | 9,725 | (15,190 | 24,915 | 164.0 | %
Cash paid for interest | 1,756 | 2,158 | (402 | 18.6 | %
Purchases of property and equipment | (1,950 | (1,536 | (414 | (27.0 | )%
Free Cash Flow | 9,531 | (14,568 | 24,099 | 165.4 | %

Adjusted EBITDA Reconciliation
Three Months Ended June 30, | Change | Six Months Ended June 30, | Change
(dollars in thousands) | 2026 | 2025 | % | 2026 | 2025 | %
Net loss | (9,789 | (17,009 | 7,220 | 42.4 | % | (12,281 | (36,594 | 24,313 | 66.4 | %
Depreciation and amortization | 1,838 | 1,805 | 33 | 1.8 | % | 3,454 | 3,589 | (135 | (3.8 | )%
Interest expense, net | 1,859 | 1,870 | (11 | (0.6 | )% | 3,793 | 7,440 | (3,647 | (49.0 | )%
Income tax and other taxes | 86 | (61 | 147 | — | % | 129 | (61 | 190 | — | %
Non-cash addbacks | (36 | 2,222 | (2,258 | (101.6 | )% | (284 | 2,059 | (2,343 | (113.8 | )%
Share-based compensation | 1,070 | 752 | 318 | 42.3 | % | 2,756 | 2,210 | 546 | 24.7 | %
Changes in fair value of liabilities | 3,237 | 4,040 | (803 | (19.9 | )% | (1,927 | 7,392 | (9,319 | (126.1 | )%
Unrealized loss on investments | — | — | — | — | % | — | 6 | (6 | (100.0 | )%
Post-combination compensation expense | — | 13 | (13 | (100.0 | )% | — | 26 | (26 | (100.0 | )%
Consulting fees | 1,814 | 506 | 1,308 | 258.5 | % | 2,087 | 839 | 1,248 | 148.7 | %
Infrastructure and workforce costs | 150 | 1,771 | (1,621 | (91.5 | )% | 64 | 3,895 | (3,831 | (98.4 | )%
Transaction costs | — | 1 | (1 | — | % | — | 1 | (1 | (100.0 | )%
Adjusted EBITDA | 229 | (4,090 | 4,319 | 105.6 | % | (2,209 | (9,198 | 6,988 | 76.0 | %

Key Business Metrics
Three Months Ended June 30,
(dollars in thousands) | 2026 | 2025
Affiliated and Network Clinics (1) | 301 | 80
Markets | 17 | 20
Lives under value-based contracts (millions) | 2.1 | 1.9

(1) | Number of clinics operated under the STLN PCs, whereby we receive a percentage of revenue under our management services agreements, or MSAs, and are consolidated. Additionally, includes independent oncology practices to which we provide limited management services and have network provider agreements, but do not bear the operating costs.

Consolidated
Balance Sheets (Unaudited)

(in thousands except share data)

June 30, 2026 | December 31, 2025
Assets
Current assets:
Cash and cash equivalents | 41,094 | 33,565
Accounts receivable, net | 66,349 | 58,998
Other receivables | 360 | 322
Inventories | 20,011 | 16,875
Prepaid expenses and other current assets | 1,176 | 2,987
Total current assets | 128,990 | 112,747
Property and equipment, net | 10,583 | 10,684
Operating right of use assets | 21,188 | 22,374
Intangible assets, net | 9,585 | 11,015
Goodwill | 7,230 | 7,230
Other assets | 657 | 606
Total assets | 178,233 | 164,656
Liabilities and stockholders' deficit
Current liabilities:
Accounts payable | 60,279 | 43,167
Current portion of operating lease liabilities | 7,225 | 7,156
Accrued expenses and other current liabilities | 27,435 | 20,639
Total current liabilities | 94,939 | 70,962
Operating lease liabilities | 17,384 | 19,131
Derivative warrant liabilities | 89 | 264
Derivative liabilities | 10,838 | 12,591
Long-term debt, net of unamortized debt issuance costs | 79,867 | 77,400
Other non-current liabilities | 30 | 28
Total liabilities | 203,147 | 180,376
Stockholders' deficit:
Common Stock, 0.0001 par value, authorized 500,000,000 shares; 102,202,753 and 100,468,979 shares issued and outstanding at June 30, 2026 and 100,596,918 shares issued and 98,863,144 shares outstanding at December 31, 2025 | 10 | 10
Series A Convertible Preferred Stock, 0.0001 par value, authorized 10,000,000 shares; 193,507 shares issued and outstanding at June 30, 2026 and 193,507 shares issued and outstanding at December 31, 2025 | — | —
Additional paid-in capital | 259,795 | 256,708
Treasury Stock at cost, 1,733,774 shares at June 30, 2026 and December 31, 2025 | (1,019 | (1,019
Accumulated deficit | (283,700 | (271,419
Total stockholders' deficit | (24,914 | (15,720
Total liabilities and stockholders' deficit | 178,233 | 164,656

Consolidated Statements of Operations (Unaudited)

(in thousands except share data)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-12_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

The Company is a leading value-based oncology company that manages community-based oncology practices for the Company and for independent oncology practices that together serve patients across 17 markets and five states throughout the United States. As of December 31, 2025, we operate 65 community-based oncology practices, staffed with 116 oncologists and advanced practice providers employed by our affiliated physician-owned professional corporations, referred to as the "TOI PCs." In addition to our TOI-affiliated providers, we also manage a network of 207 providers in Florida under the Florida Oncology Network brand. Collectively across the provider base, we manage a population of approximately 2.0 million patients under value-based agreements as of December 31, 2025 . The Company's mission is to heal and empower cancer patients through compassion, innovation, and state-of-the-art medical care.

Operationally, the Company's medical centers provide a complete suite of medical oncology services including: physician services, in-house infusion, in-house specialty pharmacy, clinical trials, radiation therapy, educational seminars, support groups, counseling, and 24/7 patient assistance. Many of our services, such as managing clinical trials and palliative care programs, are traditionally accessed through academic and tertiary care settings, while the TOI PCs bring these services to patients in a community setting. As scientific research progresses and more treatment options become available, cancer care is shifting from acute care episodes to chronic disease management. With this shift, it is increasingly important for high-quality, high-value cancer care to be available in a local community setting to all patients in need.

As a value-based oncology company, the Company seeks to deliver both better quality care and lower cost of care for payors and patients. The Company works to accomplish this goal by reducing wasteful, inefficient or counterproductive care that drives up costs but does not improve outcomes. The Company believes payors and employers are aligned with the value-based model due to its enhanced access, improved outcomes, and lower costs. Patients under the Company's affiliated providers' care can benefit from evidence-based and personalized care plans, gain access to sub-specialized care in convenient community locations, and lower out-of-pocket costs. The Company believes its affiliated providers enjoy the stability and predictability of a large multi-state practice, are not incentivized or pressured to overtreat when it may be inconsistent with a patient's goals of care, and can focus on practicing outstanding evidence-based medicine, rather than business building.

Additionally, we allow our independent network participating providers to access the ability to treat patient populations that are managed under value-based care contracts without the need to incur costs required to build clinical or operational infrastructure typical for risk-bearing entities, or to adopt new operational frameworks which may be disruptive to their existing practices.

Components of Results of Operations

Revenue

The Company receives payments from the following sources for services rendered: (i) commercial insurers; (ii) pharmacy benefit managers ("PBMs"), (iii) the federal government under the Medicare program administered by the Centers for Medicare and Medicaid Services ("CMS"); (iv) state governments under Medicaid and other programs; (v) other third-party payors and managed care organizations (e.g., risk bearing organizations and independent practice associations ("IPAs"); and (vi) individual patients and clients.

Revenue primarily consists of capitation revenue, fee-for-service ("FFS") revenue, specialty pharmacy revenue, and clinical trials revenue. Capitation and FFS revenue comprise the revenues within the Company's patient services segment and are presented together in the results of operations. The following paragraphs provide a summary of the principal forms of our billing arrangements and how revenue is recognized for each type of revenue.

Capitation

Capitation revenues consist primarily of fees for medical services provided by the TOI PCs or network providers to the Company's patients under a capitated arrangement with various risk-bearing medical groups or managed care organizations. Capitation revenue is paid monthly based on the number of enrollees by the contracted payor (per member per month or "PMPM"). Capitation contracts generally have a legal term of one year or longer. Payments in capitation contracts are variable since they primarily include PMPM fees associated with unspecified membership that fluctuates throughout the term of the contract; however, based on our experience, our total underlying membership generally increases over time as penetration of Medicare Advantage products grows and our payor partners, who tend to be the larger and more sophisticated operators within the industry, consolidate. Certain contracts include terms for a capitation deduction where the cost of out-of-network referrals of members are deducted from the future payment. Revenue is recognized in the month services are rendered on the basis of the transaction price established at that time.

Fee-for-service revenue

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The following table sets forth our Consolidated Statements of Operations data expressed as a percentage of total revenues for the periods indicated. The Company's management is not aware of material events or uncertainties that would cause the financial information below to not be indicative of future operating results or results of future financial condition, although past results should not be relied upon as an indication of future performance or future financial condition.

Year Ended December 31,
2025 | 2024
Revenue
Patient services | 45.6 | % | 52.1 | %
Specialty pharmacy | 53.5 | % | 45.7 | %
Clinical trials & other | 0.9 | % | 2.2 | %
Total operating revenue | 100.0 | % | 100.0 | %
Operating expenses
Direct costs – patient services | 40.9 | % | 47.5 | %
Direct costs – specialty pharmacy | 43.9 | % | 38.4 | %
Direct costs – clinical trials & other | — | % | 0.3 | %
Selling, general and administrative expense | 21.0 | % | 27.4 | %
Depreciation and amortization | 1.4 | % | 1.6 | %
Total operating expenses | 107.2 | % | 115.2 | %
Loss from operations | (7.2) | % | (15.2) | %
Other non-operating expense (income)
Interest expense, net | 2.2 | % | 1.9 | %
Change in fair value of derivative warrant liabilities | — | % | (0.2) | %
Change in fair value of conversion option derivative liabilities | 2.4 | % | (0.7) | %
Other, net | 0.3 | % | 0.2 | %
Total other non-operating expense | 4.9 | % | 1.2 | %
Loss before provision for income taxes | (12.1) | % | (16.4) | %
Income tax benefit | — | % | — | %
Net loss | (12.1) | % | (16.4) | %

Comparison of the Years Ended December 31, 2025 and 2024

Revenue

Year Ended December 31, | Change
(dollars in thousands) | 2025 | 2024 | %
Patient services | 228,991 | 204,883 | 24,108 | 11.8 | %
Specialty pharmacy | 269,176 | 179,916 | 89,260 | 49.6 | %
Clinical trials & other | 4,562 | 8,613 | (4,051) | (47.0) | %
Total operating revenue | 502,729 | 393,412 | 109,317 | 27.8 | %

Patient services

The increase in patient services revenue for the year ended December 31, 2025 compared to the prior year was primarily due to a 9.0% and 17.2% increase in FFS revenue and capitated revenue, respectively. This was driven by steady patient volumes in more mature markets, momentum in new markets in addition to the impact of our investments in referral relationship management, new contract development, and call center expansion.

Specialty Pharmacy

The increase in specialty pharmacy revenue was primarily due to a 66.6% increase in the number of fills offset by 10.2% decrease in the average revenue per fill. This is driven by increases in pharmacy services provided to both our capitated and fee-for-service populations, due to higher underlying patient volumes as well as a higher rate of prescriptions written by TOI's

affiliated physicians directed towards TOI's own internal pharmacy, as a result of active efforts to drive awareness and reduce 'leakage' to outside pharmacies.

Clinical trials & other

For the year ended December 31, 2025, the decrease in clinical trials and other revenue was due to the profit sharing agreement as described in Note 1 of the consolidated financial statements.

Operating Expenses

Year Ended December 31, | Change
(dollars in thousands) | 2025 | 2024 | %
Direct costs – patient services | $205,502 | 186,880 | 18,622 | 10.0 | %
Direct costs – specialty pharmacy | 220,558 | 151,231 | 69,327 | 45.8 | %
Direct costs – clinical trials & other | 234 | 1,304 | (1,070) | (82.1) | %
Selling, general and administrative expense | 105,574 | 107,828 | (2,254) | (2.1) | %
Depreciation and amortization | 6,944 | 6,287 | 657 | 10.5 | %
Total operating expenses | $538,812 | 453,530 | 85,282 | 18.8 | %

Patient services cost

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-12_item1_business.md)

Item 1. Business

Overview

Formed in 2007, the business of what is now The Oncology Institute, Inc. ("TOI", the "Company", "we", or "our) and its affiliated professional corporations was created initially as a collection of community oncology practices in southern California, and has evolved to be a national leader in the pursuit of reducing the ever-rising cost of oncology care, while embracing clinical best practices, state-of-the-art technology, and compassionate treatment of patients.

While we continue our original purpose of seeing our patients on a fee-for-service basis for their oncology, hematology, specialty infusion, oral pharmacy needs, as well as enrolling patients in clinical trials, where appropriate, TOI's true mission lies in our differentiated ability to partner with managed care providers and other risk-bearing entities to transfer the risk and patient coordination responsibility of treating cancer in the subset of the population that is experiencing an oncology treatment episode. To do this, we utilize a combination of gain/loss sharing, capitation, and full delegation contracts at the population-level, which allow TOI to control the treatment of oncology patients in an outpatient setting, across both medical oncology (traditional IV-based infusion therapy) and radiation oncology (radiation therapy provided by linear accelerator equipment).

TOI treats patients across 17 markets and five states throughout the United States, via our 65 clinics owned by affiliated physicians and staffed with 116 providers (the "TOI PCs"), 81 independently-owned clinics which are contracted with TOI's managed services organization, as well as our contracted network of 198 independent providers unaffiliated with TOI in instances where TOI is the fully delegated market manager under a value-based contract.

Through this network, TOI managed a population of approximately 2.0 million patients under value-based agreements as of December 31, 2025.

Our Business Lines

Patient Services

Fee for Service

TOI provides medical care on a fee-for service basis for physician services, in-house infusion, radiation, and innovative programs like outpatient blood product transfusions, along with 24/7 patient support. The services TOI provides in its fee for service business are generally covered under commercial and government managed care programs, which are billed retrospectively for care provided in clinics, following a typically small patient co-pay collected at the time of service. We customarily bill for physician and infusion services on a CPT-code basis, and for drugs on a cost-plus basis. We are generally reliant on outside referrals of these fee-for-service patients, who may be in the care of a primary care provider, non-oncology specialist physician, or hospitalist, who then refers the patient upon diagnosis to an oncology provider within TOI. We generate these referrals based on the reputation of our doctors and our platform within the communities we serve, as well as our active and direct referrer education efforts.

Value-based

TOI offers value-based contracts to payors, including managed care organizations and other risk-bearing entities, who are interested in transferring both the risk and responsibility for managing outpatient oncology care to us. These arrangements can take multiple different forms, but typically involve a population-level assignment, where TOI receives 100% share of a patient population and is paid either a fixed amount per member on a regular (typically monthly) schedule, or, less commonly, is paid/recoups a portion of gains/losses at the end of a measurement period. In this way, TOI receives a predictable, recurring payment for oncology care, and generates a profit to the extent the actual cost of oncology care for our contracted patient populations is less than this fixed payment. Generally, we are able to offer fixed payments to payors that represent a discount to the historical oncology cost and/or cost trend for these patient populations, while still generating positive profitability for TOI. We do this through active management of clinical pathways and drug formulary, incorporating best clinical practices and recognized quality metrics, using both our affiliated and MSO clinics, as well as negotiating network contracts with third-party providers. TOI's decade-plus of experience efficiently managing oncology populations, intensive clinical interventions, and TOI's comprehensive knowledge of therapeutic options across both pharmaceuticals and radiation therapy position us to effectively manage these contracts in a way that adds value to both our payor partners and patients.

Specialty Pharmacy

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-12_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-12_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-12_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-03-12_item7_mdna.md, 10-K_2026-03-12_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
