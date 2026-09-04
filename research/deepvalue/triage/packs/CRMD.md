# Triage pack — CRMD · CorMedix Inc.

_Generated 2026-09-04 12:10 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** CRMD · **Name:** CorMedix Inc.
- **CIK:** 0001410098
- **SIC:** 2834 — Pharmaceutical Preparations
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /Users/davidspinelli/Documents/Claude Space/research/deepvalue/filings/CRMD

## 2. Screen row (all metrics)

_Source: candidates.csv_

- **Name:** CorMedix Inc.
- **CIK:** 1,410,098 · **SIC:** 2834 (Pharmaceutical Preparations) · **Exchange:** Nasdaq

**Valuation**

| metric | value |
|---|---|
| price | 8.47 |
| mktcap | $660.2M |
| ev | $403.5M |
| ev_ebit | 2.7x |
| fcf | $172.8M |
| fcf_yield | 26.2% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 58.1% |
| net_debt | -$256.7M |
| net_debt_ebit | -1.7x |
| cash | $256.7M |
| ltd | $0.00 |
| equity | $460.8M |
| ltd_tag | none |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $311.7M |
| revenue_prior | $43.5M |
| rev_growth | 617.0% |
| rev_growth_note | n/a |
| ebit | $150.1M |
| net_income | $163.1M |
| cfo | $175.0M |
| capex | $2.3M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 4.4% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 77,944,324 |
| shares_py | 74,648,992 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -45.9% |
| r6m | 34.4% |
| off_52w_high | -35.3% |
| adv20 | $11.8M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.96 |
| r_ev_ebit | 0.99 |
| r_roic | 0.97 |
| r_rev_growth | 1.00 |
| r_buyback | 0.16 |
| score | 0.82 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q2I |
| shares_period | CY2026Q2I |
| shares_py_period | CY2025Q2I |
| capex_missing | False |
| ltd_missing | True |

**Screen rationale:** top-quartile FCF yield 26.2%; cheap at 2.7x EV/EBIT; high ROIC 58.1%; revenue +617.0%; net cash


## 3. Share count trend

- Shares outstanding: **77,944,324** (CY2026Q2I) vs **74,648,992** prior year (CY2025Q2I)
- Change: **4.4%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-02 among the 6 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 0 sh / $0 -> net $0 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 16 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 9 |
| F | 7 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-13_2-02-results.md)

## EX-99.1 - EX-99.1 (crmd_q22026earningspr.htm)

EX-99.1
2
crmd_q22026earningspr.htm
EX-99.1

Document

Exhibit 99.1

CORMEDIX THERAPEUTICS REPORTS SECOND QUARTER 2026 FINANCIAL RESULTS AND PROVIDES BUSINESS UPDATE

‒ Q2 2026 Consolidated Revenue of $101.9 million ‒

‒ Q2 2026 Net Income of $26.0 million ; Adjusted EBITDA of $58.7 million ‒

‒ Company Maintains FY 2026 Revenue and Raises Adjusted EBITDA Guidance ‒

‒ Conference Call Scheduled for Today at 8:30 a.m. Eastern Time ‒

Parsippany, NJ – August 13, 2026 – CorMedix Therapeutics (Nasdaq: CRMD) today announced financial results for the second quarter ended June 30, 2026, and provided an update on its business.

Recent Corporate Highlights:

• CorMedix announces $101.9 million of total revenue and grant income ("consolidated revenue") for the second quarter of 2026, reflecting strong second quarter execution and positive underlying demand trends. The Company also recognized net income of $26.0 million and adjusted EBITDA of $58.7 million (1). Basic and fully diluted EPS were $0.33 and $0.29 per share, respectively, for the quarter.

• DefenCath® (taurolidine and heparin) sales contributed $66.1 million of net revenue in the second quarter, driven by continued utilization of DefenCath by large outpatient dialysis customers. The acquired Melinta portfolio contributed $35.8 million.

• CorMedix announced today that in collaboration with our global development partner Mundipharma, the company anticipates FDA submission of the sNDA for an expanded indication of REZZAYO for the prophylaxis of invasive fungal disease in the third quarter of this year. Provided the application is accepted for FDA review, the Company anticipates agency action on the application in H1 2027.

• The Company signed a new multi-year commercial supply agreement for DefenCath ® with a Large Dialysis Operator (LDO), expanding the company's commercial contract footprint to include all of the top 5 providers of dialysis services in the U.S. market. The LDO has commenced ordering of DefenCath® and will begin a pilot in the third quarter this year.

