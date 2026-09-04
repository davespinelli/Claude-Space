# Triage pack — CURI · CuriosityStream Inc.

_Generated 2026-09-04 22:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** CURI · **Name:** CuriosityStream Inc.
- **CIK:** 0001776909
- **SIC:** 7812 — Services-Motion Picture & Video Tape Production
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/CURI

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** CuriosityStream Inc.
- **CIK:** 1,776,909 · **SIC:** 7812 (Services-Motion Picture & Video Tape Production) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 2.90 |
| mktcap | $172.1M |
| ev | $166.7M |
| ev_ebit | n/a |
| fcf | $13.0M |
| fcf_yield | 7.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -16.0% |
| net_debt | -$5.4M |
| net_debt_ebit | n/a |
| cash | $5.4M |
| ltd | $0.00 |
| equity | $41.5M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $71.7M |
| revenue_prior | $51.1M |
| rev_growth | 40.1% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$7.3M |
| net_income | -$6.4M |
| cfo | $13.1M |
| capex | $102k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 2.4% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 59,338,028 |
| shares_py | 57,929,733 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -36.7% |
| r6m | -9.5% |
| off_52w_high | -42.6% |
| adv20 | $8.0M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.61 |
| r_ev_ebit | 0.00 |
| r_roic | 0.07 |
| r_rev_growth | 0.92 |
| r_buyback | 0.29 |
| score | 0.38 |

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
| rank | 340 |

**Screen rationale:** revenue +40.1%; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **59,338,028** (CY2026Q2I) vs **57,929,733** prior year (CY2025Q2I)
- Change: **2.4%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-26** — Item 5.02 (officer / director change or comp arrangement): On August 26, 2026 , CuriosityStream, Inc. (the "Company") announced that Brady Hayden will step down from his position as Chief Financial Officer of the Company, effective September 1, 2026.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 200,000 sh / $538,820 vs sells 61,959 sh / $163,040 -> net $375,779 (BUYING).
Distinct insiders buying (code P): 1. Largest buy: Stinchcomb Clinton Larry bought 94,256 sh @ $2.74 ($258,638) on 2026-05-27.

Form 4 filings parsed: 12; transaction rows: 23 (open-market buys 5, sales 2).

| code | rows |
|---|---|
| A | 2 |
| F | 4 |
| G | 2 |
| M | 8 |
| P | 5 |
| S | 2 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-12_2-02-results.md)

_Extraction: started at the first release heading, 'Second Quarter 2026 Financial Results'; skipped 10 forward-looking-statement block(s); 15 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (pressrelease2q26qcuri-2026.htm)

Second Quarter 2026 Financial Results

• Rev enue of $23.2 million , compared to $19.0 million in the second quarter of 2025;

• Gross profit of $16.9 million or 72.8% gross margin, compared to $10.1 million or 53.4% gross margin in the second quarter of 2025;

• Record net income of $8.9 million compared to a net income o f $0.8 million i n the second quarter of 2025.

• Record adjusted EBITDA of $11.4 million , an increase of $8.3 million, compared to Adjusted EBITDA of $3.0 million in the second quarter of 2025, and the sixth sequential quarter of positive EBITDA;

• Reduced operating expenses by $4.5 million, or 24.1%, compared to the second quarter of 2025;

• Net cash used in operating activities of $3.0 million for the six months ended June 30, 2026 , compared to net cash provided by operating activities of $4.7 million for the six months ended June 30, 2025;

• Paid an ordinary dividend of $5.0 million and repurchased nearly $0.6 million in common shares; and

• Cash, restricted cash and held-to-maturity securities balance of $10.9 million and no debt as of June 30, 2026.

Second Quarter 2026 Business Highlights

• Licensed thousands of hours of traditional premium video to over 25 public broadcasters, streamers, paytv and digital first distributors;

• Premiered Independence Dawn, new season of Butterfly Effect and over 160 films and series to SVOD and Paytv subscribers;

