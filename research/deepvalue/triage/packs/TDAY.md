# Triage pack — TDAY · USA TODAY Co., Inc.

_Generated 2026-09-04 23:11 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** TDAY · **Name:** USA TODAY Co., Inc.
- **CIK:** 0001579684
- **SIC:** 2711 — Newspapers: Publishing or  Publishing & Printing
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/TDAY

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** USA TODAY Co., Inc.
- **CIK:** 1,579,684 · **SIC:** 2711 (Newspapers: Publishing or  Publishing & Printing) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

> **EARNINGS QUALITY FLAG — one-off items likely.**
> net income more than 3x operating income.
> Reported net income is not supported by the operating engine that is supposed to produce it (typical causes: gains on sale, legal settlements, deferred-tax valuation-allowance releases, bargain-purchase gains). Reconcile net income to operating income in the earnings release (section 7) before treating any earnings-based metric here as repeatable.

**Valuation**

| metric | value |
|---|---|
| price | 6.47 |
| mktcap | $949.9M |
| ev | $1.7B |
| ev_ebit | n/a |
| fcf | $62.9M |
| fcf_yield | 6.6% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -3.6% |
| net_debt | $792.7M |
| net_debt_ebit | n/a |
| cash | $86.7M |
| ltd | $879.4M |
| equity | $153.7M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $2.3B |
| revenue_prior | $2.5B |
| rev_growth | -8.3% |
| rev_growth_note | n/a |
| eq_flag | net income more than 3x operating income |
| ebit | -$42.8M |
| net_income | $1.7M |
| cfo | $114.4M |
| capex | $51.5M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 0.1% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 146,817,941 |
| shares_py | 146,617,081 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 107.2% |
| r6m | 0.8% |
| off_52w_high | -28.3% |
| adv20 | $19.5M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.57 |
| r_ev_ebit | 0.00 |
| r_roic | 0.21 |
| r_rev_growth | 0.13 |
| r_buyback | 0.64 |
| score | 0.36 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2024 |
| equity_period | CY2026Q2I |
| shares_period | CY2026Q2I |
| shares_py_period | CY2025Q2I |
| capex_missing | False |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 359 |

**Screen rationale:** 12-1 momentum 107.2%; EARNINGS QUALITY: net income more than 3x operating income — one-off items likely


## 3. Share count trend

- Shares outstanding: **146,817,941** (CY2026Q2I) vs **146,617,081** prior year (CY2025Q2I)
- Change: **0.1%** — roughly flat
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-02 among the 4 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 13,471 sh / $78,805 -> net $-78,805 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 27 (open-market buys 0, sales 1).

| code | rows |
|---|---|
| A | 8 |
| F | 6 |
| M | 12 |
| S | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'NEW YORK, NY — August 6, 2026 — USA TODAY Co., Inc. ("USA TODAY Co.", '; skipped 7 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (tdayq22026ex991earningsrel.htm)

NEW YORK, NY — August 6, 2026 — USA TODAY Co., Inc. ("USA TODAY Co.", "we", "us", "our", or the "Company") (NYSE: TDAY) today reported its financial results for the second quarter ended June 30, 2026.

"The second quarter reflected continued progress against our long-term strategy and reinforced our confidence in reaffirming our full-year outlook. We reduced operating expenses by approximately 8% year-over-year, generated approximately $20 million of free cash flow, an increase of approximately 11% year-over-year, and delivered positive net income for the second consecutive quarter," said Michael Reed, Chairman and Chief Executive Officer.

"Our Digital-only subscription and Digital other businesses continued to build momentum and remain important drivers of our long-term growth. Digital-only subscription revenues grew year-over-year for the second consecutive quarter, while digital-only ARPU reached another record high. Digital other revenues also grew year-over-year, and we expect this revenue stream to continue expanding throughout the year as we broaden our portfolio of content licensing partners and further grow our commerce opportunities."

