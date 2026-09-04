# Triage pack — OSPN · OneSpan Inc.

_Generated 2026-09-04 13:14 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** OSPN · **Name:** OneSpan Inc.
- **CIK:** 0001044777
- **SIC:** 7373 — Services-Computer Integrated Systems Design
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/OSPN

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** OneSpan Inc.
- **CIK:** 1,044,777 · **SIC:** 7373 (Services-Computer Integrated Systems Design) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermLineOfCredit

**Valuation**

| metric | value |
|---|---|
| price | 16.76 |
| mktcap | $617.6M |
| ev | $579.3M |
| ev_ebit | 12.0x |
| fcf | $50.5M |
| fcf_yield | 8.2% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 16.3% |
| net_debt | -$38.3M |
| net_debt_ebit | -0.8x |
| cash | $43.3M |
| ltd | $5.0M |
| equity | $273.5M |
| ltd_tag | LongTermLineOfCredit |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $243.2M |
| revenue_prior | $243.2M |
| rev_growth | 0.0% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $48.4M |
| net_income | $72.9M |
| cfo | $59.5M |
| capex | $9.0M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -3.8% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 36,852,173 |
| shares_py | 38,324,622 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 11.3% |
| r6m | 57.6% |
| off_52w_high | -0.2% |
| adv20 | $6.0M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.66 |
| r_ev_ebit | 0.69 |
| r_roic | 0.83 |
| r_rev_growth | 0.35 |
| r_buyback | 0.84 |
| score | 0.72 |

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
| rank | 46 |

**Screen rationale:** high ROIC 16.3%; buying back stock -3.8%; net cash; 12-1 momentum 11.3%


## 3. Share count trend

- Shares outstanding: **36,852,173** (CY2026Q2I) vs **38,324,622** prior year (CY2025Q2I)
- Change: **-3.8%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-06-05** — Item 5.02 (officer / director change or comp arrangement): As discussed in Item 5.07 below, on June 5, 2026, the stockholders of OneSpan Inc. (the "Company") approved an amendment (the "Amendment") to the Company's Amended and Restated 2019 Omnibus Incentive Plan (the "2019 Plan") to increase the number of shares of...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 35,000 sh / $443,978 -> net $-443,978 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 30 (open-market buys 0, sales 2).

| code | rows |
|---|---|
| A | 3 |
| F | 8 |
| M | 16 |
| P | 1 |
| S | 2 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-04_2-02-results.md)

_Extraction: started at the first release heading, 'OneSpan Reports Second Quarter 2026 Financial Results'; skipped 8 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99 - EX-99 (ospnex-991q22026.htm)

OneSpan Reports Second Quarter 2026 Financial Results

• Revenue increased 1% year-over-year to $60.5 million

• Subscription revenue increased 11% year-over-year to $46.7 million

• Operating income decreased 17% year-over-year to $8.7 million

• Adjusted EBITDA decreased 4% year-over-year to $16.9 million 1

• Annual Recurring Revenue (ARR) increased 7% year-over-year to $189.7 million 2

• Net Retention Rate (NRR) of 103% 3

BOSTON, August 4, 2026 – OneSpan Inc. (NASDAQ: OSPN) today reported financial results for the second quarter ended June 30, 2026.

"We delivered a strong second quarter highlighted by double-digit subscription revenue growth and strong profitability," stated OneSpan CEO Victor Limongelli. "Importantly, two weeks ago we introduced DigipassONE, a unified authentication platform that builds on the broadest suite of authentication functionality in the market with our new offering for verifiable credentials and digital wallets, strengthens the value of that suite with our expanded capabilities in protecting mobile applications, and ties it all together with telemetry and analytical insights to enable our customers to react to imminent threats or challenging operating conditions. In addition, the DigipassONE platform will serve as the foundation for further enhancements in the coming years, including supporting consumer agentic use cases for financial institutions and other high-trust, high-value environments."

Second Quarter 2026 Financial Highlights

• Total revenue was $60.5 million, an increase of 1% compared to $59.8 million for the same quarter of 2025. Cybersecurity revenue was $40.9 million, a decrease of 7% year-over-year. Digital Agreements revenue was $19.5 million, an increase of 25% year-over-year.