• Licensed millions of tokens of code for AI training, reinforcement learning and evaluation;

• Private code corpus of more than 880 billion tokens now available for virtually all aspects of AI training;

• Licensed thousands of hours of synchronized multi-camera action sequences to a leading video research lab to train models on advanced video editing workflows;

• Licensed 40,000 segment High Dynamic Range (HDR) dataset;

• Seventh straight quarter of expanded data and video licensing partnerships for AI training, having now built a differentiated content library of rights to over three million hours of video and audio across multiple genres;

• New subscription launches in Mexico and US with Apple, Sling, Dish and other partners; and

• Continued enhancements in payments, billing and processing. May 2026 was the Company's best month in history for retention of involuntary churn.

Financial Outlook

Cu riosityStream expects the following for the second half and full year of 2026:

• Second-half 2026 revenue in the range of $38 - $41 million, and full-year 2026 revenue in the range of $77 - $82 million.

• Second-half 2026 Adjusted EBITDA 1 in the range of $6 - $10 million, and full-year 2026 Adjusted EBITDA 1 in the range of $18 - $22 million.

• December 31, 2026, cash and investments 2 balance in the range of $17 - 22 million.

1 See Non-GAAP Financial Measures below.

2 Cash and investments consist of financial instruments, including cash and cash equivalents, restricted cash, investments in debt and other securities, and investments in equity method investees.

Conference Call Information

CuriosityStream will host a Q&A conference call today to discuss the Company's second quarter 2026 results at 5:00 p.m. Eastern Time (2:00 p.m. Pacific Time). A live audio webcast of the call will be available on the CuriosityStream Investor Relations website at https://investors.curiositystream.com. Participants may also dial-in toll free at (877) 407-9716 or International at (201) 493-6779 and reference conference ID# 13758750. An audio replay of the conference call will be available for two weeks following the call on the CuriosityStream Investor Relations website at https://investors.curiositystream.com.

CuriosityStream Inc. (Nasdaq:CURI) is the entertainment brand for people who want to know more. The global media company is home to award-winning original and curated factual films, shows, and series covering science, nature, history, technology, society, and lifestyle. CuriosityStream is also a leading provider of AI model training datasets, leveraging one of the world's largest and most valuable rights-cleared media corpora. The company's portfolio spans millions of hours of premium video and audio, 850 billion tokens of production-grade code rich with developer context, and dozens of bespoke datasets created with proprietary content intelligence tools. CuriosityStream's data licensing partnerships enable leading technology companies to train and fine-tune generative, agentic, and physical AI systems that will power the next era of infrastructure and enterprise capabilities.

CuriosityStream also reaches millions of subscribers worldwide, operating the flagship Curiosity Stream SVOD service; Curiosity Channel, the linear television channel available via global distribution partners; Curiosity University, featuring talks from the best professors at the world's most renowned universities as well as courses, short and long-form videos, and podcasts; Curiosity Now, Curiosity History, Curiosity Animals, Curiosity Explora, and other free, ad-supported channels; Curiosity Audio Network, with original content and podcasts; and Curiosity Studios, which oversees original programming. For more information, visit CuriosityStream.com.

Contacts:

CuriosityStream Investor Relations

Brett Maas

IR@CuriosityStream.com

CuriosityStream Inc.

Condensed Consolidated Balance Sheets