"Consumer discovery continues to evolve beyond traditional search, and we have been preparing for that shift by expanding our reach across social, video and newsletters while strengthening our first-party audience capabilities. Combined with investments in technologies like Palantir, these initiatives are helping us better understand and monetize our audience while building a more diversified and resilient business."

"While quarterly results may fluctuate as we execute our strategy, our long-term business plan remains intact and supports our confidence in reaffirming our full-year outlook. Across the business we continue to see meaningful progress, and we believe are getting close to crossing that revenue inflection point. We believe we are building a strong operating foundation on a large and engaged audience, from which data and signals will drive greatly improved monetization as we leverage that intelligence."

"We are confident in the steps we are taking to position the Company for sustainable long-term revenue growth combined with free cash flow growth and margin expansion, leading to long-term value creation for shareholders."

Second Quarter 2026 Financial Highlights:

• Total revenues of $536.3 million decreased 8.3% year-over-year and decreased 6.1% on a same-store basis (1)

• Total digital revenues of $254.3 million, or 47.4% of total revenues

• Net income attributable to USA TODAY Co. of $9.1 million, reflecting the second consecutive quarter of positive net income

• Total Adjusted EBITDA (1) of $56.9 million

• Cash provided by operating activities of $35.4 million

• Free cash flow (1) of $19.6 million

Second Quarter 2026 Digital Highlights:

• 158 million average monthly unique visitors (2)

• Digital advertising revenues of $79.8 million

• Digital-only subscription revenues of $45.6 million, representing the second consecutive quarter of year-over-year growth

• LocaliQ segment core platform revenues (3) of $106.3 million

(1) Total Adjusted EBITDA, Segment Adjusted EBITDA, Total Adjusted EBITDA margin, Adjusted net income (loss) attributable to USA TODAY Co., Free cash flow, and Same store revenues are non-GAAP measures. See "Use of Non-GAAP Information" below for information about these non-GAAP measures.

(2) 158 million average monthly unique visitors in the second quarter of 2026 with approximately 107 million average monthly unique visitors coming from our U.S. media network, which includes USA TODAY (as measured by © 2026 Comscore, Media Metrix (June 2026), Desktop + Mobile) and approximately 51 million average monthly unique visitors resulting from our U.K. digital properties (based on Adobe Analytics).

(3) See "Key Performance Indicators" ("KPI") below for information about our use of KPIs.

◦ Key metrics improved sequentially including core platform revenues (3) , Segment Adjusted EBITDA (1) , core platform average revenue per user (3) and core platform average customer count (3)

Second Quarter 2026 Capital Structure Highlights:

• Cash and cash equivalents of $86.7 million as of June 30, 2026

• Total debt principal outstanding at June 30, 2026 was $970.5 million, including $722.7 million in first lien debt

• First lien net leverage (4) was 2.3x, a decrease of 14% year-over-year

Business Outlook: (5)

The Company reiterates its full year 2026 outlook.

• Full Year 2026 Business Outlook (5)

◦ Total revenues are expected to be flat to down in the low single digits on a same store basis (1)

▪ Total digital revenues are expected to grow versus the prior year on a same store basis (1) and are expected to make up 50%+ of total revenues during 2026

◦ Net income attributable to USA TODAY Co. is expected to grow versus the prior year

◦ Total Adjusted EBITDA (1) is expected to grow versus the prior year

◦ Cash provided by operating activities is expected to grow double-digits versus the prior year

◦ Free cash flow (1) is expected to grow double-digits versus the prior year

Financial Highlights: 6
In thousands | Second Quarter 2026
Total revenues | 536,337
Net income attributable to USA TODAY Co. | 9,125
Total Adjusted EBITDA (6) | 56,886
Adjusted net income attributable to USA TODAY Co. (6) | 11,026
Cash provided by operating activities | 35,351
Free cash flow (6) | 19,569

