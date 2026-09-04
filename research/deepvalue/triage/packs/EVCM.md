# Triage pack — EVCM · EverCommerce Inc.

_Generated 2026-09-04 16:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** EVCM · **Name:** EverCommerce Inc.
- **CIK:** 0001853145
- **SIC:** 7372 — Services-Prepackaged Software
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/EVCM

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** EverCommerce Inc.
- **CIK:** 1,853,145 · **SIC:** 7372 (Services-Prepackaged Software) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 7.93 |
| mktcap | $1.4B |
| ev | $1.8B |
| ev_ebit | 30.1x |
| fcf | $109.2M |
| fcf_yield | 7.8% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 4.3% |
| net_debt | $381.9M |
| net_debt_ebit | 6.4x |
| cash | $133.5M |
| ltd | $515.4M |
| equity | $715.3M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $588.9M |
| revenue_prior | $562.2M |
| rev_growth | 4.8% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $59.2M |
| net_income | $17.6M |
| cfo | $111.5M |
| capex | $2.2M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -2.5% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 176,665,246 |
| shares_py | 181,278,754 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 4.0% |
| r6m | -34.6% |
| off_52w_high | -40.8% |
| adv20 | $1.4M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.63 |
| r_ev_ebit | 0.27 |
| r_roic | 0.46 |
| r_rev_growth | 0.52 |
| r_buyback | 0.81 |
| score | 0.59 |

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
| rank | 157 |

**Screen rationale:** buying back stock -2.5%; 12-1 momentum 4.0%


## 3. Share count trend

- Shares outstanding: **176,665,246** (CY2026Q2I) vs **181,278,754** prior year (CY2025Q2I)
- Change: **-2.5%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-05** — Item 5.02 (officer / director change or comp arrangement): On August 5, 2026, the Board of Directors (the "Board") of the Company appointed Alex Goor as the Company's Chief Executive Officer, effective August 6, 2026 (the "Effective Date").

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 405,872 sh / $3,844,979 -> net $-3,844,979 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 31 (open-market buys 0, sales 26).

| code | rows |
|---|---|
| F | 5 |
| S | 26 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-05_2-02-results.md)

_Extraction: started at the first release heading, 'Second Quarter 2026 Financial Highlights'; skipped 8 forward-looking-statement block(s); 6 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (evcmq226earningsrelease.htm)

Second Quarter 2026 Financial Highlights

• Revenue from continuing operations of $152.0 million, an increase of 2.7% compared to $148.0 million for the quarter ended June 30, 2025. Pro Forma Revenue increased 2.0% to $152.0 million, compared to $149.0 million for the quarter ended June 30, 2025.

• Subscription and transaction fees revenue from continuing operations of $147.4 million, an increase of 3.2% compared to $142.8 million for the quarter ended June 30, 2025. Pro Forma subscription and transaction fees revenue increased 2.4% to $147.4 million, compared to $143.9 million for the quarter ended June 30, 2025.

• Net income from continuing operations was $9.7 million, or $0.05 per basic and diluted share, for the quarter ended June 30, 2026, compared to $5.8 million, or $0.03 per basic and diluted share, for the quarter ended June 30, 2025.

• Adjusted EBITDA from continuing operations was $44.5 million for the quarter ended June 30, 2026, compared to $45.0 million for the quarter ended June 30, 2025.

"Evercommerce's second quarter results were in-line with the midpoint of guidance range for revenue and exceeded the top end of guidance range for Adjusted EBITDA." said Eric Remer, Evercommerce's Founder and CEO. "I'm proud of what our team accomplished during the quarter and, more importantly, of the Company we've built together, While our outlook for the balance of 2026 has moderated and we now expect results toward the lower end of our guidance ranges, I remain confident in the strength of our platform, our customer relationships and our long-term strategy. As the Company begins its next chapter with Alex as CEO, he will focus on accelerating long-term growth and continuing to create value for our customers, employees and shareholders."

A reconciliation of GAAP to Non-GAAP measures has been provided in the financial statement tables included at the end of this press release. An explanation of these measures is also included below under the heading "Non-GAAP Financial Measures and Key Performance Metrics."

