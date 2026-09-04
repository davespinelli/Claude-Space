# Triage pack — ELMD · Electromed, Inc.

_Generated 2026-09-04 13:14 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** ELMD · **Name:** Electromed, Inc.
- **CIK:** 0001488917
- **SIC:** 3845 — Electromedical & Electrotherapeutic Apparatus
- **Fiscal year end (MM-DD):** 06-30
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/ELMD

**Fetcher warnings for this ticker:** 10-K 2026-08-25: heading split missed Item 1A - Risk Factors

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Electromed, Inc.
- **CIK:** 1,488,917 · **SIC:** 3845 (Electromedical & Electrotherapeutic Apparatus) · **Exchange:** NYSE

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 27.61 |
| mktcap | $228.6M |
| ev | $208.2M |
| ev_ebit | 21.5x |
| fcf | $11.1M |
| fcf_yield | 4.9% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 22.8% |
| net_debt | -$20.4M |
| net_debt_ebit | -2.1x |
| cash | $20.4M |
| ltd | $0.00 |
| equity | $54.0M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $64.0M |
| revenue_prior | $54.7M |
| rev_growth | 17.0% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $9.7M |
| net_income | $7.5M |
| cfo | $11.4M |
| capex | $262k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -1.3% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 8,280,064 |
| shares_py | 8,386,115 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 75.6% |
| r6m | 13.2% |
| off_52w_high | -40.4% |
| adv20 | $3.6M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.49 |
| r_ev_ebit | 0.41 |
| r_roic | 0.90 |
| r_rev_growth | 0.79 |
| r_buyback | 0.76 |
| score | 0.72 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q2I |
| shares_period | CY2026Q1I |
| shares_py_period | CY2025Q1I |
| capex_missing | False |
| ltd_missing | True |

**Other screen columns**

| metric | value |
|---|---|
| rank | 49 |

**Screen rationale:** high ROIC 22.8%; revenue +17.0%; buying back stock -1.3%; debt data missing (net cash unverified); 12-1 momentum 75.6%


## 3. Share count trend

- Shares outstanding: **8,280,064** (CY2026Q1I) vs **8,386,115** prior year (CY2025Q1I)
- Change: **-1.3%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-25** — Item 5.02 (officer / director change or comp arrangement): On August 25, 2026, James L. Cunniff, President and Chief Executive Officer of the Company, notified the Company of his intention to retire from the Company effective on or about April 2, 2027.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 61,501 sh / $2,202,390 -> net $-2,202,390 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 28 (open-market buys 0, sales 9).

| code | rows |
|---|---|
| A | 8 |
| F | 3 |
| M | 8 |
| S | 9 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-25_2-02-results.md)

_Extraction: started at the first release heading, 'Q4 FY 2026 Company Highlights'; skipped 21 forward-looking-statement block(s); 7 block(s) of pre-heading matter dropped._

## EX-99.1 - EXHIBIT 99.1 (ex_964461.htm)

Q4 FY 2026 Company Highlights

● | Net revenue increased 11.6% to a record $ 19.4 million in Q4 FY 2026, from $ 17.4 million in the fourth quarter of the prior fiscal year.

● | Operating income increased 25.8% over the prior year to a record $ 3.8 million, or 19.7% of net revenues.

● | Net income increased 54.3% to a record $ 3.4 million, or $ 0.39 per diluted share, compared to $ 2.2 million, or $ 0.25 per diluted share, in the fourth quarter of the prior fiscal year.

FY 2026 Company Highlights

● | Net revenue increased 15.3% to a record $ 73.8 million in FY 2026, from $ 64.0 million in the prior fiscal year.

● | Operating income increased 43.7% over the prior year to a record $ 13.9 million, or 18.8% of net revenues.

● | Net income was $ 11.3 million, or $ 1.30 per diluted share, compared to $ 7.5 million, or $ 0.85 per diluted share, in the prior fiscal year.

● | Cash provided by operations totaled $ 9.7 million in FY 2026, compared to $11.4 million in the prior fiscal year.