(4) As of June 30, 2026, the First Lien Net Leverage ratio was calculated by subtracting cash on the balance sheet from the sum of our five-year first lien term loan facility (the "2029 Term Loan Facility") and dividing that by Q2 2026 LTM Total Adjusted EBITDA. The 6% Senior Secured Convertible Notes due 2027 and 6% Senior Secured Convertible Notes due 2031 are secured by liens junior to those securing our 2029 Term Loan Facility.

(5) Projections are based on Company estimates as of August 6, 2026 and are provided solely for illustrative purposes. Actual results may vary. The Company undertakes no obligation to update this information. Additionally, the Company's estimates do not factor in the impact of any possible future acquisitions or dispositions. The Company's future financial results could differ materially from the Company's current estimates.

(6) Refer to "Use of Non-GAAP Information" below for the Company's definition of Total Adjusted EBITDA, Adjusted net income (loss) attributable to USA TODAY Co., and Free cash flow, as well as the reconciliation of such measures to the most comparable GAAP measure.

Earnings Conference Call

Management will host a conference call on Thursday, August 6, 2026 at 8:30 A.M. Eastern Time to review the financial and operating results for the period. A copy of the earnings release will be posted to the Investor Relations section of USA TODAY Co.'s website, investors.usatodayco.com. The conference call may be accessed by dialing 1-888-506-0062 (from within the U.S.) or 1-973-528-0011 (from outside of the U.S.) ten minutes prior to the scheduled start of the call; please reference "USA TODAY Co. Second Quarter Earnings Call" or access code "581209". We use our website as a channel of distribution for important Company information and we use the investors.usatodayco.com website as a means of disclosing material non-public information and for complying with our disclosure obligations under Regulation FD. A simultaneous webcast of the conference call will be available to the public on a listen-only basis at investors.usatodayco.com. Please allow extra time prior to the call to visit the website and download any necessary software required to listen to the internet broadcast. A telephonic replay of the conference call will also be available approximately two hours following the call's completion through 11:59 P.M. Eastern Time on Thursday, August 20, 2026 by dialing 1-877-481-4010 (from within the U.S.) or 1-919-882-2331 (from outside of the U.S.); please reference access code "53737". A transcript of our earnings call held today also will be posted to the investors.usatodayco.com website.

About USA TODAY Co.

USA TODAY Co., Inc. (NYSE: TDAY) is a diversified media company with expansive reach at the national and local level dedicated to empowering and enriching communities. Our mission is to inspire, inform, and connect audiences. As a media and digital marketing solutions company we are focused on sustainable growth. Through our trusted brands, including the USA TODAY NETWORK, comprised of the national publication, USA TODAY, and our network of local properties, in the United States, and Newsquest, a wholly-owned subsidiary operating in the United Kingdom, we provide essential journalism, local content, and digital experiences to audiences and businesses. We deliver trusted unbiased journalism when and where consumers want it. LocaliQ, our digital marketing solutions brand, supports small and medium-sized businesses with innovative digital marketing products and solutions.