• ARR increased 7% year-over-year to $189.7 million.

• Gross profit was $44.5 million, or 74% gross margin, compared to $44.0 million, or 73% gross margin, in the same period last year.

• Operating income was $8.7 million, compared to operating income of $10.5 million in the same period last year.

• Net income was $6.8 million, or $0.18 per diluted share, compared to net income of $8.3 million, or $0.21 per diluted share, in the same period last year. Non-GAAP net income was $11.6 million, or $0.30 per diluted share, compared to non-GAAP net income of $13.3 million, or $0.34 per diluted share in the same period last year. 1

• Adjusted EBITDA was $16.9 million, compared to $17.6 million in the same period last year.

• Cash and cash equivalents were $43.3 million at June 30, 2026 compared to $70.5 million at December 31, 2025.

• OneSpan repurchased approximately 230,000 shares of its common stock for $2.9 million.

Recent Business Highlights

• OneSpan introduced DigipassONE™, a unified authentication platform that includes four components: DigipassONE Authenticate, DigipassONE Verify, DigipassONE Protect, and DigipassONE Insights.

• DigipassONE Authenticate builds on the foundation of the world's broadest suite of authentication functionality—including passkeys, FIDO2 security keys, hardware tokens, mobile authenticators, and software authenticators—to deliver secure, phishing-resistant login and transaction signing.

• DigipassONE Verify simplifies the way organizations issue, manage, and verify identities across digital wallets. Verifiable credentials are designed to improve onboarding, authentication and trust by enabling cryptographically secure and tamper-proof identity verification. An early-access release of DigipassONE Verify was released in Q2.

• DigipassONE Protect strengthens the offering with our mobile application shielding technology, which protects mobile apps against tampering, abuse, and runtime threats, promoting reliability and trustworthiness for users.

• DigipassONE Insights ties it all together with telemetry and analytical insights across authentication flows and application protection signals, so that customers can better react to imminent threats or challenging operating environments.

• OneSpan's Board of Directors has declared a quarterly cash dividend of $0.13 per share as part of the Company's recurring quarterly dividend program. The dividend is payable on September 4, 2026 to shareholders of record as of the close of business on August 14, 2026.

Financial Outlook

OneSpan is updating its previously issued financial guidance to reflect increases in its revenue and Adjusted EBITDA expectations. For the Full Year 2026, the Company expects:

• Total revenue to be in the range of $248 million to $252 million, as compared to its previous guidance range of $244 million to $249 million.

• Software and services revenue to be in the range of $202 million to $204 million, as compared to its previous guidance range of $201 million to $204 million.

• Hardware revenue to be in the range of $46 million to $48 million, as compared to its previous guidance range of $43 million to $45 million.

• ARR to be in the range of $194 million to $198 million.

• Adjusted EBITDA to be in the range of $67 million to $71 million, as compared to its previous guidance range of $64 million to $68 million.

Conference Call Details

In conjunction with this announcement, OneSpan Inc. will host a conference call today, August 4, 2026, at 4:30 p.m. ET. During the conference call, Mr. Victor Limongelli, CEO, and Mr. Jorge Martell, CFO, will discuss OneSpan's results for the second quarter 2026.

For investors and analysts accessing the conference call by phone, please refer to the press release dated July 9, 2026, announcing the date of OneSpan's second quarter 2026 earnings release. It can be found on the OneSpan investor relations website at investors.onespan.com .

The conference call is also available in listen-only mode at investors.onespan.com . Shortly after the conclusion of the call, a replay of the webcast will be available on the same website for approximately one year.

1 An explanation of the use of Non-GAAP financial measures is included below under the heading "Non-GAAP Financial Measures." A reconciliation of each Non-GAAP financial measure to the most directly comparable GAAP financial measure has also been provided in the tables below. We are not providing a reconciliation of Adjusted EBITDA guidance to GAAP net income, the most directly comparable GAAP measure, because we are unable to predict certain items included in GAAP net income without unreasonable efforts.