● | Electromed repurchased $ 3.9 million of its common stock throughout FY 2026.

"Fiscal 2026 was another exceptional year for Electromed, as the company generated record revenues and profits. The fourth fiscal quarter marked our 15th consecutive quarter of year-over-year revenue and profit growth. Also, our operating margin increased more than 370 basis points over FY 2025, which demonstrates our continued success in driving operational leverage. Our strong financial performance, combined with strategic investments in our sales force, systems, and bronchiectasis market development initiatives, positions us to capitalize on the opportunity to serve the approximately 800,000 diagnosed bronchiectasis patients who could benefit from our SmartVest® therapy. Our robust balance sheet with $ 20.5 million in cash, and recognition as one of Minnesota's fastest-growing public companies has Electromed well-positioned for durable, long-term growth and value creation for our investors."

Q4 FY 2026 Results

All amounts below are for the three months ended June 30, 2026 , and compare to the three months ended June 30, 2025 .

Net revenues grew 11.6% to $ 19.4 million from $ 17.4 million.

Revenue in our direct homecare business increased 15.2% to $ 17.7 million from $ 15.4 million. The increase in revenue was primarily due to an increase in direct sales representatives, increased sales representative productivity, and higher net revenues per approval.

Gross profit increased to $ 15.3 million or 78.7% of net revenues from $ 13.6 million or 78.3% of net revenues. The increase in gross profit and gross margin was primarily due to increased revenue and higher net revenue per device.

Selling, general and administrative ("SG&A") expenses were $ 11.1 million, representing an increase of $ 0.8 million or 8.3% . The increase in the current period was primarily due to the increased salaries and incentive compensation related to the higher average number of personnel in the sales, sales support, marketing, and reimbursement teams to process higher patient referrals.

Operating income was $ 3.8 million or 19.7% of net revenues, compared to $ 3.0 million, or 17.5% of net revenues. This increase in operating income was primarily due to increases in revenue and gross profit.

Net income increased by 54.3% to $ 3.4 million, or $ 0.39 per diluted share, compared to $ 2.2 million, or $ 0.25 per diluted share.

FY 2026 Summary

All amounts below are for the year ended June 30, 2026 ("fiscal 2026") and compare to the fiscal year ended June 30, 2025 ("fiscal 2025").

Net revenues for fiscal 2026 grew by 15.3% to a record $ 73.8 million, from $ 64.0 million in fiscal 2025.

Revenue in our direct homecare market increased year-over-year by 16.3% to $ 66.6 million, from $ 57.3 million. The increase in revenue was due to an increase in direct sales representatives, increased sales representative productivity, and higher net revenues per approval. For the year ended June 30, 2026, we averaged 58 homecare field sales representatives. The homecare revenue per weighted average direct sales representative was $1,145,000, exceeding Electromed's target range for the year of $1,000,000 to $1,100,000.

Revenue in our non-homecare business grew to $ 7.2 million in fiscal 2026, an increase of $ 0.5 million, or 6.7% , from $ 6.7 million in fiscal 2025. The increase was primarily due to increased distributor and hospital revenue.

Gross profit increased to $ 57.9 million, or 78.5% of net revenues in fiscal 2026, from $ 50.0 million, or 78.1% of net revenues, in fiscal 2025. The increase in gross profit and gross margin was primarily due to increased revenue and higher net revenue per device.

Selling, general and administrative ("SG&A") expenses were $ 42.7 million in fiscal 2026, representing an increase of $ 3.4 million or 8.7% from $ 39.3 million in fiscal 2025. The increase was primarily due to increased salaries and incentive compensation related to the higher average number of personnel in the sales, sales support, marketing, and reimbursement teams to process more patient referrals.

Operating income was $ 13.9 million or 18.8% of net revenues in fiscal 2026, compared to $ 9.7 million, or 15.1% of net revenues in fiscal 2025. This increase in operating income was primarily due to increases in net revenues and gross profit.