Share Repurchases

The Company repurchased and retired 1.4 million shares of common stock for approximately $14.8 million during the three months ended June 30, 2026. As of June 30, 2026, $19.2 million remained available under the Repurchase Program.

Repurchases under the program may be made from time to time in the open market at prevailing market prices or in privately negotiated transactions. Open market repurchases will be structured to occur within the pricing and volume requirements of Rule 10b-18. The Company may also, from time to time, enter into Rule 10b5-1 plans to facilitate repurchases of its shares under this authorization. This program does not obligate the Company to acquire any particular amount of common stock and the program may be extended, modified, suspended or discontinued at any time at the Company's discretion. The Company expects to fund repurchases with cash on hand.

Business Outlook

Based on information as of today, August 5, 2026, the Company is issuing the following financial guidance for the third quarter 2026 and full year 2026.

Third Quarter 2026:

• Revenue is expected to be in the range of $151.5 million to $154.5 million.

• Adjusted EBITDA is expected to be in the range of $44 million to $46 million.

Full Year 2026:

• Revenue is expected to be in the range of $612 million to $632 million.

• Adjusted EBITDA is expected to be in the range of $183 million to $191 million.

Based on our current outlook, we now expect full-year results to trend toward the lower end of our guidance ranges.

A reconciliation of Adjusted EBITDA to net income, the most directly comparable GAAP measure, is not available without unreasonable efforts on a forward-looking basis due to the high variability, complexity and low visibility with respect to certain charges excluded from this non-GAAP measure; in particular, the measures and effects of stock-based compensation expense specific to equity compensation awards that are directly impacted by unpredictable fluctuations in our stock price. It is important to note that these charges could be material to EverCommerce's results computed in accordance with GAAP.

Conference Call Information

