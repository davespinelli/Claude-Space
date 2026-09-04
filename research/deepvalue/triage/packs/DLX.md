# Triage pack — DLX · DELUXE CORP

_Generated 2026-09-04 16:12 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** DLX · **Name:** DELUXE CORP
- **CIK:** 0000027996
- **SIC:** 2780 — Blankbooks, Looseleaf Binders & Bookbindg & Relatd Work
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/DLX

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** DELUXE CORP
- **CIK:** 27,996 · **SIC:** 2780 (Blankbooks, Looseleaf Binders & Bookbindg & Relatd Work) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 24.40 |
| mktcap | $1.1B |
| ev | $2.4B |
| ev_ebit | 10.5x |
| fcf | $175.3M |
| fcf_yield | 15.7% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | $1.3B |
| net_debt_ebit | 5.7x |
| cash | $34.9M |
| ltd | $1.4B |
| equity | n/a |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $2.1B |
| revenue_prior | $2.1B |
| rev_growth | 0.5% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $232.4M |
| net_income | $82.1M |
| cfo | $270.6M |
| capex | $95.3M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 2.2% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 45,856,290 |
| shares_py | 44,885,245 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 45.7% |
| r6m | -11.0% |
| off_52w_high | -21.6% |
| adv20 | $10.7M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.83 |
| r_ev_ebit | 0.74 |
| r_roic | 0.50 |
| r_rev_growth | 0.36 |
| r_buyback | 0.32 |
| score | 0.60 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | n/a |
| shares_period | CY2026Q2I |
| shares_py_period | CY2025Q2I |
| capex_missing | False |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 146 |

**Screen rationale:** top-quartile FCF yield 15.7%; 12-1 momentum 45.7%


## 3. Share count trend

- Shares outstanding: **45,856,290** (CY2026Q2I) vs **44,885,245** prior year (CY2025Q2I)
- Change: **2.2%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-31** — Item 1.01 (Entry into a Material Definitive Agreement): Corporation (the "Company") and certain subsidiaries of the Company party thereto, as guarantors, entered into a Refinancing
- **2026-06-18** — Item 1.01 (Entry into a Material Definitive Agreement): Corporation (the "Company") entered into an Equity Purchase Agreement and Plan of Merger (the "Purchase Agreement")
- **2026-03-09** — Item 5.02 (Departure of Directors or Certain Officers; Election of): Directors; Appointment of Certain Officers; Compensatory Arrangements of Certain Officers.

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 25 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 10 |
| F | 1 |
| M | 14 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-05_2-02-results.md)

_Extraction: started at the first release heading, 'DELUXE REPORTS STRONG SECOND QUARTER 2026 RESULTS'; skipped 7 forward-looking-statement block(s); 6 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (exhibit991080520268-k.htm)

DELUXE REPORTS STRONG SECOND QUARTER 2026 RESULTS

INCREASES FULL-YEAR OUTLOOK TO INCLUDE CELERO ACQUISITION

• Reported revenue decreased 4.2%, inclusive of impact of in-year divestiture.

• Comparable adjusted revenue increased 2.6%, driven by 9.7% growth in combined Payments and Data segments.

• Cash from operating activities increased 32.1% to $133.9 million for the first half of the year; free cash flow increased 64.9% to $85.9 million.

• Inclusive of one-time Celero transaction costs, second quarter net income was $19.2 million, compared to $22.4 million in 2025.

• Comparable adjusted EBITDA increased 5.3% to $108.8 million.

• GAAP diluted EPS was $0.41 versus $0.50 in 2025; comparable adjusted diluted EPS improved 6.1% to $0.87.

• Provides updated 2026 guidance increasing revenue and adjusted EBITDA ranges to incorporate post-closing forecast for Celero acquisition.

Minneapolis – August 5, 2026 – Deluxe (NYSE: DLX), a trusted Payments and Data company, today reported operating results for its second quarter ended June 30, 2026.