• The Company maintains full-year 2026 consolidated revenue guidance of $325 to $345 million, and raises full-year adjusted EBITDA guidance to a range of $125 to $140 million. Cash OpEx guidance is narrowed to a range of $145 to $155 million.

• Cash and short-term investments, excluding restricted cash, at June 30, 2026 totaled $256.7 million.

Joseph Todisco, CorMedix Chairman & CEO, commented, "CorMedix delivered a strong second quarter, generating $101.9 million in consolidated revenue and $58.7 million of adjusted EBITDA, reflecting continued execution across our business. We remain confident in our full-year 2026 outlook and our revenue and adjusted EBITDA guidance as we continue to navigate the post-TDAPA reimbursement environment for DefenCath with discipline and focus. We also made meaningful progress across our pipeline and expect the near-term submission of the REZZAYO sNDA for prophylaxis. With a strong balance sheet, meaningful cash position, and a disciplined capital allocation strategy, we believe CorMedix is well positioned to support our commercial priorities, advance high-value development programs, and create sustainable long-term value for shareholders."

(1) Adjusted EBITDA is a non-GAAP financial measure and excludes non-cash items such as depreciation, amortization, stock-based compensation, interest and other income and expense, taxes and certain non-recurring items. See "Non-GAAP Financial Measures" on the following pages for additional information regarding the use of EBITDA and Adjusted EBITDA and a reconciliation to the most comparable GAAP measure.

Second Quarter 2026 Financial Highlights

For the second quarter of 2026, CorMedix recorded $101.9 million in consolidated revenue, comprised of $66.1 million in sales of DefenCath and $35.8 million associated with the acquired Melinta portfolio, an increase from $39.7 million in total revenue in the comparable period of 2025. DefenCath sales increased year over year largely due to the onboarding of a large dialysis organization in mid-2025. As the Melinta acquisition occurred in August 2025, the second quarter of 2025 included revenue from only sales of DefenCath.

Total operating expenses in the second quarter of 2026 were $34.2 million, compared with $18.3 million in the second quarter of 2025, an increase of approximately 87%. The increase of $15.9 million over the prior period was driven primarily by the contribution of operating expenses from the Melinta acquisition for the full quarter and reflects the larger combined company.

Research and development (R&D) expenses in the second quarter of 2026 were $6.7 million, compared with $2.4 million for the same period in 2025. The increase in R&D was primarily due to an increase in personnel and clinical trial services in support of the ongoing clinical programs, including pediatric studies for several brands and the continued investment in the development of DefenCath for the TPN indication.

Selling and marketing expense increased approximately 95% to $12.4 million in the second quarter of 2026 from $6.4 million in the second quarter of 2025. The increase was primarily due to higher personnel cost associated with the larger product portfolio and related marketing programs.

General and administrative expenses increased approximately 59% to $15.1 million in the second quarter of 2026 from $9.5 million in the second quarter of 2025. The increase was primarily attributable to higher costs associated with operating as a combined company following the acquisition, including branded prescription drug fees, and higher personnel, information technology, legal and facilities costs. This year-over-year increase in G&A was partially offset by the recognition of $4.2 million during the three months ended June 30, 2026, of expected insurance reimbursement of legal fees incurred by the Company to support its ongoing securities litigation. Of the $4.2 million credit recorded in the second quarter, $2.7 million related to legal fees that were incurred in prior periods.

CorMedix recorded net income of $26.0 million, or $0.33 and $0.29 per basic and diluted share, respectively, in the second quarter of 2026, compared with net income of $19.8 million, or $0.29 and $0.28 per basic and diluted share, respectively, in the second quarter of 2025. Also for the second quarter of 2026, CorMedix reported adjusted EBITDA of $58.7 million, compared to adjusted EBITDA of $22.4 million in the second quarter of 2025.

The Company reported cash and cash equivalents of $256.7 million at June 30, 2026, excluding restricted cash. The Company believes that it has sufficient resources to fund operations for at least twelve months from the issuance of the Company's Quarterly Report on Form 10-Q.

Conference Call Information

CorMedix will host a conference call and webcast today, August 13, 2026, at 8:30AM Eastern Time, to discuss recent corporate developments and financial results. Call details and dial-in information are as follows:

August 13, 2026 @ 8:30am ET

Domestic: 1-844-676-2922

International: 1-412-634-6840

Webcast: Webcast Link

About CorMedix