EverCommerce's management team will hold a conference call to discuss our second quarter 2026 results and outlook today, August 5, 2026, at 5:00 p.m. ET. Please visit the "Investor Relations" page of the Company's website (https://investors.evercommerce.com) for both telephonic and webcast access to this call as well as a copy of the presentation materials used on the call. An archive replay will be available following the conclusion of the call.

Investor Contact

Ryan Siurek

Chief Financial Officer

720-407-2888

IR@evercommerce.com

Media Contact

Jeanne Trogan

VP of Communications

737-465-2897

Press@evercommerce.com

About EverCommerce

EverCommerce (Nasdaq: EVCM) is an AI platform for the service economy, enabling more than 745,000 SMB customers worldwide with software that helps them schedule and manage work, communicate with customers and patients, bill and get paid, and build lasting customer relationships. With its EverPro, EverHealth, and EverWell brands specializing in the Home, Health, and Wellness service industries, EverCommerce delivers AI-driven workflows that matter most so service professionals can spend more time delivering great outcomes and less time on administrative work. Learn more at EverCommerce.com .

Gross profit is calculated as total revenues less cost of revenues (exclusive of depreciation and amortization), amortization of developed technology, amortization of capitalized software and depreciation expense (allocated to cost of revenues). We calculate Adjusted Gross Profit as gross profit adjusted to exclude depreciation and amortization allocated to cost of revenues. Adjusted Gross Profit should be viewed as a measure of operating performance that is a supplement to, and not a substitute for, operating income or loss, net earnings or loss and other GAAP measures of income (loss) or profitability.

Adjusted EBITDA and Adjusted EBITDA margin. Adjusted EBITDA and Adjusted EBITDA margin are key performance measures that our management uses to assess our financial performance and are also used for internal planning and forecasting purposes. We believe that these non-GAAP financial measures are useful to investors and other interested parties in analyzing our financial performance because they provide a comparable overview of our operations across historical periods. In addition, we believe that providing Adjusted EBITDA, together with a reconciliation of net income (loss) to Adjusted EBITDA, helps investors make comparisons between our company and other companies that may have different capital structures, different tax rates, and/or different forms of employee compensation.

Adjusted EBITDA and Adjusted EBITDA margin are used by our management team as additional measures of our performance for purposes of business decision-making, including managing expenditures, and evaluating potential acquisitions. Period-to-period comparisons of Adjusted EBITDA and Adjusted EBITDA margin help our management identify additional trends in our financial results that may not be shown solely by period-to-period comparisons of net income (loss) or income (loss) from continuing operations. In addition, we may use Adjusted EBITDA in the incentive compensation programs applicable to some of our employees. Our Management recognizes that Adjusted EBITDA has inherent limitations because of the excluded items, and may not be directly comparable to similarly titled metrics used by other companies.

We calculate Adjusted EBITDA as net income (loss) adjusted to exclude interest and other expense, net, income tax expense (benefit), depreciation and amortization, other amortization, stock-based compensation, and transaction-related and other non-recurring or unusual costs. Other amortization includes amortization for capitalized contract acquisition costs. Transaction-related costs are specific deal-related costs such as legal fees, financial and tax due diligence, consulting and escrow fees. Other non-recurring or unusual costs are expenses such as impairment charges, (gains) losses from divestitures, system implementation costs including amortization of cloud-based software implementation costs, executive separation costs, severance expense related to planned restructuring activities, and costs associated with integration and transformational improvements. Transaction-related and other non-recurring or unusual costs are excluded as they are not representative of our underlying operating performance. Adjusted EBITDA should be viewed as a measure of operating performance that is a supplement to, and not a substitute for, operating income or loss, net earnings or loss and other GAAP measures of income (loss).

EverCommerce Inc.

Condensed Consolidated Balance Sheets

(in thousands, except per share and share amounts)

(unaudited)

June 30, | December 31,
2026 | 2025
Assets
Current assets:
Cash and cash equivalents | 133,496 | 129,730
Accounts receivable, net of allowance for expected credit losses of $3.7 million and $3.6 million at June 30, 2026 and December 31, 2025, respectively | 37,681 | 37,046
Contract assets | 12,334 | 11,612
Prepaid expenses and other current assets | 34,948 | 34,391
Total current assets | 218,459 | 212,779
Property and equipment, net | 6,033 | 5,744
Capitalized software, net | 66,925 | 58,968
Other non-current assets | 38,544 | 36,261
Intangible assets, net | 141,950 | 164,240
Goodwill | 892,531 | 893,802
Total assets | 1,364,442 | 1,371,794
Liabilities and Stockholders' Equity
Current liabilities:
Accounts payable | 10,737 | 5,125
Accrued expenses and other | 50,532 | 55,836
Deferred revenue | 22,101 | 21,670
Customer deposits | 13,051 | 12,519
Current maturities of long-term debt | 5,500 | 5,500
Total current liabilities | 101,921 | 100,650
Long-term debt, net of current maturities and deferred financing costs | 515,442 | 517,891
Other non-current liabilities | 31,801 | 36,380
Total liabilities | 649,164 | 654,921
Stockholders' equity:
Preferred stock, $0.00001 par value, 50,000,000 shares authorized and no shares issued or outstanding as of June 30, 2026 and December 31, 2025 | — | —
Common stock, $0.00001 par value, 2,000,000,000 shares authorized and 176,601,707 and 178,111,971 shares issued and outstanding at June 30, 2026 and December 31, 2025, respectively | 2 | 2
Accumulated other comprehensive loss | (14,288) | (12,686)
Additional paid-in capital | 1,356,142 | 1,373,022
Accumulated deficit | (626,578) | (643,465)
Total stockholders' equity | 715,278 | 716,873
Total liabilities and stockholders' equity | 1,364,442 | 1,371,794

EverCommerce Inc.

Condensed Consolidated Statements of Operations and Comprehensive Income

(in thousands, except per share and share amounts)

(unaudited)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-12_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

EverCommerce is a leading provider of integrated, vertically-tailored software-as-a-service ("SaaS") solutions for service-based small- and medium-sized businesses ("service SMBs"). Our platform spans across the full lifecycle of interactions between consumers and service professionals with vertical-specific applications. As of December 31, 2025, we served more than 745,000 customers across three core verticals: EverPro for Home Services; EverHealth for Health Services; and EverWell for Wellness Services. Within our core verticals, our customers operate within numerous micro-verticals, ranging from home service professionals, such as home improvement contractors and home maintenance technicians, to physician practices and therapists within Health Services, to salon owners within Wellness. Our platform provides vertically-tailored SaaS solutions that address service SMBs' increasingly specialized demands, as well as highly complementary solutions that provide fully-integrated offerings, allowing service SMBs and EverCommerce to succeed in the market, and provide end consumers more convenient service experiences.

We offer several vertically-tailored suites of solutions, each of which follows a similar and repeatable go-to-market playbook: offer a "system of action" Business Management Software that streamlines daily business workflows, integrate highly complementary, value-add adjacent solutions and complete gaps in the value chain to create integrated solutions. These solutions focus on addressing how service SMBs market their services, streamline operations and retain and engage their customers.

• Business Management Software: Our vertically-tailored Business Management Software is the system of action at the center of a service business's operation, and is typically the point-of-entry and first solution adopted by a customer. Our software, designed to meet the day-to-day workflow needs of businesses in specific vertical end markets, streamlines front and back-office processes and provides polished customer-facing experiences. Using these offerings, service SMBs can deliver their services, streamline operations and focus on growing their customer base.

• Billing & Payment Solutions: Our Billing & Payment Solutions provide integrated payments, billing and invoicing automation and business intelligence and analytics. Our omni-channel payments capabilities include point-of-sale, eCommerce, online bill payments, recurring billing, electronic invoicing and mobile payments. Supported payment types include credit card, debit card and Automated Clearing House ("ACH") processing. Our payments platform also provides a full suite of service commerce features, including customer management as well as cash flow reporting and analytics. These value-add features help small- and medium-sized businesses ("SMBs") to ensure more timely billing and payments collection and provide improved cash flow visibility.

• Customer Experience Solutions: Our Customer Experience Solutions modernize how businesses engage and interact with customers by leveraging innovative, bespoke customer listening and communication solutions to improve the customer experience and increase retention. Our software provides customer listening capabilities with real-time customer surveying and analysis to allow standalone businesses and multi-location brands to receive VoC insights and manage the customer experience lifecycle. These applications include: customer health scoring, customer support systems, real-time alerts, NPS-based customer feedback collection, review generation and automation, reputation management, customer satisfaction surveying and a digital communication suite, among others. Additionally, the recent acquisition of ZyraTalk (as defined below) provides virtual assistant capabilities with an agentic automation platform. ZyraTalk offers production-ready fully autonomous AI agents and field service management systems designed for seamless integration across our Home Services solutions and improving the overall prospect and customer experience. Collectively, these tools help our customers gain actionable insights, increase customer loyalty and repeat purchases and improve customer experiences.

We go to market with suites of solutions that are aligned to our three core verticals. Within each suite, our Business Management Software – the system of action at the center of a service business' operation – is typically the first solution adopted by a customer. This vertically-tailored point-of-entry provides us with an opportunity to cross-sell adjacent products, previously offered as fragmented and disjointed point solutions by other software providers. This "land and expand" strategy allows us to acquire customers with key foundational solutions and expand into offerings via product development and acquisitions that cover all workflows and power the full scope of our customers' businesses. This results in a self-reinforcing flywheel effect, enabling us to drive value for our customers and, in turn, fuel growth, improve customer stickiness, and increase our market share.

II-3

Our continuing operations generate two types of revenue: (i) Subscription and Transaction Fees, which are primarily recurring revenue streams, and (ii) Other revenue, which consists primarily of one-time revenue streams. Our recurring revenue generally consists of monthly, quarterly and annual software and maintenance subscriptions and transaction revenue associated with integrated payments and billing solutions.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The following tables summarize key components of our results of operations for the years ended December 31, 2025, 2024 and 2023. The period-to-period comparison of our historical results are not necessarily indicative of our results of operations that may be expected in the future. The following comparative information for results of operations for all periods presented have been adjusted to reflect discontinued operations related to marketing technology solutions and includes the operating results of Fitness Solutions for all periods through the applicable date of sale.

Comparison of the years ended December 31, 2025, 2024 and 2023

Year Ended December 31,
2025 | 2024 | 2023
(in thousands)
Revenues:
Subscription and transaction fees | 566,915 | 542,977 | 515,119
Other | 21,992 | 19,208 | 19,752
Total revenues | 588,907 | 562,185 | 534,871
Operating expenses:
Cost of revenues (1) (exclusive of depreciation and amortization presented separately below) | 132,063 | 124,787 | 127,405
Sales and marketing (1) | 119,503 | 114,098 | 113,692
Product development (1) | 79,018 | 76,179 | 72,144
General and administrative (1) | 131,760 | 128,599 | 123,353
Depreciation and amortization | 67,228 | 80,650 | 94,872
Loss on sale and impairments | 85 | 11,670 | 6,325
Total operating expenses | 529,657 | 535,983 | 537,791
Operating income | 59,250 | 26,202 | (2,920)
Interest and other income (expense), net | (38,091) | (35,560) | (46,408)
Net income (loss) from continuing operations before income tax expense | 21,159 | (9,358) | (49,328)
Income tax expense | (2,955) | (5,839) | (1,377)
Net income (loss) from continuing operations | 18,204 | (15,197) | (50,705)

(1) Includes stock-based compensation expense as follows:

Year Ended December 31,
2025 | 2024 | 2023
(in thousands)
Cost of revenues | 345 | 387 | 367
Sales and marketing | 1,656 | 1,163 | 1,634
Product development | 2,480 | 1,939 | 2,194
General and administrative | 23,448 | 22,241 | 20,796
Total stock-based compensation expense | 27,929 | 25,730 | 24,991

II-11

Comparison of the years ended December 31, 2025, 2024 and 2023 (percentage of revenue)

The following table provides the key components of operating costs within our results of operations as a percentage of revenue for the year ended December 31, 2025 compared to the same periods in 2024 and 2023.

Year Ended December 31, | 2025 vs. 2024 | 2024 vs. 2023
2025 | 2024 | 2023 | % Change | % Change
Total Revenues | 100.0% | 100.0% | 100.0% | —% | —%
Operating expenses:
Cost of revenues (exclusive of depreciation and amortization presented separately below) | 22.4 | % | 22.2 | % | 23.8 | % | 0.2 | % | (1.6) | %
Sales and marketing | 20.3 | % | 20.3 | % | 21.3 | % | — | % | (1.0) | %
Product development | 13.4 | % | 13.5 | % | 13.5 | % | (0.1) | % | — | %
General and administrative | 22.4 | % | 22.9 | % | 23.1 | % | (0.5) | % | (0.2) | %
Depreciation and amortization | 11.4 | % | 14.3 | % | 17.7 | % | (2.9) | % | (3.4) | %
Loss on sale and impairments | — | % | 2.1 | % | 1.2 | % | (2.1) | % | 0.9 | %
Total operating expenses | 89.9 | % | 95.3 | % | 100.6 | % | (5.4) | % | (5.3) | %

While revenue growth remains a key focus, we remain committed to continued expansion of gross margin, net income and Adjusted EBITDA through ongoing transformation initiatives.

2025 compared to 2024

As a percentage of revenue, cost of revenues increased from 22.2% for the year ended December 31, 2024 to 22.4% for the year ended December 31, 2025, an increase of approximately 20 basis points. Additionally, the combination of cost of revenue, sales and marketing, product development and general and administrative costs declined from 78.9% for the year ended December 31, 2024 to 78.5% for the year ended December 31, 2025, an improvement of approximately 40 basis points.

2024 compared to 2023

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-12_item1_business.md)