(unaudited and in thousands) | June 30, 2026 | December 31, 2025
Assets
Current assets
Cash and cash equivalents | 5,379 | 18,318
Restricted cash | 60 | 60
Short-term investments in debt and other securities | 1,496 | 8,966
Accounts receivable, net | 6,402 | 8,893
Other current assets | 2,994 | 1,198
Total current assets | 16,331 | 37,435
Investments in debt securities | 3,920 | —
Investments in equity method investees | 3,733 | 3,668
Property and equipment, net | 341 | 404
Content assets, net | 32,502 | 31,000
Licensing fee receivable, net of current portion | 5,967 | —
Operating lease right-of-use assets | 2,605 | 2,763
Other assets | 2,066 | 461
Total assets | 67,465 | 75,731
Liabilities and stockholders' equity
Current liabilities
Content liabilities | 61 | 362
Accounts payable | 4,316 | 9,449
Accrued expenses and other liabilities | 8,218 | 12,094
Deferred revenue | 8,226 | 8,409
Total current liabilities | 20,821 | 30,314
Non-current operating lease liabilities | 3,234 | 3,460
Other liabilities | 1,948 | 470
Total liabilities | 26,003 | 34,244
Commitments and contingencies (Note 13)
Stockholders' equity
Common stock, $0.0001 par value – 125,000 shares authorized as of June 30, 2026, and December 31, 2025; 59,594 shares issued as of June 30, 2026 and 58,950 issued as of December 31, 2025, including 489 and 216 treasury shares; 59,105 and 58,734 shares outstanding as of June 30, 2026. and December 31, 2025, respectively. | 5 | 5
Treasury stock | (1,122) | (251)
Additional paid-in capital | 381,034 | 377,577
Accumulated deficit | (338,455) | (335,844)
Total stockholders' equity | 41,462 | 41,487
Total liabilities and stockholders' equity | 67,465 | 75,731

CuriosityStream Inc.

Condensed Consolidated Statements of Operations

Three Months Ended June 30, | Six Months Ended June 30,
(unaudited and in thousands except per share amounts) | 2026 | 2025 | 2026 | 2025
Revenues | 23,245 | 19,012 | 38,406 | 34,102
Operating expenses
Cost of revenues | 6,313 | 8,864 | 12,970 | 15,944
Advertising and marketing | 1,900 | 3,275 | 5,415 | 6,209
General and administrative | 5,852 | 6,393 | 12,385 | 11,390
14,065 | 18,532 | 30,770 | 33,543
Operating income | 9,180 | 480 | 7,636 | 559
Change in fair value of warrant liability | — | (79) | — | (86)
Interest and other income | 101 | 424 | 311 | 850
Equity method investment income (loss) | 35 | (156) | 65 | (307)
Income before income taxes | 9,316 | 669 | 8,012 | 1,016
Provision for (benefit from) income taxes | 434 | (115) | 458 | (87)
Net income | 8,882 | 784 | 7,554 | 1,103
Net income per share
Basic | 0.15 | 0.01 | 0.13 | 0.02
Diluted | 0.15 | 0.01 | 0.12 | 0.02
Weighted average number of common shares outstanding
Basic | 59,190 | 57,585 | 59,070 | 57,357
Diluted | 60,607 | 58,745 | 60,534 | 58,489

CuriosityStream Inc.

Condensed Consolidated Statements of Cash Flows

Six Months Ended June 30,
(unaudited and in thousands) | 2026 | 2025
Cash flows from operating activities
Net income | 7,554 | 1,103
Adjustments to reconcile net income to net cash (used in) provided by operating activities
Change in fair value of warrant liability | — | 86
Additions to content assets | (9,543) | (4,179)
Change in content liabilities | (301) | 120
Amortization of content assets | 8,041 | 7,113
Depreciation and amortization expenses | 88 | 83
Bad debt expenses | 48 | (61)
Loss on disposal of assets | 170 | —
Amortization of premiums and accretion of discounts associated with investments in debt securities, net | (34) | (354)
Stock-based compensation | 4,101 | 3,077
Equity method investment (income) loss | (65) | 307
Other non-cash items | 102 | 145
Changes in operating assets and liabilities
Accounts receivable | (3,811) | (5,190)
Other assets | (1,174) | 335
Accounts payable | (5,134) | (521)
Accrued expenses and other liabilities | (2,861) | 4,023
Deferred revenue | (131) | (1,376)
Net cash (used in) provided by operating activities | (2,950) | 4,711
Cash flows from investing activities
Purchases of property and equipment | — | (77)
Business acquisitions | (1,954) | —
Sales of investments in debt securities | 1,000 | 2,000
Maturities of investments in debt securities | 6,500 | 17,450
Purchases of investments in debt securities | (3,915) | (11,070)
Net cash provided by investing activities | 1,631 | 8,303
Cash flows from financing activities
Repurchases of common stock | (871) | —
Dividends paid | (9,889) | (12,665)
Payments related to tax withholding | (730) | (1,297)
Payment of debt issuance costs | (130) | —
Net cash used in financing activities | (11,620) | (13,962)
Net decrease in cash, cash equivalents and restricted cash | (12,939) | (948)
Cash, cash equivalents and restricted cash, beginning of period | 18,378 | 7,951
Cash, cash equivalents and restricted cash, end of period | 5,439 | 7,003
Supplemental non-cash operating activities:
Disposition of assets in exchange for a non-cash receivable in connection with the Curiosity Brands, LLC transaction | 250 | —
Supplemental disclosure:
Income tax refunds received, net of payments | 12 | 84
Cash paid for operating leases | (290) | (235)