CorMedix Therapeutics is a biopharmaceutical company focused on developing and commercializing therapeutic products for the prevention and treatment of life-threatening conditions and diseases in the United States. CorMedix is focused on selling and marketing products in institutional settings of care in the US and has field based medical and commercial infrastructure deployed in hospitals, clinics and infusion centers. For more information visit: www.cormedix.com.

Forward-Looking Statements

This press release contains "forward-looking statements" within the meaning of the Private Securities Litigation Reform Act of 1995, Section 27A of the Securities Act of 1933, as amended, and Section 21E of the Securities Exchange Act of 1934, as amended, as amended (the "Exchange Act"), that are subject to risks and uncertainties. Forward-looking statements are often identified by the use of words such as, but not limited to, "anticipate," "believe," "can," "continue," "could," "estimate," "expect," "intend," "may," "plan," "project," "seek," "should," "target," "will," "would," and similar expressions or variations intended to identify forward-looking statements. All statements, other than statements of historical facts, regarding management's expectations, beliefs, goals, plans or CorMedix's prospects should be considered forward-looking statements including, but not limited to statements regarding financial and business guidance; sales, revenue and operating expense estimates; Adjusted EBITDA estimates; expectations regarding product utilization and sales; the risk that topline data from CorMedix's and its partners' clinical trials, including the ReSPECT study, that CorMedix announces or publishes from time to time may change as more patient data become available or may be interpreted differently if additional data is disclosed; estimates of total addressable market size; failure to successfully conduct future clinical trials, including due to CorMedix's or its partners' potential inability to enroll or retain sufficient patients to conduct and complete the trials or generate data necessary for regulatory approval, among other things; development of unexpected safety or efficacy concerns related to CorMedix's product candidates; expectations and timing regarding clinical trials and development, performance expectations and revenue opportunities of CorMedix's product pipeline; expectations regarding implementation and perceived benefits of CorMedix's products; continued pricing pressures and the impact of actions of governmental and private payers affecting pricing of, reimbursement for, and patient access to pharmaceuticals and reporting obligations related thereto; the expiration of intellectual property protection for certain of the company's products and competition from generic and biosimilar products. Readers are cautioned that actual results may differ materially from projections or estimates due to a variety of important factors, and readers are directed to the Risk Factors identified in CorMedix's filings with the SEC, including its most recent Annual Report on Form 10-K, copies of which are available free of charge at the SEC's website at www.sec.gov or upon request from CorMedix. CorMedix may not actually achieve the goals or plans described in its forward-looking statements, and such forward-looking statements speak only as of the date of this press release. In addition, pro forma financial information does not necessarily reflect the actual results that we would have achieved had the pro forma transaction been consummated as of the date indicated nor does it reflect the potential future results of the combined company. Investors should not place undue reliance on these statements. CorMedix assumes no obligation and does not intend to update these forward-looking statements, except as required by law.

Non-GAAP Financial Measures

This release includes certain non-GAAP financial measures, including EBITDA and adjusted EBITDA, which are intended as supplemental measures of the Company's performance that are not required by or presented in accordance with GAAP. Management uses these non-GAAP measures internally to evaluate and manage the Company's operations and to better

understand its business because they facilitate a comparative assessment of the Company's operating performance relative to its performance based on results calculated under GAAP. These non-GAAP measures also isolate the effects of some items that vary from period to period without any correlation to core operating performance and eliminate certain charges that management believes do not reflect the Company's operations and underlying operational performance.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-05_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

The Company is a biopharmaceutical
company focused on developing and commercializing therapeutic products for life-threatening diseases and conditions.

Our primary focus has been
commercializing DefenCath® (taurolidine and heparin), in the U.S., which we launched in 2024 in the hemodialysis setting. The name
DefenCath is the U.S. proprietary name approved by the U.S. FDA.

DefenCath is an FDA
approved antimicrobial CLS (a formulation of taurolidine 13.5 mg/mL, and heparin 1000 USP Units/mL) indicated to reduce the
incidence of CRBSI in adult patients with kidney failure receiving chronic hemodialysis through a CVC It is indicated for use in a
limited and specific population of patients. CRBSIs can lead to treatment delays and increased costs to the healthcare system when
they occur due to extended and often repeat hospitalizations, need for IV antibiotic treatment, long-term anticoagulation therapy,
removal/replacement of the CVC, related treatment costs, as well as increased mortality. DefenCath is the first and only
FDA-approved antimicrobial CLS in the U.S. and was shown to reduce the risk of CRBSI by up to 71% in a Phase 3 clinical study.