"We increased free cash flow in the first half of the year by 65% and posted solid growth in comparable adjusted revenue, EBITDA and EPS," said Barry McCarthy, President and CEO of Deluxe. "The combined Payments and Data segments grew 11% year-to-date and accounted for 52% of total revenue. These results highlight our ability to consistently improve financial performance while executing on our strategic revenue mix shift goal. The addition of Celero decisively further shifts our mix towards Payments and Data, and our proven execution ability gives us confidence in our integration path."

"Our second quarter operating results continued to demonstrate focus against core capital allocation priorities, as we extended our strong cash generation and reduced overall debt balances during the period," said Chip Zint, Senior Vice President and Chief Financial Officer of Deluxe. "The extension of our amended credit facility maturities to 2031 further enhances liquidity and our long-term balance sheet position. As the Celero business comes aboard, we will focus on driving near-term synergy capture and continued robust earnings expansion across the combined enterprise."

Second Quarter 2026 Financial Highlights

(in millions, except per share amounts)

2 nd Quarter 2026 | 2 nd Quarter 2025 | % Change
Revenue | $499.3 | $521.3 | (4.2 | %)
Comparable Adjusted Revenue | $499.3 | $486.8 | 2.6 | %
Net Income | $19.2 | $22.4 | (14.3 | %)
Comparable Adjusted EBITDA | $108.8 | $103.3 | 5.3 | %
Diluted EPS | $0.41 | $0.50 | (18.0 | %)
Comparable Adjusted Diluted EPS | $0.87 | $0.82 | 6.1 | %

• Revenue for the second quarter decreased 4.2% from the previous year. Comparable adjusted revenue, reflecting the impact of a first quarter business exit, increased 2.6% compared to the previous year.

• Net income of $19.2 million declined from $22.4 million in the second quarter of 2025, as one-time acquisition-related costs and a slightly higher tax provision offset lower overall SG&A, restructuring, and interest expense for the period.

• Comparable adjusted EBITDA margin was 21.8%, up 60 basis points from the prior year.

• Comparable adjusted diluted EPS of $0.87 was up 6.1% year over year.

Outlook

The Company updated guidance for full year 2026 to reflect the closing of the Celero transaction as of July 31, as follows:

• Revenue of $2.095 to $2.12 billion

• Adjusted EBITDA of $455 to $475 million

• Adjusted diluted EPS of $3.60 to $4.00

• Free cash flow of approximately $200 million

This guidance remains subject to, among other things, prevailing macroeconomic conditions, global instability, including tariffs, labor supply challenges, and inflation, as well as the impact of other potential changes to the company's portfolio.

Capital Allocation and Dividend

The Board of Directors recently approved a regular quarterly dividend of $0.30 per share. The dividend will be payable on September 1, 2026, to shareholders of record as of market closing on August 18, 2026.

Earnings Call Information

Deluxe management will host a conference call today at 5:00 p.m. ET (4:00 p.m. CT) to review the financial results and updated outlook. Listeners can access the call by dialing 1-800-330-6730 (conference passcode: 541871). The audio and accompanying slides will be available via a simultaneous webcast accessible through the investor relations website at www.investors.deluxe.com . A replay will be available after 8:00 p.m. ET through midnight on August 12, 2026, via the webcast link and listen-by-phone option.

About Deluxe Corporation

Deluxe, a trusted Payments and Data company, champions business so communities thrive. Our solutions help businesses pay, get paid, and grow. For more than 100 years, Deluxe customers have relied on our solutions and platforms at all stages of their lifecycle, from start-up to maturity. Our powerful scale supports millions of small businesses, thousands of vital financial institutions, and hundreds of the world's largest consumer brands, while processing more than $2 trillion in annual payment volume. Our reach, scale, and distribution channels position Deluxe to be our customers' most trusted business partner. To learn how we can help your business, visit us at www.deluxe.com , www.facebook.com/deluxecorp , www.linkedin.com/company/deluxe , or www.x.com/deluxe .