Net income for fiscal 2026 was $ 11.3 million, or $ 1.30 per diluted share, compared to $ 7.5 million, or $ 0.85 per diluted share in fiscal 2025.

As of June 30, 2026 , Electromed had $ 20.5 million in cash, $ 29.8 million in accounts receivable and no debt, achieving working capital of $ 45.1 million and total shareholders' equity of $ 54.0 million. The cash balance reflects an increase of $ 5.2 million for the twelve months ended June 30, 2026 , compared to a decrease in cash of $0.8 million in the twelve months ended June 30, 2025. The increase in cash for the twelve months ended June 30, 2026 , was driven primarily by positive operating cash flow of $9.7 million, partially offset by share repurchases of $3.9 million of Electromed common stock.

Conference Call and Webcast Information

The conference call with members of Electromed management will be held at 5:00 p.m. Eastern Time on Tuesday, August 25, 2026.

Interested parties may participate in the call by dialing (877) 407-3982 (Domestic) or (201) 493-6780 (International).

The live conference call webcast will be accessible in the Investor Relations section of Electromed's website and directly via the following link: https://viavid.webcasts.com/starthere.jsp?ei=1770216&tp_key=c0342b57c3

For those who cannot listen to the live broadcast, a replay will be available by dialing (844) 512-2921 (Domestic) or (412) 317-6671 (International) and referencing the replay pin number 13761827. Additionally, an online replay will be available for at least one year in the Investor Relations section of Electromed's web site at: https://investors.smartvest.com/events-and-presentations/default.aspx

About Electromed, Inc.

Electromed, Inc. manufactures, markets, and sells products that provide airway clearance therapy, including the SmartVest® Airway Clearance System, to patients with compromised pulmonary function. It is headquartered in New Prague, Minnesota, and was founded in 1992. Further information about Electromed can be found at www.smartvest.com.

Electromed, Inc.

Condensed Balance Sheets

As of June 30,
2026 | 2025
Assets
Current Assets
Cash and cash equivalents | 20,450,000 | 15,287,000
Accounts receivable (net of allowances for credit losses of $45,000) | 29,805,000 | 24,660,000
Contract assets | 1,094,000 | 1,036,000
Inventories | 3,681,000 | 3,299,000
Prepaid expenses and other current assets | 1,170,000 | 392,000
Income tax receivable | 1,168,000 | 408,000
Total current assets | 57,368,000 | 45,082,000
Property and equipment, net | 5,214,000 | 4,714,000
Finite-life intangible assets, net | 379,000 | 371,000
Other assets | 1,270,000 | 1,173,000
Deferred income taxes | 2,036,000 | 2,462,000
Total assets | 66,267,000 | 53,802,000
Liabilities and Shareholders' Equity
Current Liabilities
Accounts payable | 2,643,000 | 2,667,000
Accrued compensation | 6,071,000 | 5,079,000
Warranty reserve | 1,899,000 | 1,645,000
Other accrued liabilities | 1,609,000 | 1,077,000
Total current liabilities | 12,222,000 | 10,468,000
Other long-term liabilities | 66,000 | 125,000
Total liabilities | 12,288,000 | 10,593,000
Shareholders' Equity
Common stock, $0.01 par value per share, 13,000,000 shares authorized; 8,366,163 and 8,349,176 shares issued and outstanding, as of June 30, 2026, and June 30, 2025, respectively | 84,000 | 83,000
Additional paid-in capital | 25,331,000 | 21,941,000
Retained earnings | 28,564,000 | 21,185,000
Total shareholders' equity | 53,979,000 | 43,209,000
Total liabilities and shareholders' equity | 66,267,000 | 53,802,000

Electromed, Inc.

Condensed Statements of Operations