DefenCath is subject to Medicare
ESRD PPS, which provides bundled payment for renal dialysis services and affords a TDAPA, which provides temporary, additional payments
for certain new drugs and biologicals. TDAPA reimbursement is calculated based on 100 percent ASP (or 100 percent of wholesale acquisition
price or manufacturers' list price, respectively, if such data is unavailable). TDAPA and post-TDAPA add-on payment adjustments
for DefenCath apply for five years (with such add-on payments applying to all ESRD PPS payments for years three through five). DefenCath's
TDAPA began on July 1, 2024.

Looking forward, on July 1,
2026, DefenCath's TDAPA reimbursement transitions into a three-year, post-TDAPA Add-On Payment phase, the calculation of which is
determined and published by CMS and will be $2.37 for the third and fourth quarters of 2026. As a result of the methodology utilized by
CMS, the level of reimbursement provided to institutions treating dialysis patients will significantly decline, and as a result, we expect
a corresponding reduction to net pricing for DefenCath in the third and fourth quarters of 2026. If CMS utilizes the same methodology
to calculate the 2027 post-TDAPA Add-On Adjustment, which will be effective on January 1, 2027, we estimate the value of the Add-On Adjustment
will be three to five-times higher than that granted for the third and fourth quarters of 2026, which we expect may result in higher DefenCath
sales prices in 2027 relative to the second half 2026. After January 1, 2027, the post-TDAPA Add-On Payment will be reassessed again and
be made effective on January 1, 2028 and January 1, 2029, covering the three-year period through June 30, 2029.

Acquisition of Melinta

On August 29, 2025 (the "Closing Date"),
we completed the acquisition of Melinta. The acquisition of Melinta expanded our team, commercial platform and increased the commercial
portfolio with six marketed, hospital- and clinic-focused infectious disease products, comprised of REZZAYO® (rezafungin for injection),
MINOCIN® (minocycline) for Injection, VABOMERE® (meropenem and vaborbactam), KIMYRSA® (oritavancin), ORBACTIV® (oritavancin),
BAXDELA® (delafloxacin), and an additional well-established cardiovascular product, TOPROL-XL® (metoprolol succinate) (together,
the Melinta Portfolio. REZZAYO is currently approved for the treatment of candidemia and invasive candidiasis in adults, with an ongoing
Phase III study for the prophylaxis of invasive fungal infections in adult patients undergoing allogeneic blood and marrow transplantation.
The completion of the Phase III study for REZZAYO is expected in 2026.

The financial results of Melinta are included in
our consolidated financial statements starting on August 29, 2025. Melinta's financial results were not reflected in reported figures
in the periods preceding the Closing Date. As a result, the reported results for 2025 and 2024 are not comparable. To assist with the
discussion of 2025 and 2024 results on a comparable basis and provide more meaningful discussion, certain pro forma historical results
are included in Note 3 to the Consolidated Financial Statements included herein. This information does not purport to reflect what our
financial and operational results would have been had the acquisition been consummated at the beginning of the periods presented. In addition,
further information relating to the acquisition of Melinta is included in Note 3 to the Consolidated Financial Statements included herein.

Pursuant to the terms of the
Merger Agreement, we acquired Melinta via a merger in which Merger Sub merged with and into Melinta, with Melinta surviving as a wholly-owned
subsidiary of the Company. In consideration for the Merger, we (i) paid to the former Melinta equity holders an aggregate of $260.0 million
in cash, subject to adjustment for estimated Company Cash and estimated Working Capital as compared to the Working Capital Target (each
as defined in the Merger Agreement), and (ii) issued to certain of the former Melinta equity holders an aggregate of 3.3 million common
shares of the Company (the "Merger Shares"). In addition, in connection with the Merger, we paid $23.2 million to acquire
the Toprol XL product rights, which Melinta had licensed from a third party. The total cash consideration was funded by a combination
of the Company's existing cash on hand and net proceeds from the Company's $150.0 million aggregate principal amount of convertible
senior notes due 2030 (as described below).

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Comparison of the Years Ended December 31, 2025 and 2024

The following is a tabular
presentation of our audited consolidated operating results for the years ended December 31, 2025 and 2024 (in thousands) : Results
for 2025 are inclusive of Melinta's operations from the acquisition date of August 29, 2025 through December 31, 2025, while the
prior period does not include combined results. The below discussion of changes to our revenue and expenses compared to the prior year
largely focus on material factors independent of the acquisition.

2025 | 2024 | Net of Change Increase (Decrease)
Revenue | 304,344 | 43,472 | 600 | %
Contract Revenue | 7,365 | - | 100 | %
Total Revenue | 311,709 | 43,472 | 617 | %
Cost of sales | 22,089 | 3,034 | 628 | %
Intangible Amortization | 13,872 | 156 | 8,792 | %
Gross profit (loss) | 275,748 | 40,282 | 585 | %
Operating Expenses:
Research and development | 19,333 | 3,942 | 390 | %
Selling and marketing | 38,054 | 28,737 | 32 | %
General and administrative | 68,220 | 29,959 | 128 | %
Total operating expenses | 125,607 | 62,638 | 101 | %
Income (loss) from operations | 150,141 | (22,356 | (772 | )%
Interest income | 3,846 | 2,579 | 49 | %
Foreign exchange transaction loss | (52 | (31 | 68 | %
Unrealized gain on marketable security | 5,364 | - | 100 | %
Other Income | - | 519 | (100 | )%
Change in contingent consideration | (6,501 | - | 100 | %
Interest expense | (2,782 | (36 | 7,628 | %
Total other income (expenses) | (125 | 3,031 | (104 | )%
Income (loss) before income taxes | 150,016 | (19,325 | (876 | )%
Tax (benefit) | (13,039 | (1,395 | 835 | %
Net income (loss) | 163,055 | (17,930 | (1,009 | )%
Other comprehensive (loss) income | (88 | (3 | 2,833 | %
Comprehensive income (loss) | 162,967 | (17,933 | (1,009 | )%

Revenue. Revenue for
the year ended December 31, 2025 was $311.7 million as compared to $43.5 million for the same period in 2024, an increase of $268.2 million,
or 617%.

For the years ended December
31, 2025 and 2024, product sales were $304.3 million and $43.5 million, respectively, representing an increase of $260.8 million, or 600%.
Product sales during fiscal year 2024 and 2025 consist primarily of sales of DefenCath, which was approved by the FDA in November 2023
and launched in the U.S in April 2024 (inpatient setting) and July 2024 (outpatient setting) and reflects the shipment of DefenCath to
direct customers and specialty distributors, net of estimates for applicable variable consideration. Revenue from the Melinta Portfolio
represents $45.5 million of product sales, net of applicable variable consideration, for the post-acquisition period, starting August
29, 2025.

In 2024, we entered into multi-year
commercial supply agreements with a large and several mid-sized dialysis organizations. Each dialysis provider customized its implementation
plan to provide access to patients based on a variety of clinical and other factors. We believe the currently contracted customer base
represents roughly 60% of the outpatient dialysis centers in the U.S. in terms of the total addressable patient market. During the
second quarter of 2025, the Company's largest volume customer commenced ordering, patient utilization commenced in the third quarter
of 2025, driving significant sales growth in the second half of 2025 relative to the first half.

Contract revenue for 2025
is related solely to the acquired operations of Melinta after the Closing Date of August 29, 2025 and reflects $4.2 million earned under
the BARDA agreement and $3.2 million related to milestone, royalty, and inventory revenue under Melinta's licensing agreements.

The following is a summary
of our Total Revenue between the DefenCath sales and the contribution from the Melinta Portfolio from the Closing Date of August 29, 2025
through the end of 2025. The table below represents consolidated revenue for the year ended December 31, 2025 and 2024 (in thousands) :

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-05_item1_business.md)

Item 1. Business

Overview

CorMedix Inc. (collectively,
with our wholly owned subsidiaries, referred to herein as "we," "us," "our" or the "Company")
is a biopharmaceutical company focused on developing and commercializing therapeutic products for life-threatening diseases and conditions.
Our primary focus has been commercializing DefenCath® (taurolidine and heparin), in the U.S., which we launched in 2024 in the hemodialysis
setting. The name DefenCath is the U.S. proprietary name approved by the U.S. Food and Drug Administration ("FDA").

On August 29, 2025, the Company
acquired Melinta Therapeutics, LLC, a Delaware limited liability company ("Melinta"), which expanded the Company's
team, commercial platform and increased the commercial portfolio with six marketed, hospital- and clinic-focused infectious disease products,
comprised of REZZAYO® (rezafungin for injection), MINOCIN® (minocycline) for Injection ("MINOCIN IV"), VABOMERE®
(meropenem and vaborbactam), KIMYRSA® (oritavancin), ORBACTIV® (oritavancin), and BAXDELA® (delafloxacin), as well as an
additional well-established cardiovascular product, TOPROL-XL® (metoprolol succinate) (together, the "Melinta Portfolio,"
and, together with DefenCath, "our Products"). The Melinta Portfolio supports a multi-channel strategy of delivering anti-infectives
for serious gram-positive, gram-negative and fungal infections within hospitals and the hospital ecosystem, including emergency departments,
outpatient clinics and home infusion care, and provides synergy opportunities to drive growth for DefenCath.

Business Strategy

Our corporate strategy is focused on increasing stockholder value by
maximizing the value of our current portfolio, with promotional efforts focused on DefenCath, REZZAYO, MINOCIN IV and VABOMERE. In addition,
we seek to create additional value through the pursuit of expanded indications for both DefenCath, for the reduction of central line associated
bloodstream infection ("CLABSI") in adult patients receiving total parental nutrition ("TPN"), and REZZAYO in
the prophylaxis of invasive fungal infections in adult patients that are immune compromised. We also engage in the pursuit of business
development opportunities that could be highly synergistic with our existing or future sales infrastructure deployment.

Promoted Commercial Products

DefenCath

On November 15, 2023, we
announced that the FDA approved the new drug application ("NDA") for DefenCath, an antimicrobial catheter lock solution ("CLS")
(a formulation of taurolidine 13.5 mg/mL, and heparin 1000 USP Units/mL) indicated to reduce the incidence of catheter-related bloodstream
infections ("CRBSI") in adult patients with kidney failure receiving chronic hemodialysis through a central venous catheter
("CVC"). We launched DefenCath commercially in April 2024 in the inpatient setting and July 2024 in the outpatient hemodialysis
setting, and it is the largest contributor to our net sales.

Subsequent to the launch of DefenCath in April 2024, we announced U.S.-based
multi-year commercial supply agreements consisting of a large and several mid-sized dialysis organizations. Each customer has customized
an implementation plan to provide access to their patients based on a variety of clinical and other factors. We believe the currently
contracted customer base represents roughly 60% of the outpatient dialysis centers in the U.S., in terms of the total addressable patient
market.

Market Opportunity

CVCs or 'central lines'
are an important and frequently used method for accessing the vasculature for hemodialysis (a form of dialysis where the patient's
blood is circulated through a dialysis filter), administering chemotherapy and basic fluids in cancer patients and for cancer chemotherapy,
administering long term antibiotic therapy, and administering total parenteral nutrition (complete or partial dietary support via intravenous
nutrients).

Bloodstream infections resulting from the use of central venous catheters
known as CLABSIs and a subset of them, referred to as CRBSIs, can result in significant morbidity and increased rates of hospital admissions,
readmissions, and mortality. One of the major and common risk factors for all patients requiring CVCs is the risk of acquiring a CLABSI
and the clinical complications associated with them. The total annual cost for treating outpatient derived CRBSI episodes and their related
complications in the U.S. is up to $2.3 billion, with approximately 80,000 CRBSI episodes and up to 28,000 deaths per year (Pronovost
et al., The New England Journal of Medicine , 2006).

According to the 2025 United States Renal Disease System, reporting
data from 2023, there were approximately 485,000 End-Stage-Renal-Disease ("ESRD") patients on permanent hemodialysis in the
U.S. and over 25% of these utilized a CVC for vascular access. Of the total population, approximately 108,000 hemodialysis patients were
new patients diagnosed with ESRD during the year and 80% of those were receiving dialysis through a CVC. Patients are typically treated
in various care settings including inpatient hospitals and outpatient dialysis clinics. Kidney failure patients can include both those
affected by acute kidney injury and chronic kidney disease populations that progress into dialysis. Kidney failure patients who are admitted
to the hospital have an average length of stay of approximately two weeks and additionally high 30-day readmission rates both for the
same diagnosis and all-cause with the all-cause readmissions being higher.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

- **CALL PERIOD: 2026Q2** (call dated 2026-08-13)
- **Recency:** same fiscal period as the latest earnings release in this pack.
- **File:** transcript_2026Q2_2026-08-13.md
- **Type:** EARNINGS PRESS RELEASE ONLY, not the call — no Q&A, no unscripted management commentary. Do not attribute call quotes to this.
- **Source:** https://www.sec.gov/Archives/edgar/data/1410098/000141009826000054/crmd_q22026earningspr.htm

_Body not repeated: this file is the same press release already excerpted in section 7._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-05_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-05_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-05_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-13_2-02-results.md, 10-K_2026-03-05_item7_mdna.md, 10-K_2026-03-05_item1_business.md, transcript_2026Q2_2026-08-13.md

**Missing:** none

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