Table No. 1
In thousands, except number of shares and par value | June 30, 2026 | December 31, 2025
Assets | (Unaudited)
Current assets:
Cash and cash equivalents | 86,657 | 90,213
Accounts receivable, net of allowance for credit losses of $11,743 and $13,600 as of June 30, 2026 and December 31, 2025, respectively | 221,570 | 223,551
Inventory | 12,695 | 12,888
Prepaid expenses | 52,903 | 45,959
Other current assets | 29,268 | 16,566
Total current assets | 403,093 | 389,177
Property, plant and equipment, net of accumulated depreciation of $375,066 and $368,358 as of June 30, 2026 and December 31, 2025, respectively | 164,523 | 178,461
Operating lease assets | 110,698 | 122,513
Goodwill | 518,453 | 518,762
Intangible assets, net | 307,395 | 337,845
Deferred tax assets | 70,552 | 77,858
Pension and other assets | 216,097 | 212,542
Total assets | 1,790,811 | 1,837,158
Liabilities and equity
Current liabilities:
Accounts payable and accrued liabilities | 288,020 | 308,152
Deferred revenue | 104,519 | 105,398
Current portion of long-term debt | 70,741 | 69,315
Operating lease liabilities | 29,942 | 33,435
Other current liabilities | 4,118 | 1,483
Total current liabilities | 497,340 | 517,783
Long-term debt | 639,410 | 645,811
Convertible debt | 240,043 | 239,112
Deferred tax liabilities | 11,454 | 8,142
Pension and other postretirement benefit obligations | 33,139 | 34,170
Long-term operating lease liabilities | 131,870 | 146,421
Other long-term liabilities | 84,293 | 91,107
Total noncurrent liabilities | 1,140,209 | 1,164,763
Total liabilities | 1,637,549 | 1,682,546
Commitments and contingent liabilities
Equity
Preferred stock, $0.01 par value per share, 300,000 shares authorized, none of which were issued and outstanding at June 30, 2026 and December 31, 2025 | — | —
Common stock, $0.01 par value per share, 2,000,000,000 shares authorized; 160,032,237 shares issued and 146,817,941 shares outstanding at June 30, 2026; 159,912,152 shares issued and 147,124,756 shares outstanding at December 31, 2025 | 1,600 | 1,599
Treasury stock, at cost, 13,214,296 shares and 12,787,396 shares at June 30, 2026 and December 31, 2025, respectively | (26,351) | (23,607)
Additional paid-in capital | 1,263,881 | 1,287,821
Accumulated deficit | (1,022,781) | (1,051,797)
Accumulated other comprehensive loss | (62,604) | (58,905)
Total USA TODAY Co. stockholders' equity | 153,745 | 155,111
Noncontrolling interests | (483) | (499)
Total equity | 153,262 | 154,612
Total liabilities and equity | 1,790,811 | 1,837,158

USA TODAY CO., INC.

CONDENSED CONSOLIDATED STATEMENTS OF OPERATIONS

(Unaudited)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-26_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

OVERVIEW

We are a diversified media company with expansive reach at the national and local level dedicated to empowering and

enriching communities. Our mission is to inspire, inform, and connect audiences. As a media and digital marketing solutions

company we are focused on sustainable growth. Through our trusted brands, including the USA TODAY NETWORK,

comprised of the national publication, USA TODAY, and our network of local properties , in the United States (the "U.S."), and

Newsquest, a wholly-owned subsidiary operating in the United Kingdom (the " U.K. "), we provide essential journalism, local

content, and digital experiences to audiences and businesses. We deliver trusted unbiased journalism when and where

consumers want it. LocaliQ, our digital marketing solutions brand, supports small and medium-sized businesses ("SMBs") with

innovative digital marketing products and solutions.

In November 2025, we changed our corporate name from Gannett Co., Inc. to USA TODAY Co., Inc. and we revised the

names of two of our reportable segments: Domestic Gannett Media is now referred to as USA TODAY Media and Digital

Marketing Solutions is now referred to as LocaliQ . We do not distinguish between our prior and current corporate and

reportable segment names and refer to our current corporate and reportable segment names throughout this Annual Report on

Form 10-K. As such, unless expressly indicated or the context requires otherwise, the terms " USA TODAY Co. , " "Company,"

"we," "us," and "our" in this document refer to USA TODAY Co., Inc. , a Delaware corporation, and, where appropriate, its

subsidiaries.

We report in three segments: USA TODAY Media , Newsquest and LocaliQ . We also have a Corporate category that

includes activities not directly attributable to a specific reportable segment and includes expenses associated with broad

corporate functions. A full description of our reportable segments is included in Note 15 — Segment reporting in the notes to

the Consolidated financial statements .

Strategy and executive summary

We are focused on becoming a sustainable, growth‑driven media and digital marketing solutions company. Our strategy is

rooted in three operating pillars: (i) expanding our reach and engagement, (ii) diversifying our digital revenues, and (iii)

strengthening our capital structure, all supported by an increasingly integrated operating foundation, including modernized

technology systems, automated workflows, enhanced data capabilities, and continued investment in our people and talent