Quarter Ended June 30, | Six Months Ended June 30,
2026 | 2025 | 2026 | 2025
Revenue | $499.3 | $521.3 | $1,037.4 | $1,057.7
Cost of revenue | (239.7) | (242.0) | (498.4) | (497.4)
Selling, general and administrative expense | (202.1) | (214.5) | (411.5) | (439.8)
Restructuring and integration expense | (1.8) | (4.0) | (5.2) | (11.7)
Gain on sale of businesses and long-lived assets | — | — | 5.1 | —
Operating income | 55.7 | 60.8 | 127.4 | 108.8
Interest expense | (28.0) | (30.9) | (55.6) | (62.2)
Other income, net | 2.4 | 1.8 | 4.9 | 4.3
Income before income taxes | 30.1 | 31.7 | 76.7 | 50.9
Income tax provision | (10.9) | (9.3) | (21.7) | (14.4)
Net income | 19.2 | 22.4 | 55.0 | 36.5
Non-controlling interest | (0.1) | — | (0.1) | (0.1)
Net income attributable to Deluxe | $19.1 | $22.4 | $54.9 | $36.4
Weighted average dilutive shares | 46.4 | 45.2 | 46.3 | 45.2
Diluted earnings per share | $0.41 | $0.50 | $1.18 | $0.80
Adjusted diluted earnings per share | 0.87 | 0.88 | 1.92 | 1.62
Comparable adjusted diluted earnings per share | 0.87 | 0.82 | 1.92 | 1.54
Depreciation and amortization expense | 36.2 | 33.5 | 72.9 | 68.8
EBITDA | 94.2 | 96.1 | 205.1 | 181.8
Adjusted EBITDA | 108.8 | 106.5 | 226.7 | 206.6
Comparable adjusted EBITDA | 108.8 | 103.3 | 226.7 | 201.7

DELUXE CORPORATION

CONSOLIDATED CONDENSED BALANCE SHEETS

(dollars and shares in millions)

(Unaudited)

June 30, 2026 | December 31, 2025
Cash and cash equivalents | $34.9 | $36.9
Other current assets | 339.2 | 628.9
Goodwill | 1,422.8 | 1,422.8
Intangibles | 327.8 | 348.4
Property, plant and equipment | 141.4 | 101.0
Operating lease assets | 39.4 | 43.0
Other non-current assets | 256.9 | 282.6
Total assets | $2,562.4 | $2,863.6
Current portion of long-term debt | $— | $16.3
Other current liabilities | 312.9 | 626.9
Long-term debt | 1,352.2 | 1,413.1
Finance lease liabilities | 75.4 | 25.8
Operating lease liabilities | 36.0 | 39.8
Other non-current liabilities | 78.0 | 61.0
Shareholders' equity | 707.9 | 680.7
Total liabilities and shareholders' equity | $2,562.4 | $2,863.6
Net debt | $1,317.3 | $1,392.5
Shares outstanding | 45.8 | 45.0

DELUXE CORPORATION

CONSOLIDATED CONDENSED STATEMENTS OF CASH FLOWS

(in millions)

(Unaudited)

Six Months Ended June 30,
2026 | 2025
Cash provided (used) by:
Operating activities:
Net income | $55.0 | $36.5
Depreciation and amortization of intangibles | 72.9 | 68.8
Gain on sale of businesses and long-lived assets | (5.1) | —
Other | 11.1 | (3.9)
Total operating activities | 133.9 | 101.4
Investing activities:
Purchases of capital assets | (48.0) | (49.3)
Proceeds from company-owned life insurance policies | 34.0 | —
Proceeds from sale of businesses and long-lived assets | 10.8 | 2.0
Other | 2.0 | 3.0
Total investing activities | (1.2) | (44.3)
Financing activities:
Net change in debt | (79.4) | (34.3)
Dividends | (29.2) | (28.1)
Change in settlement processing obligations | (255.7) | (258.4)
Other | (25.9) | (5.5)
Total financing activities | (390.2) | (326.3)
Effect of exchange rate change on cash, cash equivalents, restricted cash, and restricted cash equivalents | (1.1) | 1.5
Net change in cash, cash equivalents, restricted cash, and restricted cash equivalents | (258.6) | (267.7)
Cash, cash equivalents, restricted cash, and restricted cash equivalents, beginning of year | 313.0 | 309.2
Cash, cash equivalents, restricted cash, and restricted cash equivalents, end of period | $54.4 | $41.5
Free cash flow | $85.9 | $52.1

