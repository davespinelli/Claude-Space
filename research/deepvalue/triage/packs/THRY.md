# Triage pack — THRY · Thryv Holdings, Inc.

_Generated 2026-09-04 18:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** THRY · **Name:** Thryv Holdings, Inc.
- **CIK:** 0001556739
- **SIC:** 7310 — Services-Advertising
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/THRY

**Fetcher warnings for this ticker:** 10-K 2026-02-26: heading split missed Item 7 - MD&A; 10-Q 2026-08-04: MD&A heading not detected, wrote truncated full text

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Thryv Holdings, Inc.
- **CIK:** 1,556,739 · **SIC:** 7310 (Services-Advertising) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 1.92 |
| mktcap | $85.3M |
| ev | $284.9M |
| ev_ebit | 5.0x |
| fcf | $31.1M |
| fcf_yield | 36.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 10.9% |
| net_debt | $199.6M |
| net_debt_ebit | 3.5x |
| cash | $9.1M |
| ltd | $208.7M |
| equity | $211.6M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $785.0M |
| revenue_prior | $824.2M |
| rev_growth | -4.7% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $56.7M |
| net_income | $307k |
| cfo | $63.5M |
| capex | $32.4M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 1.1% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 44,439,111 |
| shares_py | 43,936,290 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -80.3% |
| r6m | -42.2% |
| off_52w_high | -85.2% |
| adv20 | $1.8M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.96 |
| r_ev_ebit | 0.93 |
| r_roic | 0.73 |
| r_rev_growth | 0.20 |
| r_buyback | 0.43 |
| score | 0.55 |

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
| rank | 197 |

**Screen rationale:** top-quartile FCF yield 36.5%; cheap at 5.0x EV/EBIT; WARNING 6m return below -40%


## 3. Share count trend

- Shares outstanding: **44,439,111** (CY2026Q2I) vs **43,936,290** prior year (CY2025Q2I)
- Change: **1.1%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-11** — Item 5.02 (officer / director change or comp arrangement): Departure of Directors or Certain Officers; Election of Directors; Appointment of Certain Officers; Compensatory Arrangements of Certain Officers.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 399,548 sh / $1,122,376 vs sells 0 sh / $0 -> net $1,122,376 (BUYING).
Distinct insiders buying (code P): 1. Largest buy: PAULSON & CO. INC. bought 254,573 sh @ $2.82 ($717,896) on 2026-08-04.

Form 4 filings parsed: 12; transaction rows: 18 (open-market buys 2, sales 0).

| code | rows |
|---|---|
| A | 6 |
| F | 8 |
| M | 2 |
| P | 2 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-04_2-02-results.md)

_Extraction: started at the first release heading, 'Thryv Reports Second Quarter 2026 Results and Launches Thryv Growth Pl'; skipped 17 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (exhibit991-pressreleaseq22.htm)

Thryv Reports Second Quarter 2026 Results and Launches Thryv Growth Platform

– Q2 SaaS Revenue Grows to 76% of Total Revenue

– Q2 SaaS Monthly ARPU Increases 12% Year-Over-Year to $394

– Company Announces Strategic Restructuring Plan to Improve Operating Efficiencies

DALLAS, August 4, 2026 – Thryv Holdings, Inc. (NASDAQ:THRY) ("Thryv" or the "Company"), the provider of Thryv®, an AI-native growth platform for local service businesses, reported results for the second quarter of 2026.

"Our second quarter marked another step forward in the transformation of our business, with SaaS now representing 76% of our revenue and ARPU growing 12% year-over-year," said Joe Walsh, Thryv Chairman and CEO. "Our SaaS profile now reflects our deliberate focus on the newly launched Thryv Growth Platform, the first platform purpose-built for the small business owner with AI running underneath to turn every lead into measurable revenue. We are also announcing a restructuring plan that realigns our cost structure to focus on a SaaS operating model and extend the agentic AI capabilities embedded in Thryv's customer-facing platform. Looking ahead, we remain focused on reaccelerating the growth of our SaaS business. We are announcing today that we have partnered Ooma and plan to establish a strategic partnership with Wix, with a shared focus on helping small businesses succeed."