development. Our strategy unifies trusted journalism and digital innovation under one brand: USA TODAY Co. and is

represented by our motto, "National voice . Local strength ." Our consolidated results for the year ended December 31, 2025 ,

reflect the execution of our operating priorities, including the changes in our mix of revenues, cost structure, and capital

allocation.

Expand reach and engagement with our customer segments

We aim to grow and strengthen our large national and local audiences across our USA TODAY Media , Newsquest , and

LocaliQ segments by delivering relevant content and expanded offerings, and as of December 31, 2025 , we have built one of

the largest digital audiences in the U.S. media sector, both locally and nationally.

Diversify digital revenues

We seek to accelerate digital revenue growth by developing a broad portfolio of monetization channels on our platforms,

maximizing yield, and tailoring opportunities to individual consumer behavior. We aim to accomplish this by offering a wide

range of solutions across advertising, subscriptions, and commerce, while increasingly leveraging our existing content to power

syndication, affiliate, content and AI partnerships, as well as licensing arrangements. As a result of these efforts, as of

December 31, 2025 , total Digital revenues as a percentage of total revenues increased by two percentage points to 46%

compared to 44% at December 31, 2024 .

Strengthen our capital structure

We remain focused on reducing debt, generating consistent cash flow, and creating flexibility to reinvest in growth

initiatives with the goal to support long‑term financial resilience and innovation. During the year ended December 31, 2025 , we

repaid $ 135.5 million of long-term debt and as of December 31, 2025 had cash provided by operating activities of $114.4

million .

Industry trends

We have considered several industry trends when assessing our strategy:

• Print advertising and Print circulation revenues have and are expected to continue to decline as our audience

increasingly moves to digital platforms. We seek to optimize our print operations to efficiently manage for the

declining print audience. We are focused on growing a digitally-oriented audience across multiple platforms and

revenue streams.

• Shortages of newsprint have resulted in price volatility and in 2026, we expect to see price increases.

• Our revenues and results of operations continue to be influenced by general macroeconomic conditions, including, but

not limited to, trade policy, inflation, interest rates, housing demand, employment levels, and consumer confidence.

We believe that these factors are contributing to uncertainty, which is resulting in lower levels of advertising

performance and reduced spending.

• We rely on third-party platforms from large technology companies, particularly search engines, social media

platforms, and emerging technologies. These platforms exert significant control over the visibility and ranking of our

content, and their actions can adversely impact traffic, engagement, and revenues. Additionally, these companies can

influence both the type of media we acquire and the associated costs. We continue to adapt by diversifying our digital

strategies and optimizing content distribution to mitigate these impacts.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

RESULTS OF OPERATIONS

Consolidated summary

A summary of our consolidated results is presented below. Refer to Segment results below for a discussion of results by

segment.