Three Months Ended | Year Ended
June 30, | June 30,
2026 | 2025 | 2026 | 2025
(Unaudited) | (Unaudited)
Net revenues | 19,417,000 | 17,393,000 | 73,776,000 | 64,000,000
Cost of revenues | 4,133,000 | 3,769,000 | 15,833,000 | 14,029,000
Gross profit | 15,284,000 | 13,624,000 | 57,943,000 | 49,971,000
Operating expenses
Selling, general and administrative | 11,131,000 | 10,282,000 | 42,748,000 | 39,315,000
Research and development | 328,000 | 302,000 | 1,314,000 | 996,000
Total operating expenses | 11,459,000 | 10,584,000 | 44,062,000 | 40,311,000
Operating income | 3,825,000 | 3,040,000 | 13,881,000 | 9,660,000
Interest income, net | 136,000 | 135,000 | 479,000 | 624,000
Net income before income taxes | 3,961,000 | 3,175,000 | 14,360,000 | 10,284,000
Income tax expense | 560,000 | 971,000 | 3,059,000 | 2,747,000
Net income | 3,401,000 | 2,204,000 | 11,301,000 | 7,537,000
Income per share:
Basic | 0.41 | 0.26 | 1.37 | 0.89
Diluted | 0.39 | 0.25 | 1.30 | 0.85
Weighted-average common shares outstanding:
Basic | 8,258,440 | 8,334,821 | 8,266,071 | 8,454,100
Diluted | 8,734,188 | 8,718,900 | 8,688,563 | 8,914,421

Electromed, Inc.

Condensed Statements of Cash Flows

