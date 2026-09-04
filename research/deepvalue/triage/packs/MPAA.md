# Triage pack — MPAA · MOTORCAR PARTS OF AMERICA INC

_Generated 2026-09-04 12:44 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** MPAA · **Name:** MOTORCAR PARTS OF AMERICA INC
- **CIK:** 0000918251
- **SIC:** 3714 — Motor Vehicle Parts & Accessories
- **Fiscal year end (MM-DD):** 03-31
- **Exchange:** Nasdaq
- **Filings fetched:** /Users/davidspinelli/Documents/Claude Space/research/deepvalue/filings/MPAA

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** MOTORCAR PARTS OF AMERICA INC
- **CIK:** 918,251 · **SIC:** 3714 (Motor Vehicle Parts & Accessories) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 11.79 |
| mktcap | $223.1M |
| ev | $204.0M |
| ev_ebit | 3.1x |
| fcf | $15.5M |
| fcf_yield | 6.9% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 22.2% |
| net_debt | -$19.1M |
| net_debt_ebit | -0.3x |
| cash | $19.1M |
| ltd | $0.00 |
| equity | $253.0M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $789.8M |
| revenue_prior | $757.4M |
| rev_growth | 4.3% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $65.8M |
| net_income | $12.0M |
| cfo | $19.2M |
| capex | $3.7M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -2.6% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 18,924,818 |
| shares_py | 19,435,706 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -3.9% |
| r6m | 13.9% |
| off_52w_high | -33.5% |
| adv20 | $1.6M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.58 |
| r_ev_ebit | 0.97 |
| r_roic | 0.89 |
| r_rev_growth | 0.50 |
| r_buyback | 0.81 |
| score | 0.75 |

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
| rank | 31 |

**Screen rationale:** cheap at 3.1x EV/EBIT; high ROIC 22.2%; buying back stock -2.6%; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **18,924,818** (CY2026Q2I) vs **19,435,706** prior year (CY2025Q2I)
- Change: **-2.6%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

- Last 11.79 (as of 2026-09-03) · 52w range 9.52 - 17.73 · -33.5% vs 52w high · 23.8% above 52w low

_Source: yfinance, live._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-02** — Item 1.01 (Entry into a Material Definitive Agreement): On June 26, 2026, Motorcar Parts of America, Inc. (the "Company") and Selwyn Joffe, the Chairman, President and Chief Executive Officer of the Company, entered into

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 1,000 sh / $9,670 vs sells 14,074 sh / $211,473 -> net $-201,803 (SELLING).
Distinct insiders buying (code P): 1. Largest buy: Bryan David bought 1,000 sh @ $9.67 ($9,670) on 2026-02-12.

Form 4 filings parsed: 34; transaction rows: 122 (open-market buys 1, sales 1).

| code | rows |
|---|---|
| A | 26 |
| F | 22 |
| M | 72 |
| P | 1 |
| S | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-10_2-02-results.md)

_Extraction: started at the first release heading, 'MOTORCAR PARTS OF AMERICA REPORTS FISCAL 2027 FIRST QUARTER RESULTS'; skipped 8 forward-looking-statement block(s); 8 block(s) of pre-heading matter dropped._

## EX-99.1 - EXHIBIT 99.1 (ef20079233_ex99-1.htm)

MOTORCAR PARTS OF AMERICA REPORTS FISCAL 2027 FIRST QUARTER RESULTS

Company Reaffirms Full-Year Guidance;

Brake-Related Products Expected to Gain Momentum Throughout Fiscal Year

LOS ANGELES, CA – August 10, 2026 – Motorcar Parts of America, Inc. ( Nasdaq: MPAA ) today reported financial results for its fiscal 2027 first quarter ended June 30, reflecting timing of orders, with the
company still on target to meet its expectations for the full year.

Positive Drivers:

• | Reaffirms fiscal 2027 net sales guidance between $780 million and $800 million and operating income between $86 million and $91 million, excluding certain non-cash and one-time expenses.