Year ended December 31,
In thousands, except per share amounts | 2025 | 2024 | $ Change | % Change | 2023 | $ Change | % Change
Digital (a) | $ 1,056,070 | $ 1,103,651 | $ (47,581) | (4) % | $ 1,050,370 | $ 53,281 | 5 %
Print and commercial (b) | 1,246,156 | 1,405,664 | (159,508) | (11) % | 1,613,180 | (207,516) | (13) %
Total revenues | 2,302,226 | 2,509,315 | (207,089) | (8) % | 2,663,550 | (154,235) | (6) %
Operating costs | 1,410,788 | 1,545,584 | (134,796) | (9) % | 1,692,031 | (146,447) | (9) %
Selling, general and administrative expenses | 639,748 | 703,645 | (63,897) | (9) % | 722,885 | (19,240) | (3) %
Depreciation and amortization | 165,759 | 156,287 | 9,472 | 6 % | 162,622 | (6,335) | (4) %
Integration and reorganization costs | 31,595 | 66,155 | (34,560) | (52) % | 24,468 | 41,687 | ***
Asset impairments | 2,243 | 46,589 | (44,346) | (95) % | 1,370 | 45,219 | ***
(Gain) loss on sale or disposal of assets, net | (16,844) | 1,106 | (17,950) | *** | (40,101) | 41,207 | ***
Interest expense | 97,225 | 104,697 | (7,472) | (7) % | 111,776 | (7,079) | (6) %
Loss (gain) early extinguishment of debt | 1,516 | (55,559) | 57,075 | *** | (4,529) | (51,030) | ***
Equity income in unconsolidated investees, net | (2,209) | (548) | (1,661) | *** | (2,379) | 1,831 | (77) %
Other (income) expense, net (c) | (26,320) | 19,032 | (45,352) | *** | 1,572 | 17,460 | ***
Loss before income taxes | $ (1,275) | $ (77,673) | $ 76,398 | (98) % | $ (6,165) | $ (71,508) | ***
(Benefit) provision for income taxes | (3,030) | (51,286) | 48,256 | (94) % | 21,729 | (73,015) | ***
Net income (loss) | 1,755 | (26,387) | 28,142 | *** | (27,894) | 1,507 | (5) %
Net income (loss) attributable to noncontrolling interests | 6 | (33) | 39 | *** | (103) | 70 | (68) %
Net income (loss) attributable to USA TODAY Co. | $ 1,749 | $ (26,354) | $ 28,103 | *** | $ (27,791) | $ 1,437 | (5) %
Income (loss) per share attributable to USA TODAY Co. - basic | $ 0.01 | $ (0.18) | $ 0.19 | *** | $ (0.20) | $ 0.02 | (10) %
Income (loss) per share attributable to USA TODAY Co. - diluted | $ 0.01 | $ (0.18) | $ 0.19 | *** | $ (0.20) | $ 0.02 | (10) %

*** Indicates an absolute value percentage change greater than 100.

(a) Amounts are net of intersegment eliminations of $134.0 million , $151.8 million and $150.5 million for the years ended December 31, 2025 , 2024 and 2023 ,

respectively. Intersegment eliminations represent digital marketing services revenues and expenses associated with products sold by sales teams in our USA

TODAY Media and Newsquest segments but fulfilled by our LocaliQ segment. When discussing segment results, these revenues and expenses are presented

gross but are eliminated in consolidation.

(b) Included Commercial printing and delivery revenues of $121.4 million , $152.0 million and $186.1 million for the years ended December 31, 2025 , 2024 and

2023 , respectively.

(c) Other (income) expense, net primarily reflects the components of net periodic pension and postretirement benefits other than service cost, expert fees

associated with the litigation with Google, consulting fees related to a discrete initiative to reformulate our go-to-market strategy and post-sales processes,

(gains) losses from the sale of investments, third-party debt costs and the components of net periodic pension and postretirement benefits other than service

cost.

Revenues

Digital revenues are primarily derived from digital advertising offerings such as digital marketing services generated

through multiple services, including search advertising, display advertising, search optimization, social media, website

development, web presence products, customer relationship management, and software-as-a-service solutions, classified

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-26_item1_business.md)

ITEM 1. BUSINESS

Overview

USA TODAY Co. is a diversified media company with expansive reach at the national and local level dedicated to

empowering and enriching communities. Our mission is to inspire, inform, and connect audiences. As a media and digital

marketing solutions company we are focused on sustainable growth. Through our trusted brands, including the USA TODAY

NETWORK, comprised of the national publication, USA TODAY, and our network of local properties , in the United States

(the "U.S."), and Newsquest, a wholly-owned subsidiary operating in the United Kingdom (the " U.K. "), we provide essential

journalism, local content, and digital experiences to audiences and businesses. We deliver trusted unbiased journalism when and

where consumers want it. LocaliQ, our digital marketing solutions brand, supports small and medium-sized businesses

("SMBs") with innovative digital marketing products and solutions.

In November 2025, we changed our corporate name from Gannett Co., Inc. to USA TODAY Co., Inc. and we revised the

names of two of our reportable segments: Domestic Gannett Media is now referred to as USA TODAY Media and Digital

