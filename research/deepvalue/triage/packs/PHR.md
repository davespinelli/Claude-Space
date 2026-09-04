# Triage pack — PHR · Phreesia, Inc.

_Generated 2026-09-04 22:10 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** PHR · **Name:** Phreesia, Inc.
- **CIK:** 0001412408
- **SIC:** 7389 — Services-Business Services, NEC
- **Fiscal year end (MM-DD):** 01-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/PHR

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Phreesia, Inc.
- **CIK:** 1,412,408 · **SIC:** 7389 (Services-Business Services, NEC) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebt

> **EARNINGS QUALITY FLAG — one-off items likely.**
> net income more than 3x operating income.
> Reported net income is not supported by the operating engine that is supposed to produce it (typical causes: gains on sale, legal settlements, deferred-tax valuation-allowance releases, bargain-purchase gains). Reconcile net income to operating income in the earnings release (section 7) before treating any earnings-based metric here as repeatable.

**Valuation**

| metric | value |
|---|---|
| price | 11.10 |
| mktcap | $686.1M |
| ev | $612.6M |
| ev_ebit | n/a |
| fcf | $67.7M |
| fcf_yield | 9.9% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -1.8% |
| net_debt | -$73.5M |
| net_debt_ebit | n/a |
| cash | $74.6M |
| ltd | $1.1M |
| equity | $371.9M |
| ltd_tag | LongTermDebt |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $480.6M |
| revenue_prior | $419.8M |
| rev_growth | 14.5% |
| rev_growth_note | n/a |
| eq_flag | net income more than 3x operating income |
| ebit | -$6.6M |
| net_income | $2.3M |
| cfo | $78.8M |
| capex | $11.1M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 3.9% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 61,811,889 |
| shares_py | 59,504,269 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -62.3% |
| r6m | -8.1% |
| off_52w_high | -64.4% |
| adv20 | $9.5M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.71 |
| r_ev_ebit | 0.00 |
| r_roic | 0.26 |
| r_rev_growth | 0.76 |
| r_buyback | 0.22 |
| score | 0.39 |

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
| rank | 329 |

**Screen rationale:** revenue +14.5%; EARNINGS QUALITY: net income more than 3x operating income — one-off items likely


## 3. Share count trend

- Shares outstanding: **61,811,889** (CY2026Q2I) vs **59,504,269** prior year (CY2025Q2I)
- Change: **3.9%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-05-04** — Item 1.01 (Entry into a Material Definitive Agreement): On April 30, 2026 (the "Closing Date"), AccessOne Funding, LLC ("AccessOne Funding"), an indirect wholly-owned subsidiary of Phreesia, Inc., a Delaware corporation ("Phreesia" or the "Company"), as seller, AccessOne MedCard, Inc. ("AccessOne MedCard"), an...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 1,247 sh / $13,617 -> net $-13,617 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 14 (open-market buys 0, sales 1).

| code | rows |
|---|---|
| A | 10 |
| F | 3 |
| S | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-09-02_2-02-results.md)

_Extraction: no Highlights/Results/quarter heading found; started at the top of the exhibit; skipped 11 forward-looking-statement block(s)._

## EX-99.1 - EX-99.1 (phr-ex991q2fy27.htm)

EX-99.1
phr-ex991q2fy27.htm
EX-99.1

Document

Exhibit 99.1

Phreesia Announces Second Quarter Fiscal 2027 Results

ALL-REMOTE COMPANY/WILMINGTON, Del., September 2, 2026 – Phreesia, Inc. (NYSE: PHR) ("Phreesia" or the "Company") announced financial results today for the fiscal second quarter ended July 31, 2026.

"Phreesia delivered a solid fiscal second quarter, with revenue growth and profitability expansion in line with our expectations. We generated positive operating and free cash flow again this quarter, which together with available cash allowed us to reduce debt principal by over $23 million while maintaining a healthy cash balance," said CEO and Co-Founder Chaim Indig. "We remain enthusiastic about two products that we believe will drive future growth, AccessOne and ProviderConnect, as well as the impact that our artificial intelligence (AI) investments are beginning to have on many aspects of our products and broader organization."