Item 1. Business

Overview

EverCommerce is simplifying and empowering the lives of business owners whose services support us every day. We provide tailored, integrated Software-as-a-Service ("SaaS") solutions that support the highly diverse workflows and customer interactions that professionals in home services, health services, and wellness services need to automate manual processes, generate new business, and create more loyal customers.

EverCommerce is a leading provider of integrated, vertically-tailored SaaS solutions for service-based small- and medium-sized businesses ("service SMBs"). Our platform spans across the full lifecycle of interactions between consumers and service professionals with vertical-specific applications. As of December 31, 2025, we served more than 745,000 customers across three core verticals: EverPro for Home Services; EverHealth for Health Services; and EverWell for Wellness Services. Within our core verticals, our customers operate within numerous micro-verticals, ranging from home service professionals, such as home improvement contractors and home maintenance technicians, to physician practices and therapists within Health Services, and salon owners within Wellness. Our platform provides vertically-tailored SaaS solutions that address service SMBs' increasingly specialized demands, as well as highly complementary solutions that provide fully-integrated offerings, allowing service SMBs and EverCommerce to succeed in the market, and provide end consumers more convenient service experiences. For the year ended December 31, 2025, we estimate that approximately 93% of our customers contributed less than $2 thousand in revenue and approximately 3% contributed more than $5 thousand in revenue.