2 ARR is calculated as the approximate annualized value of our customer recurring contracts as of the measurement date. These include subscription, term-based license, and maintenance and support contracts and exclude one-time fees. To the extent that we are negotiating a renewal with a customer within 90 days after the expiration of a recurring contract, we continue to include that revenue in ARR if we are actively in discussion with the customer for a new recurring contract or renewal and the customer has not notified us of an intention to not renew. See our Quarterly Report on Form 10-Q for the quarter ended June 30, 2026 for additional information describing how we define ARR, including how ARR differs from GAAP revenue.

3 NRR is defined as the approximate year-over-year growth in ARR from the same set of customers at the end of the prior year period.

About OneSpan

OneSpan helps organizations build secure, seamless, and trusted digital experiences through two solution portfolios: Cybersecurity and Digital Agreements. Our cybersecurity solutions protect identities, secure mobile apps, and safeguard access through advanced high-assurance authentication, threat intelligence, fraud prevention, and robust mobile app protection, defending users, devices, and applications against sophisticated attacks. Our digital agreement solutions streamline agreement workflows with secure e-signatures, identity verification, and smart digital forms, built to enable speed, compliance and exceptional customer experiences. Trusted by leading global enterprises, including more than 60% of the world's 100 largest banks, OneSpan processes over 100 million digital agreements and billions of secure authentication transactions across more than 120 countries each year.

For more information, visit our website, explore our blog, or follow us on LinkedIn or YouTube .

OneSpan Inc.

CONDENSED CONSOLIDATED BALANCE SHEETS

(In thousands, unaudited)

June 30, | December 31,
2026 | 2025
ASSETS
Current assets
Cash and cash equivalents | 43,337 | 70,499
Accounts receivable, net of allowances of $861 at June 30, 2026 and $1,227 at December 31, 2025 | 40,444 | 55,999
Inventories, net | 9,512 | 10,466
Prepaid expenses | 7,979 | 7,044
Contract assets | 15,705 | 18,269
Other current assets | 10,613 | 9,936
Total current assets | 127,590 | 172,213
Property and equipment, net | 23,896 | 22,234
Operating lease right-of-use assets | 6,639 | 7,356
Goodwill | 127,828 | 103,840
Intangible assets, net of accumulated amortization | 15,288 | 9,741
Deferred income taxes | 59,195 | 54,733
Equity investment | 11,834 | 11,834
Other assets | 14,752 | 15,751
Total assets | 387,022 | 397,702
LIABILITIES AND STOCKHOLDERS' EQUITY
Current liabilities
Accounts payable | 11,030 | 13,726
Deferred revenue | 61,272 | 71,641
Accrued wages and payroll taxes | 11,631 | 13,553
Short-term income taxes payable | 887 | 3,079
Dividend payable | 930 | 671
Other accrued expenses | 10,452 | 11,859
Deferred compensation | 15 | 42
Total current liabilities | 96,217 | 114,571
Long-term deferred revenue | 2,018 | 2,539
Long-term lease liabilities | 5,391 | 6,139
Deferred income taxes | 979 | 988
Revolving credit facility | 5,000 | —
Other long-term liabilities | 3,937 | 1,622
Total liabilities | 113,542 | 125,859
Commitments and contingencies
Stockholders' equity
Preferred stock: 500 shares authorized, none issued and outstanding at June 30, 2025 and December 31, 2025 | — | —
Common stock: $0.001 par value per share, 75,000 shares authorized; 42,252 and 42,091 shares issued; 36,783 and 37,361 shares outstanding at June 30, 2026 and December 31, 2025, respectively. | 37 | 37
Additional paid-in capital | 132,725 | 128,651
Treasury stock, at cost: 5,469 and 4,730 shares outstanding at June 30, 2026 and December 31, 2025, respectively | (68,884) | (60,521)
Retained earnings | 218,060 | 209,821
Accumulated other comprehensive loss | (8,458) | (6,145)
Total stockholders' equity | 273,480 | 271,843
Total liabilities and stockholders' equity | 387,022 | 397,702

OneSpan Inc.