Years Ended June 30,
2026 | 2025
Cash Flows from Operating Activities
Net income | 11,301,000 | 7,537,000
Adjustments to reconcile net income to net cash provided by operating activities:
Depreciation | 868,000 | 1,039,000
Impairment of intangible assets | — | 212,000
Amortization | 208,000 | 133,000
Share-based compensation expense | 2,722,000 | 3,059,000
Deferred income taxes | 426,000 | (310,000
Changes in operating assets and liabilities:
Accounts receivable | (5,145,000 | (1,327,000
Contract assets | (58,000 | (317,000
Inventories | (517,000 | 175,000
Prepaid expenses and other assets | (1,024,000 | (959,000
Income tax receivable, net | (760,000 | (685,000
Accounts payable and accrued liabilities | 652,000 | 1,650,000
Accrued compensation | 992,000 | 1,186,000
Net cash provided by operating activities | 9,665,000 | 11,393,000
Cash Flows from Investing Activities
Expenditures for property and equipment | (1,252,000 | (262,000
Expenditures for finite-life intangible assets | (48,000 | (44,000
Net cash used for investing activities | (1,300,000 | (306,000
Cash Flows from Financing Activities
Issuance of common stock upon exercise of options | 965,000 | 398,000
Taxes paid on net share settlement of stock awards | (249,000 | (2,278,000
Repurchase of common stock | (3,918,000 | (10,000,000
Net cash used for financing activities | (3,202,000 | (11,880,000
Net increase (decrease) in cash | 5,163,000 | (793,000
Cash and cash equivalents
Beginning of period | 15,287,000 | 16,080,000
End of period | 20,450,000 | 15,287,000

## EX-99.2 - EXHIBIT 99.2 (ex_1006919.htm)

EX-99.2
ex_1006919.htm
EXHIBIT 99.2

Image Exhibit

Exhibit 99.2

Electromed, Inc. Investor Presentation August 25, 2026 NYSE American: ELMD Innovation Leader in Airway Clearance Technologies

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-08-25_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

Overview

Electromed develops and provides innovative airway clearance products applying HFCWO technologies in pulmonary care for patients of all ages.

We manufacture, market and sell products that provide HFCWO, including the SmartVest System that includes our newest generation SmartVest Clearway, previous generation SmartVest SQL and related products, to patients with compromised pulmonary function. The SmartVest Clearway is an updated and modern approach to HFCWO focused on an enhanced patient experience and proven patient outcomes. The product delivers effective 360 o oscillatory pressure through our proprietary rapid inflate-deflate technology which improves the patient's ability to breathe deeply during therapy. SmartVest Clearway delivers a sleek and lightweight generator and is designed with an intuitive touchscreen to simplify programing and everyday use. Our products are sold in both the homecare market and the hospital market. The SmartVest SQL has been sold in the domestic homecare market since 2014. In 2015, we launched the SmartVest SQL into hospital and certain international markets. In June 2017, we announced the launch of the SmartVest SQL with SmartVest Connect™ wireless technology, which allows data connection between physicians and patients to track therapy performance and collaborate in treatment decisions. In 2022, we launched the SmartVest Clearway to adult pulmonary, pediatric and cystic fibrosis patients for use in the home. We have marketed the SmartVest System and its predecessor products since 2000 to patients suffering from cystic fibrosis, bronchiectasis and repeated episodes of pneumonia. Additionally, we offer our products to a patient population that includes neuromuscular disorders such as cerebral palsy, muscular dystrophies, ALS, and patients with post-surgical complications or who are ventilator dependent or have other conditions involving excess secretion and impaired mucus transport.

The SmartVest System is often eligible for reimbursement from major private insurance providers, health maintenance organizations ("HMOs"), state Medicaid systems, and the federal Medicare system, which we believe is an important consideration for patients considering an HFCWO course of therapy. For domestic sales, the SmartVest System may be reimbursed under the Medicare-assigned billing code (E0483) for HFCWO devices if the patient has cystic fibrosis, bronchiectasis (including chronic bronchitis or COPD that has resulted in a diagnosis of bronchiectasis), or any one of certain enumerated neuromuscular diseases, and can demonstrate that another less expensive physical or mechanical treatment did not adequately mobilize retained secretions. Private payers consider a variety of sources, including Medicare, as guidelines in setting their coverage policies and payment amounts.

We have primarily employed a direct-to-patient and provider model, through which we obtain patient referrals from clinicians, manage insurance claims on behalf of our patients and their clinicians, deliver our solutions to patients and train them on proper use in their homes. This model allows us to directly approach patients and clinicians, whereby we disintermediate the traditional HME distributors and capture both the manufacturer and distributor margins. We have engaged a limited number of regional HME distributors focused on respiratory therapies as an alternate sales channel.

Our key growth strategies for fiscal 2027 are to accelerate our revenue growth by taking market share and expanding the addressable population for the largest and fastest growing segments of the market: adult pulmonology/bronchiectasis. Actions to support accelerating our revenue growth in this area include the following:

● | Expand our sales force in geographies with high potential, adding additional territories with direct sales reps;

● | Increase SmartVest brand awareness through direct-to-consumer and physician marketing, and peer-to-peer education;

● | Provide best-in-class customer care and support; and

● | Develop and promulgate the body of bronchiectasis clinical evidence to increase physician adoption of the SmartVest System for patients.

Impacts of Certain Macro-Economic Conditions and the Supply Chain on Our Business and Operations

We expect that component and raw material costs will continue to be a challenge in fiscal 2027, due to supply chain constraints, rising energy costs due to ongoing geopolitical conflict, uncertainty related to trade regulations such as tariffs, and inflationary trends in electronic components. In certain instances, we have purchased key materials in advance to ensure adequate future supply and mitigate the risk of potential supply chain disruptions. It is possible that these macro-economic conditions could have a greater adverse impact on our supply chain in the future, including impacts associated with preventative and precautionary measures taken by other businesses and applicable governments. A reduction or further interruption in any of our manufacturing processes, significant changes in trade regulations, or rising energy prices could have a material adverse effect on our business. Any significant increases to our raw material or shipping costs would reduce our gross margins.

Critical Accounting Estimates

During the preparation of our financial statements, we are required to make estimates, assumptions and judgment that affect reported amounts. Those estimates and assumptions affect our reported amounts of assets and liabilities, our disclosure of contingent assets and liabilities, and our reported revenues and expenses. We update these estimates, assumptions, and judgments as appropriate. Some of our accounting policies and estimates require us to exercise significant judgment in selecting the appropriate assumptions for calculating financial statements. Such judgments are subject to an inherent degree of uncertainty. Among other factors, these judgments are based upon our historical experience, known trends in our industry, terms of existing contracts and other information from outside sources, as appropriate. The following is a summary of our primary critical accounting policies and estimates. See also Note 1 to the Financial Statements, included in Part II, Item 8, of this Annual Report on Form 10-K.

Revenue Recognition

Revenue is measured based on consideration specified in the contract with a customer, adjusted for any applicable estimates of variable consideration and other factors affecting the transaction price, including consideration paid or payable to customers and significant financing components. Revenue from all customers is recognized when a performance obligation is satisfied by transferring control of a distinct good or service to a customer.

Individual promised goods and services in a contract are considered a performance obligation and accounted for separately if the individual good or service is distinct (i.e., the customer can benefit from the good or service on its own or with other resources that are readily available to the customer and the good or service is separately identifiable from other promises in the arrangement). If an arrangement includes multiple performance obligations, the consideration is allocated between the performance obligations in proportion to their estimated standalone selling price, unless discounts or variable consideration is attributable to one or more but not all the performance obligations. Costs related to products delivered are recognized in the period incurred, unless criteria for capitalization of costs under Accounting Standards Codification ("ASC") 340-40, "Other Assets and Deferred Costs," or the requirements under other applicable accounting guidance are met.

We include shipping and handling fees in net revenues. Shipping and handling costs associated with the shipment of our SmartVest System after control has transferred to a customer are accounted for as a fulfillment cost and are included in cost of revenues.

We request that customers return previously sold units that are no longer in use to us to limit the possibility that such units would be resold by unauthorized parties or used by individuals without a prescription. The customer is under no obligation to return the product; however, we do reclaim many previously sold units upon the discontinuance of patient usage. We are certified to recondition and resell returned SmartVest System units. Returned units are typically reconditioned and resold or used for demonstration equipment and warranty replacement parts.

Results of Operations

Fiscal Year Ended June 30, 2026 Compared to Fiscal Year Ended June 30, 2025

Revenues

Revenue for the fiscal years ended June 30, 2026, and 2025 are summarized in the table below.

Fiscal Year Ended June 30,
2026 | 2025 | Increase (Decrease)
Homecare Revenue | 66,612,000 | 57,287,000 | 9,325,000 | 16.3 | %
Hospital Revenue | 3,442,000 | 3,140,000 | 302,000 | 9.6 | %
Homecare Distributor Revenue | 3,301,000 | 2,928,000 | 373,000 | 12.7 | %
Other Revenue | 421,000 | 645,000 | (224,000 | (34.7 | )%
Total Revenue | 73,776,000 | 64,000,000 | 9,776,000 | 15.3 | %

Homecare Revenue. Homecare revenue increased by $9,325,000, or 16.3%, in fiscal 2026 compared to fiscal 2025. Approximately $7,959,000 of the increase in revenue was due to higher volume, which was driven by additional sales representatives and increased sales representative productivity, and approximately $1,366,000 was due to higher net revenues per approval. For the year ended June 30, 2026, we averaged 58 homecare field sales representatives compared to an average of 54 for the year ended June 30, 2025.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-08-25_item1_business.md)

Item 1. | Business.

Overview

Electromed, Inc. ("we," "our," "us," "Electromed" or the "Company") develops, manufactures, markets and sells innovative products that provide airway clearance therapy, including the SmartVest ® Airway Clearance System ("SmartVest System") to patients with compromised pulmonary function with a commitment to excellence and compassionate service. Our goal is to make High Frequency Chest Wall Oscillation ("HFCWO") treatments as effective, convenient, and comfortable as possible, so our patients can breathe easier and live better with improved respiratory function and fewer exacerbations.

We primarily employ a direct-to-patient and provider model, through which we obtain patient referrals from clinicians, manage insurance claims on behalf of our patients, and deliver the SmartVest System to patients, training them on proper use in their homes. This model allows us to directly approach patients and clinicians, whereby we disintermediate the traditional home medical equipment ("HME") channel and capture both the manufacturer and distributor margins. We also sell our products in the acute care setting for patients in a post-surgical or intensive care unit, or who were admitted for a lung infection brought on by compromised airway clearance. Electromed was incorporated in Minnesota in 1992. Our common stock is listed on the NYSE American under the ticker symbol "ELMD."

The SmartVest System generates HFCWO, an airway clearance therapy. The SmartVest System features a programmable air pulse generator, a therapy garment worn over the upper body and a connecting hose, which together provide safe, comfortable, and effective therapy to clear the lung and airway from retained secretions and mucus which can harbor bacteria and lead to infection. One important factor of respiratory health is the ability to clear secretions from airways. Impaired airway clearance, when mucus cannot be expectorated, may result in labored breathing, inflammatory response and/or immune systems boosting mucus production that invites bacteria trapped in stagnant secretions to cause infections. Studies show that HFCWO therapy is as effective an airway clearance method for patients who have compromised pulmonary function as traditional chest physical therapy ("CPT") administered by a respiratory therapist. 1 However, HFCWO can be self-administered, relieving a caregiver of participation in the therapy, and eliminating the attendant cost of an in-home care provider. We believe that HFCWO treatments are cost-effective primarily because they reduce a patient's risk of respiratory infections and other secondary complications that are associated with impaired airway clearance and often result in costly hospital visits and repeated antibiotic use.

The SmartVest System is designed for patient comfort and ease of use which promotes adherence to prescribed treatment schedules, leading to improved airway clearance, patient outcomes and quality of life, and a reduction in healthcare utilization. We offer a broad range of garments, referred to as vests and wraps, in sizes for children and adults that allow for a tailored fit. User-friendly controls allow patients to administer their daily therapy with minimal or no assistance. Our direct product support services provide patient and clinician education, training, and follow-up to ensure that the product is integrated into each patient's daily treatment regimen. Additionally, our reimbursement department works on behalf of the patient by processing their physician paperwork, providing clinical support and billing the applicable insurance provider. We believe that the advantages of the SmartVest System and Electromed's customer service to the patient include:

● | improved quality of life;

● | reduction in healthcare utilization;

● | independence from a dedicated caregiver;

● | consistent treatments at home;

● | improved comfort during therapy; and

● | eligibility for reimbursement by private insurance, federal or state government programs or combinations of the foregoing.

1 Nicolini A, et al. Effectiveness of treatment with high-frequency chest wall oscillation in patients with bronchiectasis. BMC Pulmonary Medicine. 2013;13(21) .

Our Products

Since 2000, we have marketed the SmartVest System and its predecessor products to patients suffering from bronchiectasis, cystic fibrosis, and neuromuscular conditions such as cerebral palsy and amyotrophic lateral sclerosis ("ALS"). Our products are sold into the home health care market and the acute care setting for patients in a post-surgical or intensive care unit, or who were admitted for a lung infection brought on by compromised airway clearance. Accordingly, our sales points of contact include adult pulmonology clinics, cystic fibrosis centers, neuromuscular clinics and hospitals.

We have received clearance from the U.S. Food and Drug Administration ("FDA") to market the SmartVest System to promote airway clearance and improve bronchial drainage. In addition, Electromed is approved for HFCWO device sales in other, select international countries. The SmartVest System is available only with a physician's prescription.

The SmartVest System is currently available in two models, SmartVest SQL ® and SmartVest Clearway ® , which are sold into homecare and hospital markets. In November 2022, we announced the introduction of SmartVest Clearway ® , our next generation HFCWO system designed around an enhanced patient experience and modern design. We will continue to support and service earlier SmartVest models pursuant to the applicable product warranty. As part of our growth strategies, we evaluate opportunities involving products and services, especially those that may provide value to the respiratory homecare and hospital market.

The SmartVest Clearway System

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-08-25_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-08-25_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | **MISSING** |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-25_2-02-results.md, 10-K_2026-08-25_item7_mdna.md, 10-K_2026-08-25_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