On October 31, 2025, we completed the sale of our marketing technology solutions business to Ignite Visibility as part of our previously announced strategic review (see " Note 3. Acquisition and Dispositions" in the Notes to the Consolidated Financial Statements for additional details). Marketing technology solutions qualified as discontinued operations and is presented accordingly in the consolidated financial statements for all periods presented through the applicable date of the sale.

On September 15, 2025, we acquired 100% of the interest of Joblyt LLC, dba ZyraTalk ("ZyraTalk"), an AI-powered customer engagement solution that combines virtual assistant capabilities with an agentic automation platform (see " Note 3. Acquisition and Dispositions" in the Notes to the Consolidated Financial Statements for additional details). The acquisition helps to establish EverCommerce as an AI-driven innovator, beginning with near-term application in its Home Services vertical, EverPro, and we plan to extend ZyraTalk into broader opportunities across our other verticals.

On March 13, 2024, the Company entered into definitive sale and purchase agreements to sell our fitness solutions to Jonas Fitness Portfolio Holdco Inc. ("Jonas Software") (see " Note 3. Acquisition and Dispositions" in the Notes to the Consolidated Financial Statements for additional details). The sale of American Service Finance LLC., ASF Payment Solutions ULC and Technique Fitness Inc. (collectively, "North American Fitness"), closed simultaneous with signing. The sale of EverCommerce UK, including wholly-owned subsidiaries Fitii UK (MyPTHub and MyPTHub LLC) and ClubWise UK and its wholly-owned subsidiary ClubWise Australia (collectively, "UK Fitness" and together with North American Fitness, "Fitness Solutions"), closed on July 1, 2024.