• | Expects to add more than $100 million of additional annualized net sales by the end of fiscal 2027, with annualized net sales to be more than $900 million by the end of fiscal 2027, as referenced in the fiscal year-end release.

• | Significant new business commitments.

• | Additional opportunities are expected from the Centric Parts brand relaunch.

• | Increasing utilization of brake-related capacity to support margin accretion.

Three-Month Results

Net sales for the first quarter
of fiscal 2027 were $168.0 million, compared with $188.4 million in the prior-year period, consistent with the company's expectations. The company is reaffirming its fiscal 2027 guidance. The year-over-year decline in net sales was primarily
attributable to the anticipated timing of customer orders. In addition, certain new business opportunities were temporarily impacted as customers took advantage of inventory liquidations associated with the bankruptcy of a competitor. The company
believes this dynamic has begun to reverse. Net sales during the quarter were also delayed by the planned strategic relocation of the company's Canadian heavy-duty operations to its manufacturing facilities in Mexico.

(more)

Motorcar Parts of America, Inc.

2 - 2 -2

Gross profit for the fiscal 2027 first quarter was $27.2 million compared with $33.9 million a year earlier . Gross margin for the same period was 16.2 percent compared with 18.0 percent a year ago. Gross margin was impacted by non-cash expenses of 2.4 percent and one-time items of 1.6 percent as detailed in Exhibit 2. Excluding these non-cash expenses and certain
one-time cash items, gross margin was 20.2 percent. In addition, the company noted that gross margin was negatively impacted by approximately 2 percent, or $3.5 million, due to foreign currency fluctuations.

Operating income for the fiscal
2027 first quarter was $3.5 million compared with $20.1 million in the prior year. Operating income was impacted by non-cash expenses of $4.7 million, and one-time items of $3.0 million as detailed in Exhibit 4. Operating income for the prior year
benefited from non-cash items of $3.5 million, and partially offset by one-time cash expenses of $1.4 million, as detailed in Exhibit 4. Excluding these non-cash and certain one-time cash items,
operating income was $11.2 million, which includes the $3.5 million unfavorable impact due to foreign currency fluctuations noted above, compared with $18.0 million in the prior year period.

Interest expense for the fiscal 2027 first quarter decreased by $768,000 to $12.0 million from
$12.8 million a year ago, primarily due to lower sales which resulted in lower utilization of accounts receivable discount programs.

Net loss for the fiscal 2027 first quarter was $13.4 million, or $0.71 per share, compared with net
income of $3.0 million, or $0.15 per diluted share, for the prior year. Net loss was impacted by non-cash expenses of $4.6 million, or $0.25 per share, and one-time items of $2.3 million, or $0.12 per share, as detailed in Exhibit 1, and other items
noted above.

"We remain confident about our ability to achieve our annual guidance, notwithstanding some expected sales head winds that we and
the industry experienced in the first quarter," said Selwyn Joffe, chairman, president and chief executive officer.

He reemphasized the company's significant new business commitments and opportunities in North America -- supported by strength across all product lines, in particular the additive Centric Parts brake business with estimated historical gross sales as high as $400 million at the supplier level.

"We have received considerable customer interest in Centric Parts since our recent announcement," Joffe added.

Joffe highlighted the company recently announced the renewal of its loan agreement and extension of the maturity date of the revolver credit facility to August 2031 led by PNC Bank, N.A. The renewal recognizes the company's milestones, solid position within the
automotive aftermarket and management's commitment to strategic growth and profitability.

(more)

Motorcar Parts of America, Inc.

3 - 3 -3

After share repurchases of $1.9 million for the fiscal 2027 first quarter and the recent purchase of Centric Parts brake brands, net bank debt was $99.7
million – reflecting a revolver loan of $118.8 million less cash of $19.1 million at June 30, 2026.

Share Repurchase

