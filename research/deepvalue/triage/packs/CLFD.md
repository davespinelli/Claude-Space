# Triage pack — CLFD · Clearfield, Inc.

_Generated 2026-09-04 18:10 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** CLFD · **Name:** Clearfield, Inc.
- **CIK:** 0000796505
- **SIC:** 3661 — Telephone & Telegraph Apparatus
- **Fiscal year end (MM-DD):** 09-30
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/CLFD

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Clearfield, Inc.
- **CIK:** 796,505 · **SIC:** 3661 (Telephone & Telegraph Apparatus) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 28.32 |
| mktcap | $384.7M |
| ev | $364.2M |
| ev_ebit | 172.0x |
| fcf | $17.5M |
| fcf_yield | 4.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 0.7% |
| net_debt | -$20.4M |
| net_debt_ebit | -9.7x |
| cash | $20.4M |
| ltd | $0.00 |
| equity | $245.9M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $150.1M |
| revenue_prior | $125.6M |
| rev_growth | 19.6% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $2.1M |
| net_income | -$8.1M |
| cfo | $22.2M |
| capex | $4.7M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -1.6% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 13,583,955 |
| shares_py | 13,806,049 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 6.7% |
| r6m | -8.2% |
| off_52w_high | -44.8% |
| adv20 | $5.2M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.46 |
| r_ev_ebit | 0.04 |
| r_roic | 0.34 |
| r_rev_growth | 0.82 |
| r_buyback | 0.77 |
| score | 0.54 |

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

**Other screen columns**

| metric | value |
|---|---|
| rank | 211 |

**Screen rationale:** revenue +19.6%; buying back stock -1.6%; debt data missing (net cash unverified); 12-1 momentum 6.7%


## 3. Share count trend