Small- and medium-sized businesses ("SMBs") are an important engine for economic growth. Collectively, in 2025 SMBs represented the single largest employer and employee category in the U.S. economy, accounting for 99.9% of businesses in the United States, 46% of the U.S. private workforce and over 44% of U.S. GDP. The services sector is the backbone of the U.S. economy, representing approximately 78% of U.S. GDP and 79% of U.S. employment. Service businesses are the largest segment of the SMB market, employing approximately 60 million people in the U.S. alone.

Today, service SMBs are accelerating their adoption of digital technologies to increase growth, drive efficiencies and enhance customer engagement. At the same time, their technology needs are becoming increasingly specialized as they adapt their businesses to better compete and align with evolving consumer preferences. However, service SMBs typically lack available resources to invest in and support expensive enterprise technology solutions and often rely on little-to-no technology. When technology is used, it is often a fragmented set of point solutions with insufficient integrated capabilities to support the complete service lifecycle.

Since inception, we have taken a differentiated approach from other software providers. We recognize that all service SMBs require solutions that enable them to perform three key functions: (i) acquire new customers and generate new business opportunities; (ii) manage and scale business operations; and (iii) improve and expand on customer relationships. However, services SMBs require functionality specific to their vertical market because the workflows vary by vertical. For example, the business management requirements of home services contractors are different than the business management requirements of small physician practices. As a result, we have built a comprehensive platform designed specifically to meet the unique integrated workflow needs of service SMBs. Our integrated solutions include Business Management Software (such as route-based dispatching and medical practice management), Billing & Payment Solutions (such as e-invoicing, mobile payments and integrated payment processing), and Customer Experience

I-1

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

**Present:** meta.json, form4_summary.md, 8-K_2026-08-05_2-02-results.md, 10-K_2026-03-12_item7_mdna.md, 10-K_2026-03-12_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