Please visit the Phreesia investor relations website at ir.phreesia.com to view the Company's Q2 Fiscal 2027 Stakeholder Letter.

Fiscal Second Quarter Ended July 31, 2026 Highlights

• Total revenue was $129.5 million in the quarter, up 10% year-over-year.

• Average number of healthcare services clients ("AHSCs") was 4,744 in the quarter, up 6% year-over-year.

• Total revenue per AHSC was $27,289 in the quarter, up 4% year-over-year. See "Key Metrics" below for additional information.

• Net income was $1.9 million in the quarter, as compared to net income of $0.7 million in the same period in the prior year.

• Adjusted EBITDA 1 was $32.9 million in the quarter, as compared to $22.1 million in the same period in the prior year.

• Net cash provided by operating activities was $18.3 million in the quarter, as compared to $14.8 million in the same period in the prior year.

• Free cash flow 2 was $13.8 million in the quarter, as compared to $9.6 million in the same period in the prior year.

• Cash, cash equivalents and restricted cash as of July 31, 2026 was $74.6 million, an increase of $0.8 million from January 31, 2026. As of July 31, 2026, cash, cash equivalents and restricted cash included $1.7 million of long-term restricted cash classified within other long-term assets.

Recent Developments

Restructuring Plan

On May 7, 2026, we implemented a restructuring plan (the "Plan") intended to reduce operating expenses and better align the cost structure with our current business priorities. The Plan includes the elimination of approximately 220 positions, approximately half of which are contractor roles. We expect total restructuring charges in connection with the Plan to be approximately $10 million, substantially all of which are expected to consist of employee transition costs, severance payments and related employee benefits, and taxes. Restructuring charges of

1 Adjusted EBITDA is a non-GAAP measure. We calculate Adjusted EBITDA as net income (loss) before interest expense, interest income, income tax expense (benefit), depreciation and amortization, stock-based compensation expense, loss on extinguishment of debt, other expense (income), net and certain other items that are not considered to reflect our operating activities and performance within the ordinary course of business, such as acquisition- and restructuring-related costs. The calculation of Adjusted EBITDA was updated beginning in Q3 of Fiscal 2026 to include an adjustment for acquisition-related costs. Prior periods have not been retroactively adjusted. See "Non-GAAP Financial Measures" for more information and a reconciliation of Adjusted EBITDA to the closest GAAP measure.

2 Free cash flow is a non-GAAP measure. We calculate free cash flow as net cash provided by operating activities less capitalized internal-use software development costs and purchases of property and equipment. See "Non-GAAP Financial Measures" for a reconciliation of free cash flow to the closest GAAP measure.

approximately $2.8 million were recognized for the Plan during the second quarter of fiscal 2027. We expect the Plan to be substantially completed during fiscal year 2027.

Fiscal 2027 Outlook

We are maintaining our revenue outlook for fiscal 2027. We expect revenue to be in the range of $510 million to $520 million. As we noted over the past several quarters, there is now more variability in our network solutions revenue forecasting, particularly in the second half of each fiscal year. Our visibility into revenue across the other parts of our business is generally consistent with our views in our March 2026 earnings disclosure. The revenue range provided for fiscal 2027 assumes approximately $37 million of contribution from AccessOne (as defined below) and no additional revenue from potential future acquisitions completed between now and January 31, 2027.

We are maintaining our Adjusted EBITDA outlook for fiscal 2027. We expect Adjusted EBITDA to be in the range of $125 million to $135 million. As a reminder, in May 2026, we implemented a restructuring plan intended to reduce operating expenses and better align our cost structure with our current business priorities. The plan is expected to result in meaningful annualized run-rate expense savings, which were reflected in our Adjusted EBITDA outlook provided on March 30, 2026 and reaffirmed on May 27, 2026.

We are maintaining our expectation for AHSC growth in the mid-single-digit percentage range, and we are maintaining our outlook for total revenue per AHSC to grow in the low-single-digit percentage range in fiscal 2027.

We believe our cash, cash equivalents, restricted cash and cash generated in our normal operations will be sufficient to reach our fiscal 2027 outlook and meet our obligations for at least the next twelve months. As of July 31, 2026 we had $61 million in borrowings outstanding under our credit facility with Capital One.