- Shares outstanding: **13,583,955** (CY2026Q2I) vs **13,806,049** prior year (CY2025Q2I)
- Change: **-1.6%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-28** — Item 1.01 (Entry into a Material Definitive Agreement): into an Amendment No. 4 to Loan Agreement (the "Amendment") that amends its Loan Agreement dated April 27, 2022 (as amended,
- **2026-04-30** — Item 1.01 (Entry into a Material Definitive Agreement): into an Amendment No. 3 to Loan Agreement (the "Amendment") that amends its Loan Agreement dated April 27, 2022 (as amended,

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 23,353 sh / $1,039,324 -> net $-1,039,324 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 13 (open-market buys 0, sales 7).

| code | rows |
|---|---|
| A | 5 |
| F | 1 |
| S | 7 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-05_2-02-results.md)

_Extraction: started at the first release heading, 'Clearfield Reports Third Quarter Fiscal 2026 Results'; skipped 7 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99.1 - PRESS RELEASE (exh_991.htm)

Clearfield Reports Third Quarter Fiscal 2026 Results

Net sales from continuing operations of $43.9 million and net income per share from continuing operations of $0.22

Received first significant order for $22 million to support a hyperscale data center project after the close of the quarter; expect to begin shipments in early fiscal 2027

Share buybacks totaled $0.9 million with $15.0 million remaining available for repurchase

MINNEAPOLIS, Aug. 05, 2026 (GLOBE NEWSWIRE) -- Clearfield, Inc. (NASDAQ: CLFD), a leader in fiber connectivity, reported results for the fiscal third quarter of 2026. Additional commentary is provided in a letter to shareholders available in the Investor Relations section of the Company's website.

Fiscal Q3 2026 Financial Summary
(in millions except per share data and percentages) | Q3 2026 | vs. Q3 2025 | Change | Change (%)
Net Sales from Continuing Operations | 43.9 | 38.8 | 5.1 | 13%
Gross Profit ($) from Continuing Operations | 13.9 | 13.7 | 0.3 | 2%
Gross Profit (%) from Continuing Operations | 31.8 % | 35.3% | -3.5% | -10%
Income from Operations from Continuing Operations | 2.6 | 1.5 | 1.0 | 68%
Income Tax Expense from Continuing Operations | 0.9 | 0.8 | 0.1 | 19%
Net Income from Continuing Operations | 3.0 | 2.3 | 0.7 | 29%
Net Income per Diluted Share from Continuing Operations | 0.22 | 0.16 | 0.06 | 38%
Net Loss from Discontinued Operations, net of tax | - | (0.7 | 0.7 | 100%
Net Loss per Diluted Share from Discontinued Operations | - | (0.05 | 0.05 | 100%
Consolidated Net Income Per Diluted Share | 0.22 | 0.11 | 0.11 | 100%

Fiscal Q3 YTD 2026 Financial Summary
(in millions except per share data and percentages) | 2026 YTD | vs. 2025 YTD | Change | Change (%)
Net Sales from Continuing Operations | 112.6 | 109.1 | 3.5 | 3%
Gross Profit ($) from Continuing Operations | 36.5 | 36.3 | 0.2 | 0%
Gross Profit (%) from Continuing Operations | 32.4 % | 33.3% | -0.9% | -3%
(Loss) Income from Operations from Continuing Operations | (1.3 | 1.2 | (2.5 | -214%
Income Tax Expense from Continuing Operations | 0.8 | 1.6 | (0.8 | -52%
Net Income from Continuing Operations | 2.2 | 4.5 | (2.3 | -51%
Net Income per Diluted Share from Continuing Operations | 0.16 | 0.32 | (0.16 | -50%
Net Loss from Discontinued Operations, net of tax | (0.3 | (3.5 | 3.2 | 90%
Net Loss per Diluted Share from Discontinued Operations | (0.02 | (0.25 | 0.23 | 92%
Consolidated Net Income Per Diluted Share | 0.14 | 0.07 | 0.07 | 100%

Management Commentary

"As we continue to execute on our core business, we are increasingly focused on positioning the Company for its next phase of growth. That progress was highlighted shortly after the close of the third quarter, when we received our first significant order for $22 million to support a hyperscale data center project," said Company President and Chief Executive Officer, Cheri Beranek. "We remain focused on executing our strategy of promoting the expertise Clearfield has built in fiber connectivity, fiber management and labor-saving network design well beyond our traditional broadband markets. At the same time, we remain committed to the customers and communities that have always defined Clearfield."

"Our balance sheet and strong cash generation continue to provide the flexibility to invest in meaningful long-term growth opportunities," said Chief Financial Officer, Dan Herzog. "As customer demand evolves, we believe Clearfield is well positioned to capitalize on opportunities across both broadband and data center connectivity."

Financial Results for the Three Months Ended June 30, 2026

Net sales from continuing operations for the second quarter of fiscal 2026 increased 13% to $43.9 million from $38.8 million in the same year-ago quarter.

As of June 30, 2026, order backlog (defined as purchase orders received but not yet fulfilled) was $21.0 million, a decrease of $10.6 million, or 34%, compared to $31.6 million as of March 31, 2026, and a decrease of $9.7 million, or 32%, from June 30, 2025. The June 30, 2026 order backlog balance reflects the removal of a previously booked order of $4.6 million the Company no longer expects to fulfill.

Gross margin from continuing operations for the third quarter of fiscal 2026 was 31.8%, down from 35.3% in the prior year's third quarter and down slightly from 32.5% in the second quarter of fiscal 2026. Gross margin for the quarter included a $2.6 million inventory charge, or approximately 5.9 percentage points, related to inventory associated with the order the Company no longer expects to fulfill. Gross margin for the quarter also benefited from $1.4 million of inventory recoveries, offset by $282,000 of inventory provision, which together increased gross margin by $1.1 million, or approximately 2.6 percentage points. Additionally, the Company recognized tariff recoveries of $655,000 during the quarter, which increased gross margin by approximately 1.5 percentage points. The Company does not expect tariff recoveries to recur in future periods, as they relate to previously paid tariffs that have been refunded following a change in tariff regulations. On a net basis, these items reduced gross margin by approximately 1.8 percentage points in the quarter.

Operating expenses from continuing operations for the third quarter of fiscal 2026 decreased 6.0% to $11.4 million, or 25.9% of net sales, from $12.1 million, or 31.3% of net sales, in the same year-ago quarter, and decreased 14.0%, or $1.8 million, from $13.2 million the prior quarter ended March 31, 2026. The decrease from the prior quarter and year was due in part to a $1.7 million reduction in performance-based compensation accruals during the quarter, reflecting lower projected expense under the Company's incentive compensation programs.

Net income from continuing operations for the third quarter of fiscal 2026 totaled $3.0 million, or $0.22 per diluted share, compared to net income of $2.3 million, or $0.16 per diluted share, in the same year-ago quarter. The Company repurchased approximately 31,000 shares for $0.9 million during the 3-month period ended June 30, 2026. There is approximately $15.0 million remaining for future repurchases as of June 30, 2026.

Outlook

As a result of industry demand constraints discussed in our Shareholder Letter, we are reducing our outlook for fiscal 2026. We expect net sales from continuing operations to be in the range of $151 million to $155 million, and net income per share to a range of $0.14 to $0.21. For the fourth quarter of fiscal 2026, Clearfield expects net sales to be in the range of $38 million to $42 million and net income per share to be in the range of $0.00 to $0.07. The net income per share ranges are based on the number of shares outstanding at the end of the third quarter of fiscal 2026 and do not reflect the impact of any potential additional share repurchases completed in fiscal 2026. Our guidance also reflects our current expectations regarding the potential supply chain constraints of optical fiber mentioned in our first and second quarter letters to shareholders, as well as our current understanding of the impact of the evolving tariff situation, both which could contribute to uncertainty in our business and in the macroeconomic environment.

Conference Call

Management will hold a conference call today, August 5, 2026, at 5:00 p.m. Eastern Time (4:00 p.m. Central Time) to discuss these results and provide an update on business conditions.

Clearfield's President and Chief Executive Officer, Cheri Beranek, and Chief Financial Officer, Dan Herzog, will host the presentation, followed by a question-and-answer period.

U.S. dial-in: 1-844-826-3033

International dial-in: 1-412-317-5185

Conference ID: 10209753

The live webcast of the call can be accessed at the Clearfield Investor Relations website along with the company's earnings press release and presentation.

A replay of the call will be available after 8:00 p.m. Eastern Time on the same day through August 19, 2026, while an archived version of the webcast will be available on the Investor Relations website for 90 days.

U.S. replay dial-in: 1-844-512-2921

International replay dial-in: 1-412-317-6671

Replay ID: 10209753

About Clearfield, Inc.

Clearfield, Inc. (NASDAQ: CLFD) designs, manufactures, and distributes fiber optic management, protection, and delivery solutions that play a critical role in enabling broadband operators to close the digital divide. Our labor lite, craft-friendly platform is leveraged by community broadband, MSOs, incumbent service providers, ISPs, data centers, military, municipalities, and coops - from homes passed to homes connected faster and more efficiently. Headquartered in Minneapolis, MN, Clearfield deploys more than a million fiber ports each year. For more information, visit www.SeeClearfield.com.

CLEARFIELD, INC.
CONDENSED CONSOLIDATED BALANCE SHEETS
(IN THOUSANDS, EXCEPT SHARE AND PER SHARE DATA)
June 30, 2026 (Unaudited) | September 30, 2025
Assets
Current assets
Cash and cash equivalents | 20,449 | 21,493
Short-term investments | 80,774 | 84,484
Accounts receivables, net | 22,055 | 17,991
Inventories, net | 33,391 | 42,031
Prepaid and other current assets | 14,221 | 11,152
Current assets held for sale | - | 21,337
Total current assets | 170,890 | 198,488
Property, plant and equipment, net | 9,265 | 9,682
Long-term investments | 53,896 | 59,822
Goodwill | 4,709 | 4,709
Intangible assets, net | 7,942 | 9,353
Right-of-use lease assets | 9,968 | 8,420
Deferred tax asset | 9,970 | 10,263
Other non-current assets | 451 | 608
Non-current assets held for sale | - | 4,828
Total assets | 267,091 | 306,173
Liabilities and Shareholders' Equity
Current liabilities
Current portion of lease liability | 2,740 | 2,823
Accounts payable | 5,117 | 7,028
Accrued compensation | 4,571 | 6,598
Accrued expenses | 1,207 | 2,197
Current liabilities held for sale | - | 17,957
Total current liabilities | 13,635 | 36,603
Other liabilities
Long-term portion of lease liability | 7,536 | 5,934
Non-current liabilities held for sale | - | 7,473
Total liabilities | 21,171 | 50,010
Shareholders' equity
Preferred stock, $0.01 par value; 500,000 shares; no shares
issued or outstanding | - | -
Common stock, authorized 50,000,000, $0.01 par value;
13,597,691 and 13,839,675 shares issued and outstanding
as of June 30, 2026 and September 30, 2025, respectively | 136 | 138
Additional paid-in capital | 137,353 | 147,382
Accumulated other comprehensive (loss) income | (339 | 1,731
Retained earnings | 108,770 | 106,912
Total shareholders' equity | 245,920 | 256,163
Total Liabilities and Shareholders' Equity | 267,091 | 306,173

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2025-11-25_item7_mdna.md)

_Extraction: started at 'Results of Operations'._

Results of Operations

The Company's reportable segment is based on the Company's method of internal reporting. The internal reporting of the operating segment is defined based, in part, on the reporting and review process used by the Company's Chief Executive Officer, also known as the Chief Operating Decision Maker ("CODM"). The CODM reviews financial information presented on a consolidated basis for purposes of making operating decisions, allocating resources and evaluating financial performance. As such, the Company has determined that it operates as one reportable segment.

On November 11, 2025, the Company completed the sale of its Nestor Cables business, which was previously reported as the Nestor Cables Operating Segment. In connection with this sale, the historical results of the Nestor Cables business and certain assets and liabilities of the Nestor Cables business are reported in our consolidated financial statements as discontinued operations. Following the sale of the Nestor Cables business, the continuing operations of the Company comprise one operating segment and one reportable segment.

Reported below are the results of operations for the Company's continuing operations unless otherwise stated.

Year ended September 30, 2025, compared to year ended September 30, 2024

The Company's net sales for fiscal year 2025 increased 20%, or $24,566,000, to $150,134,000 from net sales of $125,568,000 in fiscal year 2024. The Company allocates sales from external customers to geographic areas based on the location to which the product is transported. Accordingly, international sales represented 3% and 2% of net sales for the years ended September 30, 2025, and 2024, respectively.

The increase in net sales for fiscal year 2025 of $24,566,000 compared to fiscal year 2024 is attributable to increased demand across the Company's core markets. Sales to the Community Broadband market increased 1%, or $767,000, from $66,005,000 in fiscal year 2024 to $66,772,000 in fiscal year 2025. Sales to Clearfield's MSO/Cable TV market increased 38%, or $8,864,000 from $23,487,000 in fiscal year 2024 to $32,351,000 in fiscal year 2025. Sales to the Large Regional market increased 58% to $33,706,000 from $21,293,000 in fiscal year 2024. Sales to National Carriers increased 11%, or $976,000, from $8,767,000 in fiscal year 2024 to $9,743,000 in fiscal year 2025.

Cost of sales for fiscal year 2025 was $99,597,000 compared to $99,721,000 in fiscal year 2024. Gross profit increased 96%, or $24,690,000, from $25,847,000 for fiscal year 2024 to $50,537,000 for fiscal year 2025. Gross profit percent was 33.7% in fiscal year 2025 compared to 20.6% for fiscal year 2024. The improvement in gross margin was due to increased volumes resulting in improved absorption of manufacturing overhead, as well as lower excess inventory charges of $10,074,000 in fiscal year 2025, reflecting improved inventory utilization and beneficial recoveries from inventory previously written down.

Selling, general and administrative expenses for fiscal year 2025 was $48,419,000, an increase of $3,338,000, or 7%, compared to $45,081,000 for fiscal year 2024. The increase was due to higher wages and performance-based compensation of $3,164,000.

Income from continuing operations for fiscal year 2025 was $2,118,000 compared to a loss from continuing operations of $19,234,000 for fiscal year 2024. The increase in income is attributable to increased sales and gross profit from higher customer demand and improved gross profit margin, partially offset by higher selling, general and administrative expenses as described above.

Net investment income in fiscal year 2025 was $6,549,000 compared to $7,472,000 for fiscal year 2024. The decrease in interest income is due to lower interest rates earned, partially offset by a higher average investments balance for the year ended September 30, 2025. The Company invests its excess cash primarily in Federal Deposit Insurance Company ("FDIC") backed bank certificates of deposit, United States ("U.S.") treasury securities, and money market funds and accounts. We expect interest income to decrease slightly in fiscal year 2026 due to lower expected market interest rates.

Income tax expense for fiscal year 2025 was $2,357,000 compared to income tax benefit of $3,248,000 for fiscal year 2024. The increase in tax expense of $5,605,000 from the year ended September 30, 2024, is due to the increase in pretax book income for fiscal year 2025. The income tax expense rate decreased to 27.2% for fiscal year 2025 from 27.6% for fiscal year 2024 due to changes in state tax, foreign tax and increased section 162(m) deduction. Our provision for income taxes includes current U.S. federal and state current and deferred tax expense.

Net income from continuing operations for fiscal year 2025 was $6,310,000 or $0.45 per basic and diluted share compared to net loss of $8,514,000 or $(0.58) per basic and diluted share for fiscal year 2024.

Net loss from discontinued operations for fiscal year 2025 was $3,947,000 or $(1.03) per basic and diluted share compared to net loss of $3,939,000 or $(0.27) per basic and diluted share for fiscal year 2024. Net loss from impairment of discontinued operations for fiscal year 2025 was $10,413,000. See Note 11 for further details regarding the impairment charges related to the Nestor Cables business.

Year ended September 30, 2024, compared to year ended September 30, 2023

The Company's net sales for fiscal year 2024 decreased 44%, or $100,154,000, to $125,568,000 from net sales of $225,722,000 in fiscal year 2023. The Company allocates sales from external customers to geographic areas based on the location to which the product is transported. Accordingly, international sales represented 2% and 3% of net sales for the years ended September 30, 2024, and 2023, respectively.

The decrease in net sales for fiscal year 2024 of $100,154,000 compared to fiscal year 2023 is attributable to decreased demand across the Company's core markets. Sales to the Community Broadband market decreased 41%, or $45,703,000, from $111,708,000 in fiscal year 2023 to $66,005,000 in fiscal year 2024. Sales to Clearfield's MSO/Cable TV market decreased 49%, or $22,182,000, from $45,669,000 in fiscal year 2023 to $23,487,000 in fiscal year 2024. Sales to the Large Regional market decreased 57% or $28,596,000, to $21,293,000 in fiscal 2024 from $49,889,000 in fiscal 2023. Sales to National Carriers decreased 2%, or $187,000, from $8,954,000 in fiscal year 2023 to $8,767,000 in fiscal year 2024. The decrease in sales to these customers was due to a lull in demand for fiber connectivity products as customers digest their larger than normal inventory levels built up during the pandemic which were purchased over the previous years.

Cost of sales for fiscal year 2024 was $99,721,000, a decrease of $46,144,000, or 32%, from $145,865,000 in fiscal year 2023. Gross profit decreased 68%, or $54,010,000, from $79,857,000 for fiscal year 2023 to $25,847,000 for fiscal year 2024. The decrease in gross profit was due to lower net sales and lower gross profit margin in fiscal year 2024. Gross profit percent was 20.6% in fiscal year 2024 compared to 35.4% for fiscal year 2023. Gross profit margin was negatively affected by unabsorbed overhead in our manufacturing facilities due to lower levels of demand. The Company's gross profit was also negatively impacted by an increase in inventory write-downs of $4,748,000 during the fiscal year ended September 30, 2024. Inventory write-downs are primarily due to excess inventory due to the lull in demand while customers draw down their existing products previously purchased during the period of long lead time supply chain created by the pandemic. The Company expects to operate at gross profit percentage levels at or below these levels for several quarters until revenue levels increase, which is expected to bring improved margins.

Selling, general and administrative expense for fiscal year 2024 was $45,081,000, an increase of $2,801,000, or 7%, compared to $42,280,000 for fiscal year 2023. The increase was due to increased performance-based compensation of $1,395,000, increased stock-based compensation of $819,000, and increased professional fees of $1,086,000.

Loss from continuing operations for fiscal year 2024 was $19,234,000 compared to income from continuing operations of $37,577,000 for fiscal year 2023. The decrease is attributable to lower sales and gross profit due to excess supply of fiber products and also higher unabsorbed overhead related to expanded manufacturing capacities.

Net investment income in fiscal year 2024 was $7,472,000 compared to $5,199,000 for fiscal year 2023. The increase in interest income is due to a higher average investments balance and higher interest rates earned for the year ended September 30, 2024. The higher overall investments balance is a result of the Company's capital raise of approximately $130,000,000 completed late in the first fiscal quarter of 2023 and cash generated from operations in fiscal 2024. The Company invests its excess cash primarily in Federal Deposit Insurance Company ("FDIC") backed bank certificates of deposit, United States ("U.S.") treasury securities, and money market funds and accounts.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2025-11-25_item1_business.md)

ITEM 1. BUSINESS

Company Overview

We design, manufacture, and distribute fiber protection, fiber management, and fiber delivery solutions to enable rapid and cost-effective fiber-fed deployment throughout the broadband service provider space primarily across North America. Our "fiber to anywhere" platform serves the unique requirements of Community Broadband customers (Tier 2 and 3 telco carriers, utilities, municipalities, and alternative carriers), Multiple System Operators (cable television), Large Regional Service Providers (ILEC operating a multi-state network with more than 500,000 subscribers), National Carriers (wireline/wireless national telco carriers (Tier 1)), and International customers (primarily Europe, Canada, Mexico, and Caribbean Markets).

Our mission is to enable the lifestyle that better broadband provides through innovative product design that accelerates fiber-based deployment, making communications simpler and more affordable for people everywhere. We believe our products offer broadband service providers a competitive advantage at a crucial time when demand for fiber-based services is increasing to historic levels as providers focus on passing and connecting more homes. We are driven to help broadband service providers reduce the cost - and increase the speed of fiber deployment.

Segment Information

We are engaged in global operations. Our operations currently comprise one reportable segment.

On November 11, 2025, the Company completed the sale of its Nestor Cables business, which was previously reported as the Nestor Cables Operating Segment. In connection with this sale, the historical results of the Nestor Cables business and certain assets and liabilities of the Nestor Cables business are reported in our consolidated financial statements as discontinued operations. Following the sale of the Nestor Cables business, the continuing operations of the Company comprise one operating segment and one reportable segment.

Clearfield is focused on providing fiber management, fiber protection, and fiber delivery products that accelerate the turn-up of fiber-based networks in residential homes, businesses, and network infrastructure in the wireline and wireless access network. We offer a broad portfolio of fiber products that allow service providers to build fiber networks faster, meet service delivery demands, and align build costs with take rates.

Clearfield's products allow its customers to connect twice as many homes in their Fiber to the Home ("FTTH") builds by using fewer resources in less time. Our products speed up the time to revenue for our service provider customers in Multiple Dwelling Units ("MDUs") and Multiple Tenant Units ("MTUs") by reducing the amount of labor and materials needed to provide gigabit service. Our products help make business services more profitable through faster building access, easier reconfiguration, and quicker services turn-up. Finally, Clearfield is removing barriers to wireless 4G/5G deployments in backhaul from the tower to the cloud and fiber fronthaul from the tower to the antenna at the cell site through better fiber management, test access, and fiber protection.

Substantially all of the final build and assembly is completed at Clearfield's plants in Brooklyn Park, Minnesota and Tijuana, Mexico, with manufacturing support from a network of domestic and global manufacturing partners. Clearfield specializes in producing these products on both a quick-turn and scheduled delivery basis.

Products

Our product strategy involves analyzing the broadband communications industry environment and technology, with a particular focus on simplifying our customers' business, and developing innovative, high-quality products utilizing modular designs wherever possible. We are committed to make fiber deployment success easier by providing craft-friendly, pre-connectorized plug-and-play fiber assemblies, fiber management and pathway products to speed deployments and provide the lowest total cost of ownership for our customer's networks. With the innovation of forward-thinking products, a 100 percent plug-and-play platform and creative deployment methods, we are fulfilling our mission of enabling the lifestyle of better broadband and beyond.

Throughout the fiber deployment journey from the Inside Plant (ISP) to the Outside Plant (OSP), into the Access Network and all the way to the fiber connection at the home, our labor lite solutions solve service provider fiber network design and installation challenges. Our methodologies provide easy to engineer and easy to install solutions that take the mystery out of deploying fiber networks.

Leveraging factory terminated single-fiber and multi-fiber plug-and-play connectors, homes passed, and homes connected metrics can be greatly increased. The speed to turn up the entire network is maximized, while helping ensure superior optical performance achieved by using low-loss connectors, terminated in the factory.

Whether inside a cabinet or at the home, innovative slack storage spools and deploy reels reduce the dependence on making exact cable measurements. This enables the deployment of double-ended, standard cable lengths rather than relying on highly engineered, built-to-order cable assemblies or multiple field splicing events.

Product development for the Company's product line program has mainly been conducted internally. We believe that the communication industry environment is constantly evolving, and our success depends on our ability to anticipate and respond to these changes. Research and development are reflected in Selling, General, & Administrative expenses.

Some of our products currently offered are described below.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2025-11-25_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2025-11-25_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2025-11-25_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-05_2-02-results.md, 10-K_2025-11-25_item7_mdna.md, 10-K_2025-11-25_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