During the fiscal 2027 first quarter, the company r epurchased 129,523 shares for $1.9 million at an average share price of $14.98 under its current authorization program. The company has $20.1
million remaining to repurchase shares under its current authorized share repurchase program.

The company anticipates opportunities to build shareholder value through sales gains, enhanced profitability and strong cash generation.

Use of Non-GAAP Measure

This press release includes the following non-GAAP measure – EBITDA, which is not a measure of financial performance under GAAP and
should not be considered as an alternative to net income as a measure of financial performance. The company believes this non-GAAP measure, when considered together with the corresponding GAAP measures, provides useful information to investors and
management regarding financial and business trends relating to the company's results of operations. However, this non-GAAP measure has significant limitations in that it does not reflect all the costs and other items associated with the operation of
the company's business as determined in accordance with GAAP. In addition, the company's non-GAAP measures may be calculated differently and are therefore not comparable to similar measures by other companies. Therefore, investors should consider
non-GAAP measures in addition to, and not as a substitute for, or superior to, measures of financial performance in accordance with GAAP. For a definition and reconciliation of EBITDA to net income, its corresponding GAAP measure, see the financial
tables included in this press release. Also, refer to our Form 8-K to which this release is attached, and other filings we make with the SEC, for further information regarding this measure.

Earnings Conference Call and Webcast

Selwyn Joffe, chairman, president and chief executive officer, and David Lee, chief financial officer, will host an investor conference call today at
10:00 a.m. Pacific time to discuss the company's financial results and operations. The call will be open to all interested investors either through a live Web broadcast via the company's investor relations site at www.motorcarparts.com and
the tab Events and Presentations or by calling (833) 461-5787 (domestic). Meeting ID
406 025 397.

Participants are encouraged to pre-register for the conference call to receive call details and faster access to the event. A listing of dial-in
numbers for international participants is available via: https://help.events.q4inc.com/eahc/international-dial-in-numbers .

For those who are not available to listen to the live broadcast, a replay of the call will be archived on Motorcar Parts of America's investor relations
site www.motorcarparts.com for a seven-day period.

(more)

Motorcar Parts of America, Inc.

4 - 4 -4

About Motorcar Parts of America, Inc.

Motorcar Parts of America, Inc. is a remanufacturer, manufacturer, and distributor of
automotive aftermarket parts -- including alternators, starters, wheel bearings and hub assemblies, brake calipers, brake pads, brake rotors, brake master cylinders, brake power boosters, and diagnostic testing equipment utilized in imported and
domestic passenger vehicles, light trucks, and heavy-duty applications. Its products are sold to automotive retail outlets and the professional repair market throughout the United States, Canada, and Mexico, with facilities located in California,
New York, Mexico, Malaysia, China and India, and administrative offices located in California, Tennessee, Mexico, Singapore, Malaysia, and Canada. In addition, the company's electrical vehicle subsidiary designs and manufactures testing solutions
for performance, endurance, and production of multiple components in the electric power train – providing simulation, emulation, and production applications for the electrification of both automotive and aerospace industries, including electric
vehicle charging systems. Additional information is available at www.motorcarparts.com .