The Company expects to incur total restructuring and related charges of approximately $20 million to $25 million, approximately 10% of which has already been incurred, with approximately 40% expected to be recognized in the second half of 2026 and the remaining 50% to be recognized in 2027. Cost savings are anticipated to begin in 2027, building to approximately $55 million to $60 million in gross annualized cost savings upon completion.

"We remain focused on optimizing the Thryv Growth Platform, a unified, AI-native growth offering, concentrating investments to scale the business and expand profitability. These initiatives are expected to be accretive to Adjusted EBITDA margins in the future, while strengthening the Company's free cash flow generation," stated Paul Rouse, Chief Financial Officer.

Second Quarter Financial 2026 Highlights:

• SaaS revenue was $114.5 million, a decrease of 0.5% year-over-year, of which Market, Sell, Grow initiatives grew 21% 1 year-over-year, offset by headwinds in legacy CRM products

• Marketing Services revenue was $36.2 million

• Consolidated total revenue was $150.7 million

• Consolidated net loss was $16.7 million, or $(0.38) per diluted share; compared to net income of $13.9 million, or $0.31 per diluted share, for the second quarter of 2025

• Consolidated Adjusted EBITDA was $20.8 million, representing an Adjusted EBITDA margin of 13.8%

1 Excludes Keap. Market, Sell, Grow initiatives include Marketing Center and additional marketing value-added services.

• SaaS Adjusted EBITDA was $13.6 million, representing an Adjusted EBITDA margin of 11.8%

• Marketing Services Adjusted EBITDA was $7.3 million, representing an Adjusted EBITDA margin of 20.0%

• Consolidated Gross Profit was $94.6 million

• Consolidated Adjusted Gross Profit 2 was $99.2 million

• SaaS Gross Profit was $72.7 million, representing a Gross Margin of 63.5%

• SaaS Adjusted Gross Profit 1 was $76.2 million , representing an Adjusted Gross Margin of 66.6%

Recent Business Highlights and Metrics

• Quality customers 3 (defined as those contributing more than $400 in monthly recurring revenue) accounted for 72% of SaaS revenue 3 in the second quarter of 2026

• SaaS clients were 95 thousand at the end of the second quarter of 2026

• Seasoned Net Revenue Retention 4 was 90% for the second quarter of 2026

• SaaS monthly Average Revenue per Unit ("ARPU") 5 was $394 for the second quarter of 2026, an increase of 11.9% year-over-year

Outlook

Based on information available as of August 4, 2026, Thryv is issuing guidance 6 for the third quarter of 2026 and updating full year 2026 as indicated below:

3rd Quarter | 4th Quarter | Full Year
(in millions) | 2026 | 2026 | 2026
SaaS Revenue | $111.0 - $112.0 | $111.0 - $114.0 | $453.0 - $457.0
SaaS Adjusted EBITDA 7 | $8.5 - $9.5 | $9.0 - $10.0 | $42.0 - $44.0

3rd Quarter | 4th Quarter | Full Year
(in millions) | 2026 | 2026 | 2026
Marketing Services Revenue | $34.0 - $35.0 | $40.0 - $41.0 | $161.0 - $163.0
Marketing Services Adjusted EBITDA 7 | $5.0 - $6.0 | $5.5 - $6.5 | $31.0 - $33.0

2 Defined as Gross profit adjusted to exclude the impact of depreciation and amortization expense and stock-based compensation expense.

3 Excludes customers and revenue attributed to the Keap acquisition.

4 Seasoned NRR is calculated by dividing the revenue of all clients that have had one or more SaaS offerings for at least two years as of the last month of the year or quarter, as applicable, by the same clients' revenue one year ago. For each reporting quarter, the weighted-average monthly NRR from all the months in the quarter are reported. Seasoned NRR excludes clients acquired in the Keap acquisition.

5 Defined as total client billings for a particular month divided by the number of clients that have one or more revenue-generating solutions in that same month. This is a weighted-average calculation and inclusive of the impact from the Keap acquisition.