Non-GAAP 3 Financial Measures

We have not reconciled our Adjusted EBITDA outlook to GAAP net income (loss) because we do not provide an outlook for GAAP net income (loss) due to the uncertainty and potential variability of other expense (income), net and income tax expense (benefit), which are reconciling items between Adjusted EBITDA and GAAP net income (loss). Because we cannot reasonably predict such items, a reconciliation of the non-GAAP financial measure outlook to the corresponding GAAP measure is not available without unreasonable effort. We caution, however, that such items could have a significant impact on the calculation of GAAP net income (loss). For further information regarding the non-GAAP financial measures included in this press release, including a reconciliation of GAAP to non-GAAP financial measures and an explanation of these measures, please see "Non-GAAP Financial Measures" below.

Available Information

We intend to use our Company website (including our Investor Relations website) as well as our Facebook, X, LinkedIn and Instagram accounts as a means of disclosing material non-public information and for complying with our disclosure obligations under Regulation FD.

Phreesia is a trusted leader in patient activation, giving healthcare providers, life sciences companies and other organizations tools to help patients take a more active role in their care. Founded in 2005, Phreesia enabled more than 180 million patient visits in 2025—1 in 6 visits across the U.S. This scale allows Phreesia to make meaningful impact across the healthcare ecosystem. Offering patient-driven digital solutions for intake, outreach, education and

more, Phreesia enhances the patient experience, drives operational efficiency and improves healthcare outcomes. To learn more, visit phreesia.com.

Investor Relations Contact:

Balaji Gandhi

Phreesia, Inc.

investors@phreesia.com

(929) 506-4950

Media Contact:

Nicole Gist

Phreesia, Inc.

nicole.gist@phreesia.com

(407) 760-6274

Phreesia, Inc.

Consolidated Balance Sheets

(in thousands, except share and per share data)

July 31, 2026 | January 31, 2026
(Unaudited)
Assets
Current:
Cash, cash equivalents and restricted cash (including restricted cash of $— and $1,691 as of July 31, 2026 and January 31, 2026, respectively) | 72,945 | 73,830
Settlement assets | 26,746 | 32,999
Accounts receivable, net of allowance for doubtful accounts of $879 and $1,523 as of July 31, 2026 and January 31, 2026, respectively | 89,406 | 97,453
Cardholder receivables | 29,351 | 38,330
Deferred purchase price receivables | 14,799 | 18,003
Accrued interest and fees receivables | 723 | 840
Deferred contract acquisition costs | 394 | 410
Prepaid expenses and other current assets | 19,139 | 17,978
Total current assets | 253,503 | 279,843
Property and equipment, net of accumulated depreciation and amortization of $90,281 and $94,193 as of July 31, 2026 and January 31, 2026, respectively | 18,122 | 20,332
Capitalized internal-use software, net of accumulated amortization of $77,389 and $69,390 as of July 31, 2026 and January 31, 2026, respectively | 54,127 | 54,270
Operating lease right-of-use assets | 1,205 | 2,002
Deferred contract acquisition costs | 130 | 338
Intangible assets, net of accumulated amortization of $18,728 and $13,489 as of July 31, 2026 and January 31, 2026, respectively | 74,522 | 79,761
Goodwill | 171,468 | 170,064
Deferred tax assets | 990 | 1,593
Other assets (includes $1,691 and $— of long-term restricted cash as of July 31, 2026 and January 31, 2026, respectively) | 6,669 | 2,442
Long-term cardholder receivables | 59,587 | 47,723
Long-term deferred purchase price receivables | 6,654 | 5,422
Total Assets | 646,977 | 663,790
Liabilities and Stockholders' Equity
Current:
Settlement obligations | 26,746 | 32,999
Current portion of debt and finance lease liabilities | 5,281 | 7,971
Current portion of operating lease liabilities | 824 | 1,254
Accounts payable | 12,237 | 11,477
Accrued expenses | 35,706 | 41,257
Due to healthcare providers | 29,737 | 38,056
Deferred revenue | 32,573 | 49,522
Other current liabilities | 731 | 705
Total current liabilities | 143,835 | 183,241
Long-term debt and finance lease liabilities | 61,165 | 92,117
Operating lease liabilities, non-current | 677 | 1,107
Long-term due to healthcare providers | 59,734 | 45,329
Long-term deferred revenue | 4,687 | 244
Long-term deferred tax liabilities | 4,589 | 4,498
Other long-term liabilities | 439 | 47
Total Liabilities | 275,126 | 326,583
Commitments and contingencies
Stockholders' Equity:
Preferred stock, undesignated, $0.01 par value—20,000,000 shares authorized as of both July 31, 2026 and January 31, 2026; no shares issued or outstanding as of both July 31, 2026 and January 31, 2026 | — | —
Common stock, $0.01 par value—500,000,000 shares authorized as of both July 31, 2026 and January 31, 2026; 63,516,793 and 62,020,186 shares issued as of July 31, 2026 and January 31, 2026, respectively | 635 | 620
Additional paid-in capital | 1,212,775 | 1,181,679
Accumulated deficit | (794,309) | (799,190)
Accumulated other comprehensive loss | (621) | (382)
Treasury stock, at cost, 1,476,215 and 1,355,169 shares as of July 31, 2026 and January 31, 2026, respectively | (46,629) | (45,520)
Total Stockholders' Equity | 371,851 | 337,207
Total Liabilities and Stockholders' Equity | 646,977 | 663,790