DELUXE CORPORATION

SEGMENT INFORMATION

(In millions)

(Unaudited)

Quarter Ended June 30, | Six Months Ended June 30,
2026 | 2025 | 2026 | 2025
Revenue:
Merchant Services | $107.6 | $101.4 | $212.5 | $199.2
B2B Payments | 73.5 | 71.0 | 147.1 | 141.1
Data Solutions | 82.3 | 67.8 | 179.7 | 145.1
Print | 235.9 | 281.1 | 498.1 | 572.3
Total | $499.3 | $521.3 | $1,037.4 | $1,057.7
Comparable Adjusted Revenue | $499.3 | $486.8 | $1,037.4 | $1,010.6
Adjusted EBITDA:
Merchant Services | $25.1 | $21.7 | $51.8 | $43.1
B2B Payments | 18.3 | 15.6 | 35.5 | 28.9
Data Solutions | 18.1 | 20.4 | 41.0 | 40.0
Print | 86.0 | 90.4 | 171.7 | 181.2
Corporate | (38.7) | (41.6) | (73.3) | (86.6)
Total | $108.8 | $106.5 | $226.7 | $206.6
Comparable Adjusted EBITDA | $108.8 | $103.3 | $226.7 | $201.7
Adjusted EBITDA Margin:
Merchant Services | 23.3 | % | 21.4 | % | 24.4 | % | 21.6 | %
B2B Payments | 24.9 | % | 22.0 | % | 24.1 | % | 20.5 | %
Data Solutions | 22.0 | % | 30.1 | % | 22.8 | % | 27.6 | %
Print | 36.5 | % | 32.2 | % | 34.5 | % | 31.7 | %
Total | 21.8 | % | 20.4 | % | 21.9 | % | 19.5 | %
Comparable Adjusted EBITDA | 21.8 | % | 21.2 | % | 21.9 | % | 20.0 | %

Segment information was calculated using the methodology described in the Notes to Consolidated Financial Statements in the company's Annual Report on Form 10-K for the year ended December 31, 2025. The reconciliation of the comparable GAAP financial measure to consolidated adjusted EBITDA, comparable adjusted revenue, and comparable adjusted EBITDA is provided on a following page.

DELUXE CORPORATION

RECONCILIATION OF GAAP TO NON-GAAP MEASURES

(in millions)

(Unaudited)

The company has not reconciled the adjusted EBITDA, adjusted diluted EPS, or free cash flow outlook for 2026 to the directly comparable GAAP financial measures because the company does not provide outlook guidance for the reconciling items between net income, adjusted net income, and adjusted EBITDA, and some of these reconciling items affect cash flows from operating activities. Due to the significant uncertainty and variability associated with certain forward-looking reconciling items such as restructuring and integration expense, gains and losses on sales of businesses and long-lived assets, and certain legal and environmental expenses, a reconciliation of the outlook for these non-GAAP financial measures to the corresponding GAAP measures is not available without unreasonable effort. The potential impact of these reconciling items is substantial and, based on past experience, could be material.

Management does not consider the non-GAAP measures presented below to be substitutes for GAAP performance measures, but believes they are useful performance measures that should be considered in addition to GAAP performance measures.

EBITDA, ADJUSTED EBITDA, AND ADJUSTED EBITDA MARGIN

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-13_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

EXECUTIVE OVERVIEW

We empower businesses to build stronger customer relationships through a broad range of trusted, technology-enabled solutions designed to facilitate payments, drive growth, and improve operational efficiency. Our comprehensive portfolio includes merchant services solutions, marketing and data analytics, treasury management solutions, and promotional products, as well as customized checks and business forms tailored to our clients' needs.