CONDENSED CONSOLIDATED STATEMENTS OF CASH FLOWS

(In thousands, unaudited)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-26_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

OneSpan helps organizations build secure, seamless, and trusted digital experiences through two solution portfolios: Cybersecurity and Digital Agreements. Our cybersecurity solutions protect identities, secure mobile apps, and safeguard access through advanced high-assurance authentication, threat intelligence, fraud prevention, and mobile app protection, defending users, devices, and applications against sophisticated attacks. Our digital agreement solutions streamline agreement workflows with secure e-signatures, identity verification, and smart digital forms, built to enable speed, compliance and exceptional customer experiences. Trusted by leading global enterprises, including more than 60% of the world's 100 largest banks, OneSpan processes over a hundred million digital agreements and billions of secure authentication transactions across more than 120 countries each year.

We offer our products primarily through a subscription licensing model and provide multiple deployment options, including cloud-based and on-premises solutions. Our solutions are sold worldwide through our direct sales force, as well as through distributors, resellers, systems integrators, and original equipment manufacturers.

We report our financial results under the following two business divisions, which are our reportable operating segments: Cybersecurity and Digital Agreements.

• Cybersecurity. Cybersecurity, formerly Security Solutions, consists of our broad portfolio of software products, software development kits ("SDKs") and Digipass authenticator devices that are used to build applications designed to defend against attacks on digital transactions across online environments, devices, and applications. The software products and SDKs included in the Cybersecurity segment are delivered through on-premises and cloud-based deployment models and include standards-based authentication technologies such as Fast Identity Online ("FIDO") authentication and passkeys, multi-factor authentication, transaction signing solutions and mobile application security.

• Digital Agreements. Digital Agreements consists of solutions that enable our clients to secure and automate business processes associated with their digital agreement and customer transaction lifecycles that require consent, non-repudiation and compliance. These solutions, which are cloud-based, include OneSpan Sign e-signature, OneSpan Notary, and OneSpan Identity Verification.

Beginning in mid-2023 and through the third quarter of 2024, our focus was on adjusting our cost structure to enable both business divisions to operate profitably. These cost optimization efforts were a major factor in the overall business returning to operating profitability in the fourth quarter of 2023. The subsequent increase in profitability, combined with high levels of cash generation, enabled us to return approximately $31.6 million to shareholders in 2025 in the form of quarterly dividends and share repurchases. Beginning in the fourth quarter of 2024 and continuing through 2025, we continued to operate profitably while taking a number of important steps to generate future revenue growth:

• In December 2024, we hired a new Chief Technology Officer, Ashish Jain, to lead our research and development efforts.

• In June 2025, we acquired Nok Nok Labs, a provider of passwordless software authentication solutions, which brought S3, a leading FIDO software product, to our product portfolio. This acquisition provides OneSpan's customers with a wider range of flexible, adaptable authentication options. See Note 6, Business Acquisitions , for additional information.

• In June 2025, we entered into the Credit Agreement with MUFG and other lenders party thereto. The Credit Agreement provides for a $100.0 million revolving credit facility with a $10.0 million letter of credit sublimit and a $10.0 million swingline loan sublimit. The proceeds of borrowings under the Credit Agreement may be used for general corporate purposes. We may borrow, repay and reborrow funds under the revolving credit facility until its maturity on June 23, 2030. See Note 12, Debt , for additional information.

• In October 2025, we announced a strategic investment in, and partnership with, ThreatFabric Holding B.V., a Dutch company that provides mobile threat intelligence, malware risk detection, and behavioral analytics, to further enhance the value we offer by providing fraud detection solutions to our customers. See Note 2, Summary of Significant Accounting Policies , for additional information.

• In December 2025, we hired a new Chief Revenue Officer, Shaun Bierweiler, to lead our go-to-market efforts, and to drive growth and customer success.

• Later in December 2025, we entered into a definitive agreement to acquire Build38, a leader in next-generation mobile application protection solutions, to extend our investment in advanced mobile security technologies. See Note 6, Business Acquisitions , for additional information.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The following table sets forth information about the Company's two operating segments, for the periods indicated, and selected segment and consolidated operating results. Unallocated corporate costs include costs related to administrative functions that are performed in a centralized manner that are not attributable to a particular segment.