CuriosityStream Inc.

Reconciliation from Net Income to Adjusted EBITDA

Three Months Ended June 30, | Six Months Ended June 30,
(unaudited and in thousands) | 2026 | 2025 | 2026 | 2025
Net Income | 8,882 | 784 | 7,554 | 1,103
Change in fair value of warrant liability | — | 79 | — | 86
Interest and other income | (101) | (424) | (311) | (850)
Provision for (benefit from) income taxes | 434 | (115) | 458 | (87)
Equity method investment income (loss) | (35) | 156 | (65) | 307
Depreciation and amortization 1 | 47 | 42 | 88 | 83
Restructuring 2 | — | 13 | — | 36
Other nonrecurring 3 | 281 | 273 | 452 | 366
Stock-based compensation | 1,860 | 2,214 | 4,101 | 3,077
Adjusted EBITDA | 11,368 | 3,022 | 12,277 | 4,121
1 Amounts do not include amortization of content assets.
2 Consists primarily of severance and other costs associated with ongoing workforce optimization.
3 Consists of nonrecurring license, risk mitigation expenses, and loss on asset disposal associated with the Curiosity Brands transaction.

CuriosityStream Inc.

Reconciliation from Net Cash Flow provided by Operating Activities to Adjusted Free Cash Flow

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-12_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

OVERVIEW

Founded by John Hendricks, former Chairman of Discovery Communications and founder of the Discovery Channel, CuriosityStream is a media and entertainment company that offers premium video and audio programming across the principal categories of factual entertainment, including science, history, society, nature, lifestyle and technology. Our mission is to provide premium factual entertainment that informs, enchants and inspires.

We seek to meet demand for high-quality factual entertainment via subscription video on-demand ("SVOD") platforms, content licensing, bundled content licenses for SVOD and linear offerings, talks and courses and partner bulk sales.

The main sources of our revenue are:

1. Subscription and license fees earned from our Direct-to-Consumer business and Partner Direct subscribers ("Direct Business"),

2. License fees from content licensing arrangements ("Content Licensing"),

3. Bundled license fees from distribution affiliates ("Bundled Distribution"), and

4. Other revenue, including advertising and sponsorships ("Other").

We operate our business as a single operating segment that provides premium content through multiple channels, including the use of various applications, partnerships and affiliate relationships.

CuriosityStream's award-winning content library features approximately 6,000 programs that explore topics ranging from space engineering to ancient history to the rise of Wall Street, and includes shows and series from leading nonfiction producers. Each week we launch new video titles, which are available on demand in high- or ultra-high definition. Through new and long-standing international partnerships, substantial portions of our video library have been localized from English into eleven different languages. The Company also aggregates rights to millions of video and audio programs, course materials and other assets to utilize on our own services as well as license to other media and technology companies.

RESULTS OF OPERATIONS