Three Months Ended | Six Months Ended
June 30, | June 30,
(in thousands, except share and per share data) | 2026 | 2025 | 2026 | 2025
Revenue | 150,728 | 210,470 | 318,412 | 391,841
Cost of services | 56,168 | 63,850 | 114,596 | 125,933
Gross profit | 94,560 | 146,620 | 203,816 | 265,908
Operating expenses:
Sales and marketing | 47,038 | 56,063 | 94,986 | 115,905
Research and development | 7,509 | 8,661 | 18,940 | 18,870
General and administrative | 41,156 | 52,356 | 86,975 | 104,627
Total operating expenses | 95,703 | 117,080 | 200,901 | 239,402
Operating (loss) income | (1,143) | 29,540 | 2,915 | 26,506
Other income (expense):
Interest expense | (5,035) | (5,981) | (9,176) | (12,048)
Interest expense, related party | (2,483) | (2,971) | (4,949) | (5,977)
Net periodic pension cost | (357) | (778) | (702) | (1,546)
Other income | (446) | 2,557 | 987 | 2,949
(Loss) income before income tax expense | (9,464) | 22,367 | (10,925) | 9,884
Income tax expense | (7,196) | (8,436) | (1,193) | (5,571)
Net (loss) income | (16,660) | 13,931 | (12,118) | 4,313
Other comprehensive loss:
Foreign currency translation adjustment, net of tax | (114) | (72) | (509) | (259)
Comprehensive (loss) income | (16,774) | 13,859 | (12,627) | 4,054
Net (loss) income per common share:
Basic | (0.38) | 0.32 | (0.27) | 0.10
Diluted | (0.38) | 0.31 | (0.27) | 0.10
Weighted-average shares used in computing basic and diluted net (loss) income per common share:
Basic | 44,358,330 | 43,744,144 | 44,283,478 | 43,579,171
Diluted | 44,358,330 | 44,303,331 | 44,283,478 | 44,586,162

Thryv Holdings, Inc. and Subsidiaries

Consolidated Balance Sheets

(in thousands, except share data) | June 30, 2026 | December 31, 2025
Assets
Current assets
Cash and cash equivalents | 9,136 | 10,752
Accounts receivable, net of allowance of $13,144 in 2026 and $13,830 in 2025 | 127,756 | 136,394
Contract assets, net of allowance of $2 in 2026 and $2 in 2025 | 622 | 411
Taxes receivable | 1,172 | 8,134
Deferred costs | 8,243 | 11,548
Prepaid expenses and other current assets | 11,041 | 11,618
Total current assets | 157,970 | 178,857
Fixed assets and capitalized software, net | 49,242 | 50,885
Goodwill | 253,809 | 253,809
Intangible assets, net | 22,979 | 25,929
Deferred tax assets | 137,604 | 133,221
Other assets | 32,528 | 45,886
Total assets | 654,132 | 688,587
Liabilities and Stockholders' Equity
Current liabilities
Accounts payable | 5,509 | 9,764
Accrued liabilities | 88,753 | 91,246
Current portion of unrecognized tax benefits | 1,847 | 28,303
Contract liabilities | 24,820 | 28,875
Current portion of Term Loan | 21,000 | 10,500
Current portion of Term Loan, related party | 14,000 | 7,000
Other current liabilities | 2,518 | 3,905
Total current liabilities | 158,447 | 179,593
Term Loan, net | 115,886 | 125,419
Term Loan, net, related party | 78,788 | 85,448
ABL Facility | 14,057 | 25,120
Pension obligations, net | 41,425 | 44,171
Other liabilities | 33,967 | 10,697
Total long-term liabilities | 284,123 | 290,855
Commitments and contingencies
Stockholders' equity
Common stock - $0.01 par value, 250,000,000 shares authorized; 72,970,119 shares issued and 44,417,798 shares outstanding at June 30, 2026; and 72,002,129 shares issued and 43,815,268 shares outstanding at December 31, 2025 | 730 | 720
Additional paid-in capital | 1,310,845 | 1,303,144
Treasury stock - 28,552,321 shares at June 30, 2026 and 28,186,861 shares at December 31, 2025 | (499,764) | (498,103)
Accumulated other comprehensive loss | (16,020) | (15,511)
Accumulated deficit | (584,229) | (572,111)
Total stockholders' equity | 211,562 | 218,139
Total liabilities and stockholders' equity | 654,132 | 688,587