We serve a diverse customer base, including small and medium-sized businesses, financial institutions, and some of the world's leading consumer brands. In addition, we offer checks and related accessories directly to individual consumers. Our extensive reach, scale, and multi-channel distribution network enable us to deliver innovative solutions and reliable support, positioning us as a valued partner to our customers.

Our Strategy

A comprehensive discussion of our strategy is provided in Part I, Item 1 of this report. With our infrastructure modernization largely complete and non-strategic businesses divested, our attention is on growth investments that drive scale and accelerate profit growth ahead of revenue. Our disciplined pricing strategies and rigorous cost management continue to support operational excellence.

Over the past three years, we successfully executed our North Star program, a comprehensive, multi-year initiative designed to enhance shareholder value by accelerating adjusted EBITDA growth, increasing cash flow, reducing debt, and improving our leverage ratio. The positive impact of the North Star program is reflected in our 2025 results, with both adjusted EBITDA and adjusted EBITDA margin increasing year-over-year. These improvements were driven in part by a 3.9% reduction in selling, general and administrative (SG&A) expense. Within our Print segment, our continued focus on driving efficiencies contributed to adjusted EBITDA margin improvement in 2025, despite continued revenue pressures in that business. We also

achieved a $76.3 million year-over-year increase in net cash provided by operating activities and reduced total debt by $73.7 million from the previous year-end. These results underscore our commitment to disciplined execution and the creation of long-term shareholder value.

In August 2025, we acquired certain assets of JPMorgan Chase Bank's CheckMatch electronic check conveyance service business for cash payments totalling $24.6 million, approximately half of which was paid at closing and the remainder due in the first quarter of 2026. This acquisition is expected to enhance our market position and extend the scale of our B2B Payments segment.

In February 2026, we entered into an agreement to sell certain assets and liabilities related to the small business distributor channel in our Print segment for approximately $25.0 million, with approximately half paid at closing and the remainder due over the next three years. The sale is expected to close in the first quarter of 2026.

2025 Financial Results

Below are highlights of our financial performance for 2025, compared to the prior year.

• Consolidated revenue – Increased by $11.4 million to $2.13 billion, including a decrease of $10.8 million attributable to business exits. The increase in revenue was mainly due to growth in our data-driven marketing and merchant services businesses. This growth was partially offset by weaker demand for certain of our promotional products, the ongoing secular decline in order volumes for checks, business forms, and various business accessories, as well as the impact of business exits.

• Net income – Increased by $29.3 million to $82.2 million, reflecting the benefits of our pricing strategies and cost management initiatives. The increase also resulted from lower amortization expense, due to accelerated amortization associated with business exits and a trade name intangible asset in 2024, as well as lower acquisition-related amortization in 2025. Restructuring and integration expense also declined, and our data-driven marketing business delivered year-over-year growth, further contributing to the improvement.

These positive factors were partially offset by weaker demand for certain promotional products and the continuing secular declines in the Print segment, inflationary pressures on materials and delivery costs, and the loss of earnings from exited businesses. Additionally, in 2024, we recognized a $31.2 million gain from the sale of businesses and long-lived assets, which did not recur in 2025.

.

• Adjusted EBITDA – Increased $19.4 million to $431.5 million, including the impact of business exits, which drove a $5.6 million decrease year-over-year. The increase in adjusted EBITDA was primarily driven by the benefits of our pricing strategies and cost management initiatives, and growth in data-driven marketing. These positive impacts were partially offset by the weaker demand for certain promotional products, ongoing secular declines in the Print segment, and inflationary cost pressures.

Adjusted EBITDA margin increased to 20.2% in 2025, compared to 19.4% in 2024. The margin improvement was primarily driven by our pricing strategies and cost management initiatives, partially offset by inflationary pressures. A reconciliation of net income to adjusted EBITDA can be found in the Consolidated Results of Operations section.