The following table represents a summary of our Consolidated Statements of Operations for the years ended December 31, 2025, and 2024 , and the discussion that follows compares the financial results for year ended December 31, 2025, to the year ended December 31, 2024 :

Year Ended December 31, | $ Change | % Change
(in thousands) | 2025 | 2024
Revenues
Direct Business | 33,613 | 47 | % | 38,592 | 75 | % | (4,979) | (13 | %)
Content Licensing | 33,233 | 46 | % | 7,798 | 15 | % | 25,435 | 326 | %
Bundled Distribution | 3,379 | 5 | % | 3,937 | 8 | % | (558) | (14 | %)
Other | 1,433 | 2 | % | 807 | 2 | % | 626 | 78 | %
Total revenues | 71,658 | 100 | % | 51,134 | 100 | % | 20,524 | 40 | %
Operating expenses
Cost of revenues | 31,113 | 39 | % | 25,363 | 39 | % | 5,750 | 23 | %
Advertising and marketing | 14,028 | 18 | % | 14,434 | 23 | % | (406) | (3 | %)
General and administrative | 33,821 | 43 | % | 24,670 | 38 | % | 9,151 | 37 | %
Total operating expenses | 78,962 | 100 | % | 64,467 | 100 | % | 14,495 | 22 | %
Operating loss | (7,304) | (13,333) | 6,029 | (45 | %)
Other income (expense)
Change in fair value of warrant liability | 88 | (44) | 132 | *n/m
Interest and other income | 983 | 3,074 | (2,091) | (68 | %)
Equity method investment loss | (180) | (2,506) | 2,326 | (93 | %)
Loss before income taxes | (6,413) | (12,809) | 6,396 | (50 | %)
(Benefit from) provision for income taxes | 14 | 132 | (118) | *n/m
Net loss | (6,427) | (12,941) | 6,514 | (50 | %)
* Percentage not meaningful

Operating loss for the years ended December 31, 2025, and 2024, was $7.3 million and $13.3 million, respectively. The reduction in operating loss of $6.0 million, or 45%, was primarily driven by an increase of $20.5 million, or 40% in total revenue. This revenue growth was partially offset by an increase of $14.5 million, or 22% in our operating expenses, which was primarily attributable to higher revenue share and an increase in stock-based compensation charges during the period.

Net loss for the years ended December 31, 2025, and 2024, was $6.4 million and $12.9 million, respectively, representing a decrease of $6.5 million, or 50% in net loss. This improvement was primarily driven by a $6.0 million reduction in operating loss for 2025. Additional contributing factors included a decrease in losses from equity method investments, partially offset by lower interest income. The change in the fair value of warrant liabilities had a minimal offsetting effect on the overall results.

Our future operating results and cash flows are dependent upon a number of opportunities, challenges, and other factors, including our ability to efficiently grow our subscriber base, increase our prices and expand our service offerings to maximize subscriber lifetime value.

Revenue

Since the Company was founded in 2015, we have generated a significant portion of our revenues from consumers directly accessing our content in the form of monthly or annual subscription plans. More recently, we have expanded our revenue streams through strategic content licensing arrangements. As a result of this expansion, Content Licensing has become a core component of our diversified revenue model, now contributing nearly as much to our total revenue as our Direct Business.

For the years ended December 31, 2025, and 2024, revenues totaled $71.7 million and $51.1 million, respectively, representing an increase of $20.5 million, or 40%. This growth was primarily driven by an increase of $25.4 million in Content Licensing revenue, which was partially offset by a $5.0 million, or approximately 13%, decrease in our Direct Business revenue and a $0.6 million , or 14% , decrease in Bundled Distribution revenue. Other revenue contributed an additional $0.6 million in the growth over the prior year.