Thryv Holdings, Inc. and Subsidiaries

Consolidated Statements of Cash Flows

Six Months Ended June 30,
(in thousands) | 2026 | 2025
Cash Flows from Operating Activities
Net (loss) income | (12,118) | 4,313
Adjustments to reconcile net (loss) income to net cash provided by operating activities:
Depreciation and amortization | 20,060 | 21,707
Amortization of deferred commissions | 3,046 | 6,944
Amortization of debt issuance costs | 1,465 | 1,648
Deferred income taxes | (4,116) | 2,310
Provision for credit losses and service credits | 6,734 | 9,020
Stock-based compensation expense | 7,537 | 13,745
Net periodic pension cost | 702 | 1,546
Gain on foreign currency exchange rates | (962) | (2,787)
Other | 2 | 38
Changes in working capital items, excluding acquisitions:
Accounts receivable | 24,677 | 15,392
Prepaid expenses and other assets | (389) | (16,493)
Accounts payable and accrued liabilities | (33,831) | (20,515)
Contract liabilities | (4,443) | (13,748)
Other liabilities | 18,990 | (4,045)
Net cash provided by operating activities | 27,354 | 19,075
Cash Flows from Investing Activities
Additions to fixed assets and capitalized software | (16,121) | (14,855)
Other | — | (143)
Net cash used in investing activities | (16,121) | (14,998)
Cash Flows from Financing Activities
Payments of Term Loan | — | (15,750)
Payments of Term Loan, related party | — | (10,500)
Proceeds from ABL Facility | 154,389 | 206,317
Payments of ABL Facility | (165,451) | (190,292)
Principal payments on finance lease obligations | (436) | —
Other | (1,486) | 165
Net cash used in financing activities | (12,984) | (10,060)
Effect of exchange rate changes on cash, cash equivalents and restricted cash | 61 | 592
Decrease in cash, cash equivalents and restricted cash | (1,690) | (5,391)
Cash, cash equivalents and restricted cash, beginning of period | 10,869 | 17,760
Cash, cash equivalents and restricted cash, end of period | 9,179 | 12,369
Supplemental Information
Cash paid for interest | 13,438 | 16,480
Cash (received) paid for income taxes, net | (3,969) | 3,373

Segment Information

The following tables summarize the operating results of the Company's reportable segments :

Three Months Ended June 30, | Change
(dollars in thousands) | 2026 | 2025 | Amount | %
Revenue
SaaS | 114,480 | 115,005 | (525) | (0.5) | %
Marketing Services | 36,248 | 95,465 | (59,217) | (62.0) | %
Total Revenue | 150,728 | 210,470 | (59,742) | (28.4) | %
Adjusted EBITDA
SaaS | 13,562 | 23,393 | (9,831) | (42.0) | %
Marketing Services | 7,263 | 27,839 | (20,576) | (73.9) | %
Consolidated Adjusted EBITDA 8 | 20,825 | 51,232 | (30,407) | (59.4) | %

_[...truncated at ~12,000 chars of this document]_

## 8. MD&A — no 10-K Item 7 fetched, using 10-Q MD&A (10-Q_2026-08-04_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We are a software-led platform company focused on enabling small and medium-sized businesses (" SMBs ") to run and grow their businesses more efficiently. Our strategy is centered on delivering a unified, extensible SaaS platform that supports customer acquisition, engagement, operations, and retention across the SMB lifecycle.

Our expertise in delivering solutions for our client base is rooted in our deep history of serving SMBs. In 2026, SMB demand for integrated technology solutions continues to grow as SMBs adapt their business and service models to facilitate remote working and virtual interactions.

We serve approximately 215,000 SMB clients globally through two business segments: SaaS and Marketing Services.

SaaS

Our SaaS segment generated $114.5 million and $115.0 million of consolidated revenue for the three months ended June 30, 2026 and 2025, respectively, and $231.2 million and $226.1 million of consolidated revenue for the six months ended June 30, 2026 and 2025, respectively.