Phreesia, Inc.

Unaudited Consolidated Statements of Operations

(in thousands, except share and per share data)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-31_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We provide an integrated software, payments, and engagement platform designed to address three foundational challenges in healthcare delivery: access to care, affordability of care, and health patient outcomes. Our platform is embedded directly into provider workflows and patient interactions, enabling healthcare organizations to activate patients, streamline administrative processes, and improve financial performance across the care continuum. Our integrated platform is designed to address challenges patients and healthcare providers face in three core areas: Access, Affordability, and Outcomes.

Access: Our solutions facilitate access to care by reducing friction in how patients find, schedule, and register for care, while enabling providers to improve capacity utilization and reduce administrative burden. Key capabilities include care discovery and scheduling through MediFind, our online provider directory, and self-scheduling tools; appointment optimization and referral management using AI-enabled workflows; and our AI-based smart answering solution patient communications supported by voice and messaging solutions.

Affordability: Our solutions directly address affordability challenges and improve the patient experience while helping providers improve collections, accelerate cash flow, and reduce revenue cycle friction. Capabilities include eligibility and cost transparency tools, integrated payment solutions embedded in intake and post-visit workflows, and financing solutions that enable healthcare organizations to accelerate cash collections while offering flexible payment options to patients.

Outcomes: Our solutions are designed to improve patient outcomes by promoting patient engagement, treatment adherence and satisfaction, while enabling healthcare stakeholders, including providers and life sciences organizations, to measure and influence patient behavior in a compliant and scalable manner. Capabilities include digital intake and clinical data capture, patient engagement and activation tools, and measurement and analytics solutions.

We serve a diverse group of healthcare organizations including ambulatory practices, health systems, and hospitals, as well as life sciences companies, government entities, patient advocacy, public interest and not-for-profit and other organizations. Our solutions support the patient journey from care discovery and scheduling through intake, payment, and post-visit follow-up. In fiscal year 2026, our platform facilitated approximately 180 million patient visits, representing approximately one in six ambulatory patient visits in the United States.

We generate revenue through a diversified model that includes three revenue streams: subscription and related services; payment solutions, which include payment processing fees and financing fees; and Network Solutions, which provides a channel for life sciences companies and other organizations to deliver compliant, personalized engagement to patients and providers who use our solutions.

Subscription and related services revenue is relatively consistent throughout the fiscal year due to the recurring nature of our contracts. Payment solutions revenue is typically higher during the first two to three months of the calendar year, driven in part by the resetting of patient deductibles. Network Solutions revenue is primarily generated through annual contracts priced on a per-engagement basis, supported by closed-loop reporting and third-party measurement, and is typically higher in the second half of our fiscal year, reflecting life sciences marketing budget cycles. Phreesia creates high-intent engagement opportunities delivered at critical moments in the care journey.