We engage in non-monetary trade and barter transactions with media counterparties as a strategic means of expanding our content library while preserving liquidity. These arrangements, which are common within the media industry, involve the exchange of content assets or advertising services. In accordance with our revenue recognition policy, revenue recorded from such transactions represents the fair value of the content assets or services received from the counterparties at the time the performance obligation is satisfied. And such revenue recorded from such transactions represents the fair value of content received from the counter parties. Content-for-content exchanges are classified within Content Licensing revenue, while exchanges involving promotional services or media campaigns are recognized as Other revenue.

For more information, see Note 5 - Revenue in the Notes to Consolidated Financial Statements .

Direct Business

The Company's streaming content is provided to consumers through two primary distribution channels: (i) direct-to-consumer ("DTC") and (ii) third-party platforms, referred to as Partner Direct. The DTC offering includes access through the Company's website and applications developed for electronic devices. Collectively, DTC and Partner Direct comprise the Company's Direct Business.

DTC offering includes subscriptions to consumers as well as bulk subscriptions through enterprises, and provides monthly or annual subscription terms. Pricing varies based on the subscriber's location, the selected subscription tier and term. To ensure wide accessibility, the Company has developed applications for major customer devices, including streaming media players such as Roku, Apple TV, and Amazon Fire TV, and smart TVs from brands including LG, Vizio, Sony, and Samsung.

Following the global implementation of price adjustments for legacy subscribers—a process initiated in March 2023, we continue to evaluate our pricing structures to align with market conditions. Alongside our standard subscription, we offer the "Smart Bundle" service, which includes access to Tastemade, Kidstream, SommTV, and Curiosity University. Future adjustments to these subscription plans may be considered to further enhance revenue from our legacy subscribers.

The multichannel video programming distributors ("MVPDs"), virtual MVPDs ("vMVPDs") and digital distributor partners making up Partner Direct pay us a license fee for subscribers to CuriosityStream via the partners' respective platforms. We have affiliate relationships with, and our service is available directly from, major MVPDs that include Comcast, Cox, and Dish, and vMVPDs and digital distributors that include Amazon Prime Video Channels, Apple Channel, The Roku Channel, Sling TV and YouTube TV.

The following table details our Direct Business for the years ended December 31, 2025, and 2024:

Year Ended December 31, | $ Change | % Change
(in thousands) | 2025 | 2024
Direct-to-Consumer | 23,763 | 71% | 31,332 | 81% | (7,569) | (24 | %)
Partner Direct | 9,850 | 29 | % | 7,260 | 19 | % | 2,590 | 36 | %
Total Direct Business | 33,613 | 100 | % | 38,592 | 100 | % | (4,979) | (13 | %)

For the year ended December 31, 2025, our Direct-to-Consumer revenue decreased by $7.6 million, or 24%, compared to 2024, due to a decrease in DTC subscriber base. This decrease was partially offset by a $2.6 million, or 36%, increase in Partner Direct revenue, which was driven by continued subscriber growth as well as the price increase that only fully deployed to all partners since 2024.

Content Licensing

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-12_item1_business.md)

ITEM 1. BUSINESS

Unless the context otherwise requires, all references in this section to "we," "us," "our," the "Company," or "CuriosityStream" refer to CuriosityStream Inc. and its subsidiaries prior to and following the consummation of the Business Combination.

CORPORATE HISTORY AND BACKGROUND

On October 14, 2020, Software Acquisition Group Inc., a special purpose acquisition company and a Delaware corporation ("SAQN"), and CuriosityStream Operating Inc., a Delaware corporation ("Legacy CuriosityStream"), consummated a reverse merger pursuant to the Agreement and Plan of Merger, dated August 10, 2020 (the "Business Combination"). Upon the consummation of the Business Combination, Legacy CuriosityStream became a wholly owned subsidiary of SAQN and the registrant changed its name from "Software Acquisition Group Inc." to "CuriosityStream Inc." Following the consummation of the Business Combination, Legacy CuriosityStream changed its name from "CuriosityStream Operating Inc." to "Curiosity Inc."