Year Ended December 31, 2025
(In thousands) | Cybersecurity | Digital Agreements | Corporate and Other | Total
Revenue | 177,688 | 65,492 | — | 243,180
Cost of goods sold | 45,373 | 18,453 | — | 63,826
Gross profit | 132,315 | 47,039 | — | 179,354
Gross margin | 74% | 72% | * | 74%
Sales and marketing | 29,752 | 13,885 | 3,313 | 46,950
Research and development | 21,559 | 11,711 | 886 | 34,156
Other segment items (2)(4) | 999 | 5,482 | 43,321 | 49,802
Operating income (loss) (3)(5) | 80,005 | 15,961 | (47,520) | 48,446
Interest income, net | — | — | 1,985
Other expense, net | — | — | — | (1,069)
Income before income taxes | 49,362
Benefit from income taxes | (23,542)
Net income | 72,904

Year Ended December 31, 2024
(In thousands) | Cybersecurity | Digital Agreements | Corporate and Other | Total
Revenue | 182,187 | 60,992 | — | 243,179
Cost of goods sold | 49,319 | 19,281 | 3 | 68,603
Gross profit (1) | 132,868 | 41,711 | (3) | 174,576
Gross margin | 73% | 68% | * | 72%
Sales and marketing | 24,684 | 15,658 | 4,204 | 44,546
Research and development | 16,132 | 16,117 | 174 | 32,423
Other segment items (2)(4) | 1,990 | 4,321 | 46,491 | 52,802
Operating (loss) income (3)(5) | 90,062 | 5,615 | (50,872) | 44,805
Interest income, net | 1,807
Other expense, net | (125)
Income before income taxes | 46,487
Benefit from income taxes | (10,595)
Net income | 57,082

* Percentage not meaningful

(1) Digital Agreements gross profit includes an intangible asset write-off of $0.8 million and an internal capitalized software write-off of $0.7 million for the year ended December 31, 2024 (see Note 8, Intangible Assets, net and Note 9, Property and Equipment, net ).

(2) Cybersecurity other segment items includes general and administrative expense, restructuring and other related charges, and amortization of intangibles for the years ended December 31, 2025 and 2024.

(3) Cybersecurity operating income includes $1.3 million and $0.9 million of total amortization and depreciation expense for the years ended December 31, 2025 and 2024, respectively.

Cybersecurity operating income includes $0.3 million and $2.0 million of restructuring and other related charges for the years ended December 31, 2025 and 2024, respectively.

(4) Digital Agreements other segment items includes general and administrative expense, restructuring and other related charges, and amortization of intangibles for the years ended December 31, 2025 and 2024.

(5) Digital Agreements operating income includes $7.5 million and $6.2 million of total amortization and depreciation for the years ended December 31, 2025 and 2024, respectively.

Digital Agreements operating income includes $1.0 million and $1.7 million of restructuring and other related charges for the years ended December 31, 2025 and 2024, respectively.

Revenue by products and services allocated to the segments for the years ended December 31, 2025 and 2024 is as follows:

Years Ended December 31,
2025 | 2024
(In thousands) | Cybersecurity | Digital Agreements | Cybersecurity | Digital Agreements
Subscription | 90,929 | 65,199 | 80,555 | 58,848
Maintenance and support | 34,736 | 90 | 38,342 | 1,736
Professional services and other | 2,916 | 203 | 4,439 | 408
Hardware products | 49,107 | — | 58,851 | —
Total Revenue | 177,688 | 65,492 | 182,187 | 60,992

For the year ended December 31, 2025, total revenue was flat compared to the year ended December 31, 2024. Changes in foreign exchange rates as compared to the same period in 2024 favorably impacted total revenue by approximately $3.7 million.

Additional information on our revenue by segment follows.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-26_item1_business.md)

Item 1 – Business

Overview