• Net cash provided by operating activities – Increased by $76.3 million to $270.6 million. Key contributors included the positive impacts of our pricing and cost management actions, lower income tax payments, mainly from foreign operations, reduced performance-based employee bonus payouts, and lower restructuring and integration expenditures. Additional positive impacts came from growth and volume-based rebates in our data-driven marketing business.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

CONSOLIDATED RESULTS OF OPERATIONS

Consolidated Revenue

(in millions) | 2025 | 2024 | Change
Total revenue | 2,133.2 | 2,121.8 | 0.5%

Total revenue increased in 2025 compared to 2024, including the impact of business exits, which reduced revenue by $10.8 million. The increase in revenue was driven by robust demand for our data-driven marketing services, particularly from financial institutions, which contributed a $73.5 million year-over-year improvement. Strategic price increases implemented in response to inflation, particularly within our Print and Merchant Services segments, also supported revenue growth. These positive factors were partially offset by softer demand for certain promotional products, the continued secular decline in order volumes for checks, business forms, and various business accessories, as well as the impact of business exits.

We do not manage our business based on product versus service revenue. Instead, we analyze our revenue based on the product and service offerings shown under the caption "Note 15: Business Segment Information" in the Notes to Consolidated Financial Statements located in Part II, Item 8 of this report. Our revenue mix by business segment was as follows:

2025 | 2024
Merchant Services | 18.7 | % | 18.1 | %
B2B Payments | 13.6 | % | 13.6 | %
Data Solutions | 14.4 | % | 11.0 | %
Print | 53.3 | % | 56.8 | %
All other | — | 0.5 | %
Total revenue | 100.0 | % | 100.0 | %

Consolidated Cost of Revenue

(in millions) | 2025 | 2024 | Change
Total cost of revenue | 1,002.5 | 995.3 | 0.7%
Total cost of revenue as a percentage of total revenue | 47.0 | % | 46.9 | % | 0.1 pt.

Cost of revenue primarily includes raw materials for product manufacturing, shipping and handling, third-party costs for outsourced products and services, payroll and related expenses, information technology costs, depreciation and amortization of production and digital assets, residuals paid to independent sales organization (ISOs), and related overhead.

Total cost of revenue increased in 2025 compared to 2024, primarily due to the revenue growth in our data-driven marketing business and ongoing inflationary pressures on materials and delivery costs. These increases were partially offset by softer demand for certain promotional products and the continued secular decline in checks, business forms, and various business accessories in our Print segment. Our cost management initiatives, including volume-based rebates in Data Solutions, also helped mitigate some of the cost increases. Additionally, business exits reduced costs by approximately $11.0 million, including the impact of accelerated amortization expense recognized in 2024.

As a percentage of total revenue, total cost of revenue remained relatively flat in 2025 compared to 2024. Inflationary pressures on our cost structure and a shift in revenue mix toward our lower-margin growth businesses were offset by the benefits of our pricing strategies and cost management actions, as well as the absence of accelerated amortization expense recognized in the prior year.

Consolidated SG&A Expense

(in millions) | 2025 | 2024 | Change
SG&A expense | 873.3 | 909.2 | (3.9%)
SG&A expense as a percentage of total revenue | 40.9 | % | 42.9 | % | (2.0) pt.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-13_item1_business.md)

ITEM 1. BUSINESS

COMPANY OVERVIEW

In 2025, Deluxe Corporation proudly celebrated its 110th anniversary, marking over a century of business excellence. Our enduring success is a testament to our innovation, our ability to adapt to the evolving needs of our customers, and the trust they place in us. We have transformed into a trusted Payments and Data company, serving small and medium-sized businesses, financial institutions, and some of the world's largest consumer brands. Our products and services are delivered through four business segments, primarily catering to clients and customers across North America.