Core Platform Offerings. The core offerings of our Thryv Platform include Thryv Marketing Center and Keap®. Thryv Marketing Center contains everything an SMB owner needs to effectively market and grow their business, including easy to understand, artificial intelligence (" AI ") driven analytics and lead attribution that help them understand which marketing efforts are delivering results. Keap® is our customer relationship management (" CRM ") and automation engine that helps SMBs efficiently grow by automating repetitive tasks, campaigns, and processes, using automation tools and AI.

Extensions. The Thryv Platform supports extensions and integrations that allow customers to tailor the platform to their specific business needs. Our extension offerings include Thryv Leads®, growth packages, SEO tools, and website creation and management tools. These optional platform add-ons provide a seamless user experience for our end-users and drive higher engagement within the Thryv Platform while also producing incremental revenue growth.

Payment Solutions. ThryvPay® and KeapPay are our own branded payment solutions that allow users to get paid via credit card and ACH and are tailored to service-based businesses that want to provide consumers with safe, contactless, and fast online payment options.

Supporting Software Solutions. We offer supporting software solutions, including Thryv Business Center, that seamlessly integrate with our core platform offerings, providing customers with enhanced functionality and additional features.

Professional Services. We offer implementation, training, and consulting services to help customers maximize value from our platform, including onboarding and implementation, a year-one Customer Success Manager, and Thryv Success Services, which includes listing refresh services, strategic content creation, and ongoing strategic consulting.

Marketing Services

Our Marketing Services segment provides both print and digital solutions and generated $36.2 million and $95.5 million of consolidated revenue for the three months ended June 30, 2026 and 2025, respectively, and $87.2 million and $165.7 million of consolidated revenue for the six months ended June 30, 2026 and 2025, respectively.

Our Marketing Services offerings include our owned and operated Print Yellow Pages, which carry the " The Real Yellow Pages " tagline, our proprietary Internet Yellow Pages, known by the Yellowpages.com, Superpages.com, and Dexknows.com URLs. Our Search Engine Marketing solutions deliver business leads through increased traffic to clients' websites from major engines and directories by increasing visibility and search engine results pages through paid advertising. Additionally, we offer other digital media solutions including online display and social advertising and search engine optimization tools.

During the year ended December 31, 2024, we made a strategic decision to terminate our Marketing Services solutions by the end of 2028.

Transition of Digital Marketing Services Clients to the Thryv Platform

During the fourth quarter of 2023, we made a strategic decision to accelerate the transition of clients with Digital marketing services solutions to our Thryv Platform by converting certain Marketing Services products for customers to the Thryv Platform by initiating upgrades for clients outside of the sales process at no additional base cost to these clients at the time of upgrade. The cost of bringing these clients into SaaS products is generally lower than the cost of acquiring a new SaaS customer or selling a SaaS product to an existing Marketing Services customer because the Company does not pay commissions to sales personnel for upgrades that Thryv initiates for customers outside of the sales process.

During the twelve months ended June 30, 2026, we converted approximately 11,000 clients with Digital marketing services products to our Thryv Platform who were not already SaaS clients at the time of conversion. As of June 30, 2026, approximately 9,000 of these clients remained as SaaS clients. The conversion of these Marketing Services clients increased SaaS revenue by $5.0 million and $7.6 million during the three and six months ended June 30, 2026, respectively.

Additionally, during the twelve months ended June 30, 2026, we converted Digital marketing services products to our Thryv Platform for approximately 4,000 clients who already had at least one SaaS product in our Thryv Platform at the time of conversion. The conversion of these Marketing Services clients increased SaaS revenue by $1.8 million and $3.2 million during the three and six months ended June 30, 2026, respectively.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Consolidated Results of Operations

The following table presents certain consolidated financial data for each of the periods indicated:

Three Months Ended June 30,
2026 | 2025
(unaudited)
(dollars in thousands) | Amount | % of Revenue | Amount | % of Revenue
Revenue | 150,728 | 100 | % | 210,470 | 100 | %
Cost of services | 56,168 | 37.3 | % | 63,850 | 30.3 | %
Gross profit | 94,560 | 62.7 | % | 146,620 | 69.7 | %
Operating expenses:
Sales and marketing | 47,038 | 31.2 | % | 56,063 | 26.6 | %
Research and development | 7,509 | 5.0 | % | 8,661 | 4.1 | %
General and administrative | 41,156 | 27.3 | % | 52,356 | 24.9 | %
Total operating expenses | 95,703 | 63.5 | % | 117,080 | 55.6 | %
Operating (loss) income | (1,143) | 0.8 | % | 29,540 | 14.0 | %
Other income (expense):
Interest expense | (7,518) | 5.0 | % | (8,952) | 4.3 | %
Net periodic pension cost | (357) | 0.2 | % | (778) | 0.4 | %
Other (expense) income | (446) | 0.3 | % | 2,557 | 1.2 | %
(Loss) income before income tax expense | (9,464) | 6.3 | % | 22,367 | 10.6 | %
Income tax expense | (7,196) | 4.8 | % | (8,436) | 4.0 | %
Net (loss) income | (16,660) | 11.1 | % | 13,931 | 6.6 | %
Other financial data:
Adjusted EBITDA (1) | 20,825 | 13.8 | % | 51,232 | 24.3 | %
Adjusted Gross Profit (2) | 99,177 | 150,658
Adjusted Gross Margin (3) | 65.8 | % | 71.6 | %

(1) See " Non-GAAP Financial Measures " for a definition of Adjusted EBITDA and a reconciliation to Net (loss) income, the most directly comparable measure presented in accordance with GAAP.

(2) See " Non-GAAP Financial Measures " for a definition of Adjusted Gross Profit and a reconciliation to Gross profit, the most directly comparable measure presented in accordance with GAAP.

(3) See " Non-GAAP Financial Measures " for a definition of Adjusted Gross Margin.

Comparison of the Three Months Ended June 30, 2026 to the Three Months Ended June 30, 2025

Revenue

The following table summarizes Revenue by business segment for the periods indicated:

Three Months Ended June 30, | Change
2026 | 2025 | Amount | %
(dollars in thousands) | (unaudited)
SaaS | 114,480 | 115,005 | (525) | (0.5) | %
Marketing Services | 36,248 | 95,465 | (59,217) | (62.0) | %
Revenue | 150,728 | 210,470 | (59,742) | (28.4) | %

Revenue decreased by $59.7 million, or 28.4%, for the three months ended June 30, 2026 compared to the three months ended June 30, 2025. The decrease was driven by a decrease in Marketing Services revenue of $59.2 million and a decrease in SaaS revenue of $0.5 million.

SaaS Revenue

SaaS revenue decreased by $0.5 million, or 0.5%, for the three months ended June 30, 2026 compared to the three months ended June 30, 2025. The decrease was primarily attributable to clients downgrading or cancelling their SaaS solutions, partially offset by new sales, client expansion, and the Company's conversion of Digital marketing services solutions for clients to its SaaS offerings. SaaS revenue decreased $12.9 million due to net revenue changes associated with products sold or converted prior to January 1, 2026. The Company's conversion of Digital marketing services solutions for clients to SaaS offerings during the first six months of 2026 increased SaaS revenue by $4.0 million, and new sales and client expansion during the first six months of 2026 increased SaaS revenue by $8.4 million.

Marketing Services Revenue

Marketing Services revenue decreased by $59.2 million, or 62.0%, for the three months ended June 30, 2026 compared to the three months ended June 30, 2025.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-26_item1_business.md)

Item 1. Business

Overview

Thryv is a software-led platform company focused on enabling small and medium-sized businesses (" SMBs ") to run and grow their businesses more efficiently with artificial intelligence (" AI ") tools and automations. Our strategy is centered on delivering a unified, extensible SaaS platform that supports customer acquisition, engagement, operations, and retention across the SMB lifecycle.

As of December 31, 2025 , we serve approximately 230,000 SMB clients through our two business segments: SaaS and Marketing Services. SaaS represents the strategic growth engine of the Company. Marketing Services is our legacy segment that we are actively managing and exiting as part of a multi-year transition to a pure SaaS business model.