OneSpan helps organizations build secure, seamless, and trusted digital experiences through two solution portfolios: Cybersecurity and Digital Agreements. Our cybersecurity solutions protect identities, secure mobile apps, and safeguard access through advanced high-assurance authentication, threat intelligence, fraud prevention, and robust mobile app protection, defending users, devices, and applications against sophisticated attacks. Our digital agreement solutions streamline agreement workflows with secure e-signatures, identity verification, and smart digital forms, built to enable speed, compliance and exceptional customer experiences. Trusted by leading global enterprises, including more than 60% of the world's 100 largest banks, OneSpan processes over 100 million digital agreements and billions of secure authentication transactions across more than 120 countries each year.

We offer our products primarily through a subscription licensing model and provide multiple deployment options, including cloud-based and on-premises solutions. Our solutions are sold worldwide through our direct sales force, as well as through distributors, resellers, systems integrators, and original equipment manufacturers.

We report our financial results under the following two business divisions, which are our reportable operating segments: Cybersecurity and Digital Agreements.

• Cybersecurity. Cybersecurity, formerly Security Solutions, consists of our broad portfolio of software products, software development kits ("SDKs") and Digipass authenticator devices that are used to build applications designed to defend against attacks on digital transactions across online environments, devices, and applications. The software products and SDKs included in the Cybersecurity segment are delivered through on-premises and cloud-based deployment models and include standards-based authentication technologies such as Fast Identity Online ("FIDO") authentication and passkeys, multi-factor authentication, transaction signing solutions and mobile application security.

• Digital Agreements. Digital Agreements consists of solutions that enable our clients to secure and automate business processes associated with their digital agreement and customer transaction lifecycles that require consent, non-repudiation and compliance. These solutions, which are cloud-based, include OneSpan Sign e-signature, OneSpan Notary, and OneSpan Identity Verification.

Beginning in mid-2023 and through the third quarter of 2024, our focus was on adjusting our cost structure to enable both business divisions to operate profitably. These cost optimization efforts were a major factor in the overall business returning to operating profitability in the fourth quarter of 2023. The subsequent increase in profitability, combined with high levels of cash generation, enabled us to return approximately $31.6 million to shareholders in 2025 in the form of quarterly dividends and share repurchases. Beginning in the fourth quarter of 2024 and continuing through 2025, we continued to operate profitably while taking a number of important steps to generate future revenue growth:

• In December 2024, we hired a new Chief Technology Officer, Ashish Jain, to lead our research and development efforts.

• In June 2025, we acquired Nok Nok Labs, Inc. ("Nok Nok Labs"), a provider of passwordless software authentication solutions, which brought S3, a leading FIDO software product, to our portfolio. This acquisition provides OneSpan's customers with a wider range of flexible, adaptable authentication options. See Note 6, Business Acquisitions , for additional information.

• In June 2025, we entered into a $100.0 million credit agreement (the "Credit Agreement") with MUFG Bank, Ltd ("MUFG") and other lenders party thereto. The Credit Agreement provides for a $100.0 million revolving credit facility with a $10.0 million letter of credit sublimit and a $10.0 million swingline loan sublimit. The proceeds of borrowings under the Credit Agreement may be used for general corporate purposes. We may borrow, repay and reborrow funds under the revolving credit facility until its maturity on June 23, 2030. See Note 12, Debt , for additional information.

• In October 2025, we announced a strategic investment in, and partnership with, ThreatFabric Holding B.V., a Dutch company that provides mobile threat intelligence, malware risk detection, and behavioral analytics, to further enhance the value we offer to our customers. See Note 2, Summary of Significant Accounting Policies , for additional information.

• In December 2025, we hired a new Chief Revenue Officer, Shaun Bierweiler, to lead our go-to-market efforts, and to drive growth and customer success.

• Later in December 2025, we entered into a definitive agreement to acquire Build38 GmbH ("Build38"), a leader in next-generation mobile application protection solutions, to extend our investment in advanced mobile security technologies. See Note 6, Business Acquisitions , for additional information.

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

**Present:** meta.json, form4_summary.md, 8-K_2026-08-04_2-02-results.md, 10-K_2026-02-26_item7_mdna.md, 10-K_2026-02-26_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