Business Segment | Category | Percentage of 2025 consolidated revenue | Description
Merchant Services | Merchant services solutions | 18.7 | % | Merchant in-store, online, and mobile payment solutions that provide tools to accept electronic payments, such as debit cards, credit cards, and other forms of payment
B2B Payments | Treasury management solutions | 10.5 | % | Automated receivables technology, including remittance and lockbox processing, remote deposit capture, and cash application, as well as payment acceptance solutions
Other payment solutions | 3.1 | % | Integrated accounts payable disbursements, including eChecks, as well as Deluxe Payment Exchange, including digital and print and mail payments, also Medical Payment Exchange and fraud and security services
Total | 13.6 | %
Data Solutions | Data-driven marketing | 13.5 | % | Data analytics and marketing services for business-to-business and business-to-consumer marketing
Other web-based solutions | 0.9 | % | Financial institution profitability reporting and business incorporation services
Total | 14.4 | %
Print | Checks | 32.4 | % | Printed business and personal checks
Forms and other business products | 10.5 | % | Business essentials, including business forms, envelopes, labels, stationery, and more
Promotional solutions | 10.4 | % | Branded promotional, print, apparel, and digital storefront solutions
Total | 53.3 | %

In recent years, we made strategic decisions to exit certain of our businesses. During 2023, we sold our North American web hosting and logo design businesses, completing our exit from the web hosting space. Also in 2023, we entered into agreements to exit our payroll and human resources services business, facilitating the transition of our U.S. and Canadian customers to other service providers. These customer conversions were substantially completed during 2024. We believe these actions enabled us to focus our resources on our growth businesses, while optimizing our operations.

OUR STRATEGY

Our enterprise strategy is clear and focused: we leverage the strong cash flows, customer relationships, and brand equity from our print business to drive sustainable, profitable growth across our broader portfolio. To achieve this, we are prioritizing three strategic pillars:

1. Accelerating profitable growth: By embracing our "Customers First" philosophy in market engagement, we are unlocking new opportunities across our broad portfolio of services. This approach enables us to deliver comprehensive solutions that adapt to evolving customer needs, while strategically focusing on growth within our payments and data businesses to drive sustainable profitability.

2. Enhancing operational efficiency: We are committed to ongoing process improvements, cost optimization, and performance enhancements to ensure our operations remain agile and competitive.

3. Disciplined capital deployment: Our capital allocation framework ensures investments are strategically aligned with our growth objectives and deliver optimal returns. Strengthening our balance sheet remains a priority, supported by robust cash flow generation and targeted debt reduction.

By focusing on these areas, we are positioned to sustain our growth momentum while maintaining a solid financial foundation.

Our transformation journey has enabled us to evolve from a traditional check printing company into a trusted partner in Payments and Data solutions. With our infrastructure modernization largely complete and non-strategic businesses divested, our attention is on growth investments that drive scale and accelerate profit growth ahead of revenue. Our disciplined pricing strategies and rigorous cost management continue to support operational excellence.

Over the past three years, we successfully executed our North Star program, a comprehensive, multi-year initiative designed to enhance shareholder value by accelerating adjusted earnings before interest, taxes, depreciation, and amortization (EBITDA) growth, increasing cash flow, reducing debt, and improving our leverage ratio. The program was structured to balance disciplined cost management with targeted investments to support sustainable growth. On the cost side, we advanced our organizational redesign, consolidated roles, streamlined management layers, and expanded spans of control. We also leveraged technology and automation to digitize and simplify our operations, while global talent helped us scale back-office functions. On the growth side, we focused on building an integrated software channel in Merchant Services, expanding our Data Solutions business into more industry verticals, and strengthening our marketing and sales capabilities.

Our disciplined execution of the North Star strategy is reflected in our financial performance. Revenue for 2025 increased over 2024, despite the impact of strategic business exits. We reduced selling, general and administrative expense by $35.9 million in 2025 as compared to the prior year, and we lowered total debt by $73.7 million from the previous year-end. These results highlight our ongoing commitment to improving financial performance and delivering value to our shareholders through strategic initiatives and disciplined operational management.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-13_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-13_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-13_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-05_2-02-results.md, 10-K_2026-02-13_item7_mdna.md, 10-K_2026-02-13_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