SAQN, a blank check company, was incorporated as a Delaware corporation on May 9, 2019, for the purpose of effecting a merger, capital stock exchange, asset acquisition, stock purchase, reorganization or similar business combination with one or more businesses.

CuriosityStream LLC, Legacy CuriosityStream's predecessor, was formed in the State of Delaware in June 2008. CuriosityStream LLC officially launched its subscription service to U.S. based customers in March 2015 and to international customers in September 2015.

BUSINESS OVERVIEW

Founded by John Hendricks, former Chairman of Discovery Communications and founder of the Discovery Channel, CuriosityStream is a media and entertainment company that offers premium video and audio programming across the principal categories of factual entertainment, including science, history, society, nature, lifestyle and technology. Our mission is to provide premium factual entertainment that informs, enchants and inspires.

We seek to meet the demand for high-quality factual entertainment via subscription video on-demand ("SVOD")

platforms, content licensing, bundled content licenses for SVOD and linear offerings, talks and courses and partner bulk sales.

The main sources of our revenue are:

1. Subscription and license fees earned from our Direct-to-Consumer business and Partner Direct subscribers ("Direct Business"),

2. License fees from content licensing arrangements ("Content Licensing"),

3. Bundled license fees from distribution affiliates ("Bundled Distribution"), and

4. Other revenue, including advertising and sponsorships ("Other").

We operate our business as a single operating segment that provides premium content through multiple channels, including the use of various applications, partnerships and affiliate relationships.

CuriosityStream's award-winning content library features approximately 14,000 programs that explore topics ranging from space engineering to ancient history to the rise of Wall Street, and includes shows and series from leading nonfiction producers. Each week we launch new video titles, which are available on demand in high- or ultra-high definition. Through new and long-standing international partnerships, substantial portions of our video library have been localized from English into eleven different languages. The Company also aggregates rights to millions of video and audio programs, course materials and other assets to utilize on our own services as well as license to other media and technology companies.

Our programs are produced, co-produced or commissioned by us, or licensed through one of our content partnerships, such as with NHK in Japan, ZED in France and Terra Mater in Austria. Our programs are hosted by and feature scientists, experts and celebrities, such as Stephen Hawking, Sir David Attenborough, Sigourney Weaver, Patrick Aryee and James Burke. Our programs have received four Emmy nominations, including an Emmy Award win for Stephen Hawking's Favorite Places . Every video title on our SVOD platform is available on-demand and, other than historical footage or classic documentaries, in high definition or 4K quality.

Through our acquisition of One Day University in 2021, we acquired more than 500 lectures from some of the most popular and acclaimed college and university professors in the U.S. on topics ranging from American history to Broadway shows. In addition, through our acquisition of Learn25, we acquired approximately 5,000 episodes of audio content and about 1,250 video episodes, packaged as courses on factual topics ranging from religion to biographies to psychology. These acquisitions enabled us to expand our offering of factual content into audio and educational courses, as well as package our products in special bundles for consumers and business customers. In January 2024, we rebranded our service that offers these audio and video courses and talks "Curiosity University."

In 2021, the Company invested in Watch Nebula LLC ("Nebula"), an SVOD streaming service controlled by Standard Broadcast LLC and its affiliated content creators.

Also in 2021, the Company partnered with Spiegel TV to accelerate international expansion of CuriosityStream services, taking a one-third stake in the German venture controlled by a German media company, Spiegel TV GmbH, and a German documentary producer, Autentic GmbH. The joint venture, Spiegel TV Geschichte und Wissen GmbH & Co. KG (the "Spiegel Venture"), operates two documentary channels (including one branded as "Curiosity Channel") and a FAST channel, as well as revenue sharing with respect to a localized CuriosityStream SVOD service in German-speaking Europe.

Business Model and Services

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

**Present:** meta.json, form4_summary.md, 8-K_2026-08-12_2-02-results.md, 10-K_2026-03-12_item7_mdna.md, 10-K_2026-03-12_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