Since our inception, we have focused substantially all of our sales efforts within the United States. Accordingly, substantially all of our revenue from historical periods has come from the United States, and our current strategy is to continue to focus substantially all of our sales efforts within the United States.

Our revenue growth has been primarily organic and reflects our significant addition of new healthcare services clients. New healthcare services clients are defined as clients that go live in the applicable period and existing healthcare services clients are defined as clients that go live in any period before the applicable period.

Recent developments and current economic conditions

AccessOne Acquisition

On August 29, 2025, the Company entered into a definitive agreement (the "Merger Agreement") to acquire AccessOne for the base purchase price of approximately $160.0 million, subject to customary closing and post-closing adjustments (such transactions contemplated by the agreement, the "AccessOne Acquisition"). On November 12, 2025 (the "Closing Date"), we completed the transactions contemplated by the Merger Agreement, pursuant to which, upon the terms and subject to the conditions set forth therein, Ace Merger Sub, Inc. merged with and into AccessOne, with AccessOne continuing as the surviving corporation and becoming a wholly owned subsidiary of the Company. The purchase price was funded with a combination of cash and the net proceeds from a new, 364-day $110.0 million secured term loan (the "Bridge Loan") entered into on the Closing Date.

The AccessOne Acquisition expands our addressable market for healthcare payments. Our payment solutions now offer healthcare providers a trusted, scalable, compliant and operationally efficient healthcare payment card that accelerates cash flow.

Bridge Loan

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of operations

The following tables set forth our results of operations for the periods presented and as a percentage of revenue for those periods:

For the fiscal years ended January 31,
(in thousands) | 2026 | 2025 | 2026 | 2025
Revenue
Subscription and related services | 219,461 | 196,510 | 46 | % | 47 | %
Payment solutions (1) | 121,459 | 101,740 | 25 | % | 24 | %
Network solutions | 139,671 | 121,563 | 29 | % | 29 | %
Total revenues | 480,591 | 419,813 | 100 | % | 100 | %
Expenses
Cost of revenue (excluding depreciation and amortization) | 71,365 | 66,227 | 15 | % | 16 | %
Payment solutions expense (1) | 82,758 | 68,707 | 17 | % | 16 | %
Sales and marketing | 100,243 | 121,129 | 21 | % | 29 | %
Research and development | 121,481 | 117,364 | 25 | % | 28 | %
General and administrative | 79,903 | 76,597 | 17 | % | 18 | %
Depreciation | 12,972 | 14,183 | 3 | % | 3 | %
Amortization | 18,481 | 13,703 | 4 | % | 3 | %
Total expenses | 487,203 | 477,910 | 101 | % | 114 | %
Operating loss | (6,612) | (58,097) | (1) | % | (14) | %
Other income, net | 2,953 | 1,956 | 1 | % | — | %
Loss on extinguishment of debt | (501) | — | — | % | — | %
Interest expense | (6,953) | (2,347) | (1) | % | (1) | %
Interest income | 2,173 | 2,677 | — | % | 1 | %
Total other (expense) income, net | (2,328) | 2,286 | — | % | 1 | %
Loss before income tax expense | (8,940) | (55,811) | (2) | % | (13) | %
Income tax benefit (expense) | 11,246 | (2,716) | 2 | % | (1) | %
Net income (loss) | 2,306 | (58,527) | — | % | (14) | %
(1) The revenue line previously labeled "Payment processing fees" has been relabeled "Payment solutions" to reflect the expanded scope of our payments offerings following the AccessOne Acquisition, which closed on November 12, 2025. Additionally, "Payment processing expense" has been relabeled "Payment solutions expense." Prior period amounts have not been reclassified, as the Company did not own the acquired operations in prior periods and the change in presentation did not affect any previously reported amounts. See Note 2 - Basis of presentation.

Components of consolidated statements of operations

Revenue

We generate revenue primarily from providing an integrated SaaS-based software and payment platform for the healthcare industry. We derive revenue from subscription fees and related services generated from our healthcare services clients for access to our solutions, payment solutions fees based on patient payment processing volume and financing fees based on a portfolio of cardholder receivables; and from fees from life sciences companies and other organizations for delivering direct communications to help activate, engage and educate patients about topics critical to their health.