Three Months Ended June 30,
2026 | 2025
Net sales | 168,021,000 | 188,364,000
Cost of goods sold | 140,847,000 | 154,447,000
Gross profit | 27,174,000 | 33,917,000
Operating expenses:
General and administrative | 15,517,000 | 12,680,000
Sales and marketing | 6,546,000 | 6,210,000
Research and development | 3,176,000 | 3,306,000
Foreign exchange impact of lease liabilities and forward contracts | (1,597,000 | (8,348,000
Total operating expenses | 23,642,000 | 13,848,000
Operating income | 3,532,000 | 20,069,000
Other expenses:
Interest expense, net | 12,044,000 | 12,812,000
Change in fair value of compound net derivative liability | 1,540,000 | 1,790,000
Total other expenses | 13,584,000 | 14,602,000
(Loss) income before income tax expense | (10,052,000 | 5,467,000
Income tax expense | 3,369,000 | 2,425,000
Net (loss) income | (13,421,000 | 3,042,000
Basic net (loss) income per share | (0.71 | 0.16
Diluted net (loss) income per share | (0.71 | 0.15
Weighted average number of shares outstanding:
Basic | 18,922,938 | 19,369,060
Diluted | 18,922,938 | 19,917,663

MOTORCAR PARTS OF AMERICA, INC. AND SUBSIDIARIES

Consolidated Balance Sheets

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-06-08_item7_mdna.md)

_Extraction: started at the Overview heading._

Overview

We had working capital (current assets minus current liabilities) of $184,386,000 and $160,446,000, a ratio of current assets to current liabilities of 1.5:1.0 at March 31, 2026 and 2025, respectively.

Our primary source of liquidity was from cash generated from operations and the use of our accounts receivable discount programs during the year ended March 31, 2026. We believe our cash generated from operations, cash and cash equivalents, use of accounts receivable discount programs, and amounts available under our credit facility are sufficient to satisfy our expected future liquidity needs over the next 12 months.

Cash Flows

The following summarizes cash flows as reflected in the consolidated statements of cash flows:

Fiscal Years Ended March 31,
2026 | 2025 | 2024
Cash provided by (used in):
Operating activities | 19,158,000 | 45,477,000 | 39,172,000
Investing activities | (3,590,000 | (4,469,000 | (479,000
Financing activities | (10,980,000 | (44,655,000 | (36,439,000
Effect of exchange rates on cash and cash equivalents | 633,000 | (898,000 | 124,000
Net increase (decrease) in cash and cash equivalents | 5,221,000 | (4,545,000 | 2,378,000
Additional selected cash flow data:
Depreciation and amortization | 9,788,000 | 10,400,000 | 11,619,000
Capital expenditures | 3,696,000 | 4,578,000 | 1,000,000

Fiscal 2026 Compared with Fiscal 2025

Net cash provided by operating activities was $19,158,000 and $45,477,000 for fiscal 2026 and 2025, respectively. Our operating activities were primarily impacted by the following changes in our working capital: (i) the build-up of our inventory to support future sales and (ii) higher accounts receivable balances resulting from increased sales that will be collected in future periods. In addition, our operating activities were further impacted by changes in operating results (net income (loss) plus the net add-back for non-cash transactions in earnings). We continue to manage our working capital to maximize our operating cash flow.

Net cash used in investing activities was $3,590,000 and $4,469,000 for fiscal 2026 and 2025, respectively. The change in our investing activities primarily resulted from decreased capital expenditures.

Net cash used in financing activities was $10,980,000 and $44,655,000 for fiscal 2026 and 2025, respectively. The change in our financing activities primarily resulted from (i) net borrowing of $3,881,000 in fiscal 2026 compared with net repayments of $37,213,000 in fiscal 2025, under our revolving facility and (ii) the repurchase of 955,608 shares of our common stock for $11,351,000 in fiscal 2026 compared with 542,134 shares of our common stock for $4,832,000 in fiscal 2025.

Fiscal 2025 Compared with Fiscal 2024

A discussion of the changes in our operating activities, investing activities, and financing activities for the year ended March 31, 2025, as compared with the year ended March 31, 2024, has been omitted from this Form 10-K but may be found in Item 7. "Management's Discussion and Analysis of Financial Condition and Results of Operations" of the annual report on Form 10-K for the year ended March 31, 2025, filed with the SEC on June 9, 2025, which is available free of charge on the SEC's website at www.sec.gov by searching with our ticker symbol "MPAA" or at our internet address, www.motorcarparts.com , by clicking "Investors/Financials/SEC Filings" located at the top of the page.

Capital Resources

Credit Facility

We are party to a $268,620,000 senior secured financing, (as amended from time to time, the "Credit Facility") with a syndicate of lenders, and PNC Bank, National Association, as administrative agent, consisting of (i) a $238,620,000 revolving loan facility, subject to borrowing base restrictions, a $24,000,000 sublimit for borrowings by Canadian borrowers, and a $20,000,000 sublimit for letters of credit (the "Revolving Facility") and (ii) a $30,000,000 term loan facility (the "Term Loans"). The Term Loans were repaid during the year ended March 31, 2024. The Credit Facility matures on December 12, 2028. The lenders have a security interest in substantially all of our assets.

We had $94,668,000 and $90,787,000 outstanding under the Revolving Facility at March 31, 2026 and 2025, respectively. In addition, $15,470,000 was outstanding for letters of credit at March 31, 2026. At March 31, 2026, after certain contractual adjustments, $119,048,000 was available under the Revolving Facility. The interest rate on our Revolving Facility was 6.79% and 7.46%, at March 31, 2026 and 2025, respectively.

The Credit Facility requires us to maintain a minimum fixed charge coverage ratio if undrawn availability is less than 22.5% of the aggregate revolving commitments and a specified minimum undrawn availability. During the year ended March 31, 2026, undrawn availability was greater than the 22.5% threshold, therefore, the fixed charge coverage ratio financial covenant was not required to be tested.

Convertible Notes, Related Party

On March 31, 2023, we entered into a note purchase agreement, as amended, (the "Note Purchase Agreement") with Bison Capital Partners VI, L.P. and Bison Capital Partners VI-A, L.P. (collectively, the "Purchasers") and Bison Capital Partners VI, L.P., as the purchaser representative (the "Purchaser Representative") for the issuance and sale of $32,000,000 in aggregate principal amount of convertible notes due in 2029 (the "Convertible Notes"), which was used for general corporate purposes. The Convertible Notes bear interest at a rate of 10.0% per annum, compounded annually, and payable (i) in kind or (ii) in cash, annually in arrears on April 1 of each year. In April 2025, non-cash accrued interest on the Convertible Notes of $3,521,000 was paid in-kind and is included in the principal amount of Convertible Notes at March 31, 2026. In April 2024, non-cash accrued interest on the Convertible Notes of $3,209,000 was paid in-kind and is included in the principal amount of Convertible Notes at March 31, 2025.

The aggregate proceeds from the offering were approximately $31,280,000, net of initial purchasers' fees and other related expenses. The initial conversion rate is 66.6667 shares of our common stock per $1,000 principal amount of notes (equivalent to an initial conversion price of approximately $15.00 per share of common stock). At March 31, 2026, we had 28,680,086 shares of our common stock available to be issued if the Convertible Notes were converted.

In connection with the Note Purchase Agreement, we entered into common stock warrants (the "Warrants") with the Purchasers, which mature on March 30, 2029. The Warrants do not become exercisable unless a Company Redemption (as defined below) occurs and the volume weighted average price of our common stock for 20 consecutive days prior to the redemption is less than $15.00. The fair value of the Warrants, using Level 3 inputs and the Monte Carlo simulation model, was zero at March 31, 2026 and 2025. We estimate the fair value of the Warrants at each balance sheet date. Any subsequent changes from the initial recognition in the fair value of the Warrants will be recorded in current period earnings in the consolidated statements of operations.

The Convertible Notes may be converted, subject to certain conditions, at an initial conversion price of $15.00, subject to adjustment as provided in the Convertible Notes (the "Conversion Option"). The Convertible Notes also include a provision for a return of interest ("Return of Interest"), which requires the Purchasers to return 15.0% of the interest paid to us in certain circumstances, subject to reduction of the Return of Interest amount in the event that the Return of Interest amount would result in total payments to the Purchasers of less than two times the original principal amount. The Return of Interest provision is accounted for as part of the Conversion Option and if the Conversion Option is exercised in the future, the Return of Interest provision will remain outstanding until the Purchaser sells all of the underlying stock received upon conversion. Upon conversion, any value associated with the Return of Interest provision will be reflected as a derivative asset upon conversion, with changes in fair value being recorded in earnings in the consolidated statements of operations until settlement in connection with the sale of the underlying stock by the Purchaser. Unless and until we deliver a redemption notice, the Purchasers of the Convertible Notes may convert their Convertible Notes at any time at their option. Upon conversion, the Convertible Notes will be settled in shares of our common stock. The conversion rate and conversion price are subject to customary adjustments upon the occurrence of certain events. The Convertible Notes have a stated maturity of March 30, 2029, subject to earlier conversion or redemption in accordance with their terms.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-06-08_item1_business.md)

Item 1.

Business

General

We are a leading supplier of automotive aftermarket non-discretionary replacement parts and test solutions and diagnostic equipment -- building upon industry leading technology to be "The Global Leader for Parts and Solutions that Move Our World Today and Tomorrow" . We operate in the $130 billion automotive aftermarket for replacement hard parts in North America. Our hard parts products include light-duty rotating electrical products and brake-related products. In addition, we sell test solutions and diagnostic equipment, which were added with our acquisitions of D&V Electronics Ltd. in July 2017 and Mechanical Power Conversion, LLC in December 2018 and heavy-duty rotating electrical products, which were added with our January 2019 acquisition of Dixie Electric, Ltd.

The automotive aftermarket is divided into two markets. The first is the do-it-yourself ("DIY") market, which is generally serviced by the large retail chain outlets and online resellers. Consumers who purchase parts from the DIY market generally install parts into their vehicles themselves. In most cases, this is a less expensive alternative than having the repair performed by a professional installer. The second is the professional installer market, commonly known as the do-it-for-me ("DIFM") market. Traditional warehouse distributors, dealer networks, and commercial divisions of retail chains service this market. Generally, the consumer in this market is a professional parts installer. Our products are distributed to both the DIY and DIFM markets. The distinction between these two markets has become less defined over the years, as retail outlets leverage their distribution strength and store locations to attract customers.

D emand for replacement parts generally increases with the age of vehicles and miles driven, which provides favorable opportunities for sales of our products. The current population of light-duty vehicles in the U.S. is approximately 296 million, and the average age of these vehicles is approximately 13 years and is expected to continue to grow, in particular during recession years. Although miles driven can fluctuate for various reasons, including fuel prices, they have been generally increasing for several years.

In addition, we operate in the $11 billion-plus rapidly emerging global market for automotive test solutions and diagnostic equipment and see the opportunity for accelerating growth rates for today and the future as electrification becomes increasingly important around the world. We also operate in the $40 billion market for medium and heavy-duty automotive aftermarket replacement parts for truck, industrial, marine, and agricultural applications.

Growth Strategies and Key Initiatives

With a scalable infrastructure and abundant growth opportunities, we continue to focus on strategic growth by leveraging our competitive advantage and growing our industry position by providing innovative and intuitive solutions to our customers.

To accomplish our strategic vision, we are focused on the following key initiatives:

Hard Parts

●

Grow our current product lines both with existing and potential new customers. We continue to develop and offer current and new sales programs to ensure that we are supporting our customers' business needs. We remain dedicated to managing growth and continuing to focus on enhancements to our infrastructure and making investments in resources to support our customers. We have globally positioned manufacturing and distribution centers to support our continuous growth.

●

Introduction of new product lines. While we have not introduced any new product lines recently, we have expanded our new product introduction in existing product lines, and we continue to engage with our customers to identify potential new product opportunities to grow our business.

●

Creating value for our customers. A core part of our strategy is ensuring that we add meaningful value for our customers. We consistently support and pilot our customers' supply management initiatives in addition to providing demand analytics, inventory management services, online training guides, and market share and retail store layout information to our customers.

●

Technological innovation. We continue to develop in-house technologies and advanced testing methods. This elevated level of technology aims to deliver our customers high quality products and support services.

●

Leverage our manufacturing capacity and supply chain sourcing. We continue to focus on improving our manufacturing efficiencies and supply chain costs. This includes (i) leveraging manufacturing capacity to meet demand across all non-discretionary product lines, (ii) capitalizing on our existing operations in Mexico with volume and efficiency benefits, and (iii) ongoing focus on lowering supply chain sourcing, particularly lower-tariff cost locations.

Test Solutions and Diagnostic Equipment

●

We provide industry-leading test solutions and diagnostic equipment to both original equipment manufacturers and the aftermarket. We are continuously upgrading our equipment to accommodate testing for the latest alternator and starter technology for both existing and new customers. These software and hardware upgrades are also available for existing products that the customer is using. In addition, we provide industry leading maintenance and service support to provide a better end-user experience and value to our customers.

●

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

- **CALL PERIOD: 2027Q1** (call dated 2026-08-10)
- **Recency:** same fiscal period as the latest earnings release in this pack.
- **File:** transcript_2027Q1_2026-08-10.md
- **Type:** EARNINGS PRESS RELEASE ONLY, not the call — no Q&A, no unscripted management commentary. Do not attribute call quotes to this.
- **Source:** https://www.sec.gov/Archives/edgar/data/918251/000114036126031937/ef20079233_ex99-1.htm

Exhibit 99.1

NEWS RELEASE

CONTACT:

Gary S. Maier

Vice President, Corporate Communications & IR

(310) 972-5124

MOTORCAR PARTS OF AMERICA REPORTS FISCAL 2027 FIRST QUARTER RESULTS

Company Reaffirms Full-Year Guidance;

Brake-Related Products Expected to Gain Momentum Throughout Fiscal Year

LOS ANGELES, CA – August 10, 2026 –
Motorcar Parts of America, Inc. (
Nasdaq: MPAA
) today reported financial results for its fiscal 2027 first quarter ended June 30, reflecting timing of orders, with the
company still on target to meet its expectations for the full year.

Positive Drivers:

•

Reaffirms fiscal 2027 net sales guidance between $780 million and $800 million and operating income between $86 million and $91 million, excluding certain non-cash and one-time expenses.

•

Expects to add more than $100 million of additional annualized net sales by the end of fiscal 2027, with annualized net sales to be more than $900 million by the end of fiscal 2027, as referenced in
the fiscal year-end release.

•

Significant new business commitments.

•

Additional opportunities are expected from the Centric Parts brand relaunch.

•

Increasing utilization of brake-related capacity to support margin accretion.

Three-Month Results

Net sales
for the first quarter
of fiscal 2027 were $168.0 million, compared with $188.4 million in the prior-year period, consistent with the company’s expectations. The company is reaffirming its fiscal 2027 guidance. The year-over-year decline in net sales was primarily
attributable to the anticipated timing of customer orders. In addition, certain new business opportunities were temporarily impacted as customers took advantage of inventory liquidations associated with the bankruptcy of a competitor. The company
believes this dynamic has begun to reverse. Net sales during the quarter were also delayed by the planned strategic relocation of the company’s Canadian heavy-duty operations to its manufacturing facilities in Mexico.

(more)

Motorcar Parts of America, Inc.

2
-
2
-2

Gross profit
for the fiscal
2027 first
quarter was
$27.2 million compared with $33.9 million a year earlier
.
Gross margin
for the same period was 16.2 percent compared with 18.0 percent a year
ago. Gross margin was impacted by non-cash expenses of 2.4 percent and one-time items of 1.6 percent as detailed in Exhibit 2.
Excluding these non-cash expenses and certain
one-time cash items, gross margin was 20.2 percent. In addition, the company noted that gross margin was negatively impacted by approximately 2 percent, or $3.5 million, due to foreign currency fluctuations.

_[...truncated at ~3,000 chars of this document]_

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-06-08_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-06-08_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-06-08_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-10_2-02-results.md, 10-K_2026-06-08_item7_mdna.md, 10-K_2026-06-08_item1_business.md, transcript_2027Q1_2026-08-10.md

**Missing:** none

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