Our SaaS platform (or " Thryv Platform ") is designed for active daily use by business owners and operators. Customers engage directly with the platform to help business owners build a strong online presence, manage leads, automate workflows, communicate with customers, create websites, manage social media content, process payments, and make data-informed decisions that drive business outcomes.

We report our results based on two reportable segments (see Note 17, Segment Information) :

• SaaS , which includes our unified SMB marketing platform, supporting software solutions, related extensions, payment solutions, and professional services; and

• Marketing Services , which includes our legacy print and digital solutions business, which we plan to exit by the end of 2028.

SaaS

Thryv's SaaS segment consists of a unified marketing platform that combines customer relationship management (" CRM "), marketing execution, automation, communications, payments, and reporting into a single system. The platform is modular by design, allowing customers to adopt core capabilities and extend functionality as their needs evolve.

The platform incorporates Keap's CRM and automation engine with Thryv's marketing, communication, payment, and reporting capabilities. Rather than operating as standalone products, these capabilities are connected and function as integrated components of a single platform.

Revenue in the SaaS segment is generated through subscription plans, platform extensions, payment solutions, and professional services (collectively referred to as our " SaaS solutions "). Customers may expand their usage of the SaaS solutions over time through purchasing additional features and expanding capacity.

Our subscription offerings are sold on a recurring basis and are designed to scale with the growth and complexity of our customers' businesses. Additionally, the Company has expanded its approach for certain SaaS offerings by introducing a performance-based model, in which clients' fees are based on the volume of inquiries generated by the Company's services.

Core Platform Capabilities

The Thryv Platform delivers a set of core capabilities that support the full SMB customer lifecycle, including:

• Marketing execution, including social media management, across digital channels;

• Customer data and relationship management;

• Workflow automation and customer communications;

• Payments, invoicing, and revenue tracking; and

• Embedded reporting and performance insights.

These capabilities are delivered through a unified interface and are designed to work together, enabling SMBs to seamlessly transition from customer acquisition to engagement, conversion, and retention.

Our core platform offerings include Thryv Marketing Center and Keap®.

Thryv Marketing Center includes everything an SMB owner needs to effectively market and grow their business, including easy to understand, AI-driven analytics and lead attribution that help them understand which marketing efforts are delivering results. Thryv Marketing Center offers the following:

• AutoID . Marketing Center connects prospects' and customers' digital interactions with the business and synchronizes these activities with the Thryv CRM records. This enables device-level attribution, giving Thryv's users clear insight into when and where a client found them for proper attribution of what works and what doesn't.

• Enhanced Online Presence . Marketing Center includes paid profiles on YP.com, Yelp.com, and other partner sites, as well as a robust Google Business Profile Optimization service. This ensures that the SMB's most viewed online profiles stand out from the competition, get noticed, and drive results.

• Marketing Tools . Marketing Center includes additional marketing tools to help users optimize their online marketing efforts. These include a robust heat mapping tool to optimize and improve their website and landing pages based on visitor behavior and off-line call tracking to track the efficacy of offline media efforts such as lawn signs or post cards. Marketing Center also includes a robust competitor watch to track the digital advertising activities of competitors, providing valuable insights and helping users gain a competitive advantage when run in conjunction with paid campaigns. Additionally, Marketing Center's social media management tools generate content tailored for each social media platform and allow an SMB to share content instantly across their channels. SMBs can also plan and schedule social media posts in advance using Marketing Center's scheduling software.

Keap® is our CRM and automation engine that helps SMBs efficiently grow by automating repetitive tasks, campaigns, and processes, using automation tools and AI. Keap offers the following:

• CRM. Manage contacts, notes, tags, and custom fields—all in one place.

• Sales and Marketing Automations. Streamline repetitive tasks such as lead follow-up, re-engagement campaigns, and gathering customer reviews using Keap's Automation Builder.

• Sales Pipelines. Organize and manage leads with a drag-and-drop interface that triggers emails, quotes, and invoices as leads progress through the pipeline.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-26_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | **MISSING** |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-26_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-04_2-02-results.md, 10-Q_2026-08-04_mdna.md (10-Q MD&A used in place of the 10-K), 10-K_2026-02-26_item1_business.md

**Missing:** 10-K Item 7 MD&A (substituted 10-Q MD&A), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