Marketing Solutions is now referred to as LocaliQ . We do not distinguish between our prior and current corporate and

reportable segment names and refer to our current corporate and reportable segment names throughout this Annual Report on

Form 10-K. As such, unless expressly indicated or the context requires otherwise, the terms " USA TODAY Co. , " "Company,"

"we," "us," and "our" in this document refer to USA TODAY Co., Inc. , a Delaware corporation, and, where appropriate, its

subsidiaries.

We report in three segments: USA TODAY Media , Newsquest and LocaliQ . We also have a Corporate category that

includes activities not directly attributable to a specific reportable segment and includes broad corporate functions, such as

legal, human resources, accounting, analytics, finance, marketing and technology, as well as other general business costs. A full

description of our reportable segments is included in Note 15 — Segment reporting in the notes to the Consolidated financial

statements .

Growing digital revenue is a core strategic priority, and we employ a digital-first strategy, focused on audience growth and

engagement and on diversifying revenue streams. As a result, in 2025 , total Digital revenues, which includes Digital advertising

revenues, Digital marketing services revenues, Digital-only subscription revenues, and Other Digital revenues, including digital

content syndication, affiliate, content and artificial intelligence ("AI") partnerships, and licensing revenues, grew to 46% of our

total revenues, or $1.1 billion . In total, during 2025 we averaged 186 million (a)(b) unique visitors across both the USA TODAY

Media and Newsquest segments, and as of December 31, 2025 , we had approximately 1.5 million paid digital-only

subscriptions, which outnumbered our print subscriptions.

We believe that a number of factors and industry trends have, and will continue to, present risks and challenges to our

business. For a detailed discussion of certain factors that could materially affect our business, results of operations and financial

condition, see "Item 1A — Risk Factors."

Strategy

We are committed to inspiring, informing and connecting audiences as a sustainable, growth-focused media and digital

marketing solutions company. Our strategy is rooted in three operating pillars: (i) expanding our reach and engagement, (ii)

diversifying our digital revenues, and (iii) strengthening our capital structure, all supported by an increasingly integrated

operating foundation, including modernized technology systems, automated workflows, enhanced data capabilities, and

continued investment in our people and talent develop ment. Our strategy unifies trusted journalism and digital innovation under

one brand: USA TODAY Co. and is represented by our motto, "National voice . Local strength ."

Three operating pillars

Expand reach and engagement with our customer segments

We believe a scaled and engaged base is key to our ongoing growth - including audience in our USA TODAY Media and

Newsquest segments and clients in our LocaliQ segment.

As of December 31, 2025 , we have built one of the largest digital audiences in the U.S. media sector, both locally and

nationally. For both the USA TODAY Media and Newsquest segments, we seek to strengthen the connection with our audience

by providing relevant content and expanded offerings that resonate with our readers. We believe a scaled, engaged audience is

the catalyst for creating diversified, predictable, and repeatable digital revenues.

In our LocaliQ segment, we seek to expand our client base through enhancements in our customer acquisition and retention

and by broadening our product portfolio. By capitalizing on our domain expertise, we aim to grow our addressable market and

provide comprehensive solutions that meet the evolving needs of our clients.

Diversify digital revenues

We seek to accelerate digital revenue growth by developing a broad portfolio of monetization channels on our platforms,

maximizing yield across our platforms, and tailoring opportunities to individual consumer behavior.

Our strategy aims to allow us to more fully monetize the numerous visitors to our digital platforms, capitalizing on every

interaction. Given our extensive portfolio, we seek to deliver and optimize a wide range of offerings across advertising,

subscriptions, and commerce while increasingly leveraging our existing content to power syndication, affiliate, content and AI

partnerships, as well as licensing arrangements.

Likewise, we are also focused on enhancing and expanding our core digital marketing services products and solutions. This

includes continuing to develop software-based solutions, including AI-powered solutions, which are intended to increase our

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-26_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-26_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-26_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-02-26_item7_mdna.md, 10-K_2026-02-26_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