Our total revenue consists of the following:

• Subscription and related services. We primarily generate subscription fees from our healthcare services clients based on the number of healthcare services clients that subscribe to and utilize our solutions. Our healthcare services clients are typically billed monthly in arrears, though in some instances, healthcare services clients may opt to be billed quarterly or annually in advance. Subscription fees are typically auto-debited from

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-31_item1_business.md)

Item 1. Business

Overview

Phreesia, Inc. ("Phreesia," "we," "our," or the "Company") was founded in 2005 and completed its initial public offering in July 2019. Phreesia provides an integrated software, payments, and engagement platform designed to address three foundational challenges in healthcare delivery: access to care, affordability of care, and patient health outcomes. Our platform is embedded directly into provider workflows and patient interactions, enabling healthcare organizations to activate patients, streamline administrative processes, and improve financial performance across the care continuum.

We serve a diverse group of healthcare organizations including ambulatory practices, health systems, and hospitals, as well as life sciences companies, government entities, patient advocacy, public interest and not-for-profit and other organizations. Our solutions support the patient journey from care discovery and scheduling through intake, payment, and post-visit follow-up. In fiscal year 2026, our platform facilitated approximately 180 million patient visits, representing approximately one in six ambulatory patient visits in the United States.

In fiscal year 2026, we completed the acquisition (the "AccessOne Acquisition") of AccessOne Parent Holdings, Inc. (together with its subsidiaries, "AccessOne"), which expands our addressable market for healthcare payments. Our payment solutions now offer healthcare providers a trusted, scalable, compliant and operationally efficient healthcare payment card that accelerates cash flow.

Revenue

We generate revenue through a diversified model that includes three revenue streams: subscription and related services; payment solutions (previously labeled payment processing fees), which include payment processing fees and financing fees; and Network Solutions, which provides a channel for life sciences companies and other organizations to deliver compliant, personalized engagement to patients and providers who use our solutions.

Our business model provides meaningful visibility into future revenue, as our revenue is primarily derived from recurring subscription fees and re-occurring payment processing fees and financing fees. Subscription and related services revenue is relatively consistent throughout the fiscal year due to the recurring nature of our contracts. Payment solutions revenue is typically higher during the first two to three months of the calendar year, driven in part by the resetting of patient deductibles. Network Solutions revenue is primarily generated through annual contracts priced on a per-engagement basis, supported by closed-loop reporting and third-party measurement, and is typically higher in the second half of our fiscal year, reflecting life sciences marketing budget cycles. Phreesia creates high-intent engagement opportunities delivered at critical moments in the care journey.

Our Platform and Solutions

Phreesia's integrated platform is designed to address challenges patients and healthcare providers face in three core areas: Access, Affordability, and Outcomes.

Access

Phreesia's solutions facilitate access to care by reducing friction in how patients find, schedule, and register for care, while enabling providers to improve capacity utilization and reduce administrative burden.

Key capabilities include care discovery and scheduling through MediFind, our online provider directory, and self-scheduling tools; appointment optimization and referral management using AI-enabled workflows; and our AI-based smart answering solution for patient communications supported by voice and messaging solutions.

Affordability

Phreesia's solutions directly address affordability challenges and improve the patient experience while helping providers improve collections, accelerate cash flow, and reduce revenue cycle friction.

Capabilities include eligibility and cost transparency tools, integrated payment solutions embedded in intake and post-visit workflows, and financing solutions that enable healthcare organizations to accelerate cash collections while offering flexible payment options to patients.

Outcomes

Phreesia's solutions are designed to improve patient outcomes by promoting patient engagement, treatment adherence and satisfaction, while enabling healthcare stakeholders, including providers and life sciences organizations, to measure and influence patient behavior in a compliant and scalable manner.

Capabilities include digital intake and clinical data capture, patient engagement and activation tools, and measurement and analytics solutions.

Market Opportunity

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-31_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-31_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-31_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-09-02_2-02-results.md, 10-K_2026-03-31_item7_mdna.md, 10-K_2026-03-31_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
