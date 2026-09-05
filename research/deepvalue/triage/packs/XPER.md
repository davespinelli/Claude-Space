# Triage pack — XPER · Xperi Inc.

_Generated 2026-09-05 02:09 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** XPER · **Name:** Xperi Inc.
- **CIK:** 0001788999
- **SIC:** 7372 — Services-Prepackaged Software
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/XPER

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Xperi Inc.
- **CIK:** 1,788,999 · **SIC:** 7372 (Services-Prepackaged Software) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 5.83 |
| mktcap | $284.3M |
| ev | $233.7M |
| ev_ebit | n/a |
| fcf | -$5.9M |
| fcf_yield | -2.1% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | -$50.6M |
| net_debt_ebit | n/a |
| cash | $90.6M |
| ltd | $40.0M |
| equity | n/a |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $448.1M |
| revenue_prior | $493.7M |
| rev_growth | -9.2% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$43.7M |
| net_income | -$56.3M |
| cfo | -$515k |
| capex | $5.4M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 5.4% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 48,771,822 |
| shares_py | 46,260,160 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 33.2% |
| r6m | -6.4% |
| off_52w_high | -32.5% |
| adv20 | $3.2M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.15 |
| r_ev_ebit | 0.00 |
| r_roic | 0.50 |
| r_rev_growth | 0.12 |
| r_buyback | 0.18 |
| score | 0.24 |

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
| rank | 448 |

**Screen rationale:** 12-1 momentum 33.2%


## 3. Share count trend

- Shares outstanding: **48,771,822** (CY2026Q2I) vs **46,260,160** prior year (CY2025Q2I)
- Change: **5.4%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-03 among the 4 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 17 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 11 |
| F | 5 |
| G | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-05_2-02-results.md)

_Extraction: started at the first release heading, 'Financial Highlights'; skipped 8 forward-looking-statement block(s); 11 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (xper-ex99_1.htm)

Financial Highlights

GAAP ($ millions, except per share data) | Q2 FY26 | Q2 FY25
Revenue | 114.5 | 105.9
GAAP operating income (loss) | 2.9 | (11.1
GAAP net loss | (1.5 | (14.8
GAAP diluted net loss per share | (0.03 | (0.32
Non-GAAP * ($ millions, except per share data) | Q2 FY26 | Q2 FY25
Revenue | 114.5 | 105.9
Non-GAAP operating income | 18.3 | 8.8
Non-GAAP net income | 13.6 | 4.8
Non-GAAP diluted earnings per share | 0.28 | 0.11
Non-GAAP adjusted EBITDA | 24.5 | 15.2
Non-GAAP adjusted EBITDA Margin | 21.4 | % | 14.4 | %

* For further information on supplemental non-GAAP metrics included in this press release, refer to the "Non-GAAP Financial Measures" description and "GAAP to Non-GAAP Reconciliations" provided in the financial statement tables.

Recent Key Operating Achievements

Media Platform

Growth in footprint, product enhancements, and expanded advertising partnerships continue to accelerate advertising and related revenue

•
Ended the quarter with 6.3 million TiVo One Monthly Active Users, representing 70% year-over-year footprint growth. Media Platform revenue grew 44% year-over-year and trailing 12-month ARPU reached $6.70.

•
Successfully executed homepage video campaigns in the U.S. and Europe including global advertising brands ranging from the entertainment, insurance, automotive and technology industries.

•
Advanced integration of the TiVo One ad platform with key partners, including Teads and Kargo, to enable seamless transactions for TiVo One's unique homepage video inventory.

Connected Car

Continued growth in AutoStage platform footprint as well as new automotive OEM programs are beginning to accelerate advertising and related revenue

•
DTS AutoStage platform footprint grew 42% year-over-year, reaching 17 million cumulative vehicles shipped with DTS AutoStage across 13 automotive brands.

•
BYD, the largest electric vehicle manufacturer in the world by global sales, joined the AutoStage program as the 14th automotive brand and committed to deploy our audio and video platform across export models in its portfolio.

•
Signed Cumulus, one of the largest U.S. broadcasters and operators of AM/FM radio stations, as the first customer for advanced analytics in our DTS AutoStage broadcaster portal. This revenue is advertising-related and will be recognized within Media Platform.

•
Signed a multi-year HD Radio program with a large Asian Tier 1 supplier to enable future HD Radio shipment growth. In addition, automotive brands BMW, Toyota, Mercedes-Benz, and Volkswagen launched new vehicle models with HD Radio in the U.S., Canada and Mexico.

Pay TV

Continued double-digit subscriber growth in video-over-broadband along with key design wins demonstrate partner commitment to the TiVo platform

•
Ended the quarter with 3.4 million global IPTV subscriber households, representing 13% year-over-year growth.

•
Expanded our advertising reach by executing a partnership agreement for Programmatic Dynamic Ad Insertion (PDAI) with the National Cable Television Cooperative (NCTC).

•
Entered into agreements with NCTC member operators Summit Broadband, EPB, and Buckeye to adopt TiVo as their PDAI platform.

Consumer Electronics

Continued trend of securing long-term renewals with commitments to our technology

•
Closed a multi-year renewal for DTS audio solutions, including new commitments for DTS Clear Dialogue across multiple TV and PC brands.

•
Renewed DTS agreements with leading TV, audio, and video receiver brands, including Sony, Yamaha, Pioneer, and Insignia.

•
Renewed DTS agreements for PC and mobile devices with MSI and Tecno Reallytek.

Financial Outlook

The Company maintains its guidance with respect to Revenue, Adjusted EBITDA Margin, Operating Cash Flow, Non-GAAP Tax Expense and Share Count.

The Company has increased its Capital Expenditures outlook to approximately $25 million, from a prior range of $15-20 million, due primarily to continued constraints in the memory market that resulted in price increases in planned capital equipment purchases. In addition, the Company is responding to partner demand for incremental investment to reduce memory requirements in the Company's software platforms.

The Company has lowered its anticipated Stock-based Compensation outlook to approximately $29 million, from a prior estimate of $31 million, due primarily to the impact of workforce reductions.

Category | Outlook
Revenue | $440M to $470M
Adjusted EBITDA Margin 1,2 | 17% to 19%
Operating Cash Flow | $15M to $25M
Capital Expenditures 3 | ~$25M
Non-GAAP Tax Expense 2 | ~$20M
Basic and Fully Diluted Share Count | 48M to 49M
Stock-based Compensation | ~$29M

1 See discussion of "Non-GAAP Financial Measures" below.

2 With respect to Adjusted EBITDA Margin and Non-GAAP Tax Expense, the Company has determined that it is unable to provide a quantitative reconciliation of these forward-looking non-GAAP measures to the most directly comparable forward-looking GAAP measure with a reasonable degree of confidence in its accuracy without unreasonable effort, as items including restructuring and impacts from discrete tax adjustments and tax law changes are inherently uncertain and depend on various factors, many of which are beyond the Company's control.

3 Capital Expenditures is defined as the sum of two items from the Consolidated Statements of Cash Flows: Capitalized Internal-Use Software and Purchases of Property and Equipment.

Conference Call Information

The Company will hold its second quarter 2026 earnings conference call at 2:00 PM Pacific Time (5:00 PM Eastern Time) on Wednesday, August 5, 2026. To access the call toll-free, please dial 1-888-596-4144, otherwise for USA/International dial 1-646-968-2525 and Canada-Toronto 1-647-495-7514. The conference ID is 5483252. All participants should dial in 15 minutes prior to the start of the call using the conference ID listed above. Alternatively, the call can be accessed via the following webcast link: Q2 2026 Earnings Call Webcast .

Average Revenue Per User (ARPU) for TiVo One is calculated by dividing advertising and related revenue (excluding automotive-related revenue) for the trailing four quarters by the average number of TiVo One Monthly Active Users during that same period. This metric helps investors and management measure how effectively the Company monetizes its media platform through advertising and data.

Non-GAAP Financial Measures

In addition to disclosing financial results calculated in accordance with U.S. Generally Accepted Accounting Principles ("GAAP"), the Company's press release contains non-GAAP financial measures, including Non-GAAP Operating Income/(Loss), Non-GAAP Net Income/(Loss), Non-GAAP Net Income/(Loss) Per Share, Non-GAAP Adjusted EBITDA, Non-GAAP Adjusted EBITDA Margin, Free Cash Flow, and Non-GAAP Tax Expense.

Non-GAAP Operating Income/(Loss) is defined as GAAP Operating Income/(Loss), less the impact of stock-based compensation; amortization of intangible assets; transaction, integration and restructuring costs; severance and retention costs; and other items not indicative of our ongoing operating performance.

Non-GAAP Net Income/(Loss) is defined as GAAP Net Income/(Loss) excluding the impact of stock-based compensation; amortization of intangible assets; transaction, integration and restructuring costs; severance and retention costs; and other items not indicative of our ongoing operating performance; and related tax effects for each adjustment.

Non-GAAP Net Income/(Loss) Per Share is defined as Non-GAAP Income/(Loss) divided by Non-GAAP weighted average shares outstanding - diluted.

Non-GAAP Adjusted EBITDA is defined as GAAP Net Income/(Loss), less the impact of interest expense; provision for income taxes; stock-based compensation; depreciation expense; amortization of intangible assets; amortization of capitalized cloud computing costs; transaction, integration and restructuring costs; severance and retention costs; and other items not indicative of our ongoing operating performance.

Non-GAAP Adjusted EBITDA Margin is defined as Non-GAAP Adjusted EBITDA divided by total revenue.

Free Cash Flow is defined as net cash from operating activities, less cash investments for capitalized internal-use software and purchases of property and equipment.

Non-GAAP Tax Expense is defined as the GAAP provision for income taxes, adjusted to reflect the net direct and indirect income tax effects of the various non-GAAP pretax adjustments.

Management believes that the non-GAAP measures used in this press release provide investors with important perspectives into the Company's ongoing business and financial performance and provide a better understanding of our core operating results reflecting our normal business operations. The non-GAAP financial measures disclosed by the Company should not be considered a substitute for, or superior to, financial measures calculated in accordance with GAAP. Our use of non-GAAP financial measures has certain limitations in that the non-GAAP financial measures we use may not be directly comparable to those reported by other companies. For example, the terms used in this press release, such as adjusted EBITDA, do not have a standardized meaning. Other companies may use the same or similarly named measures, but exclude different items, which may not provide investors with a comparable view of our performance in relation to other companies. We seek to compensate for the limitation of our non-GAAP presentation by providing a detailed reconciliation of the non-GAAP financial measures to the most directly comparable GAAP financial measures in the tables attached hereto. Investors are encouraged to review the related GAAP financial measures and the reconciliation of these non-GAAP financial measures to their most directly comparable GAAP financial measures. All financial data is presented on a GAAP basis except where the Company indicates its presentation is on a non-GAAP basis.

Set forth below are reconciliations of the Company's reported GAAP to non-GAAP financial measures.

Xperi Investor Contact:

Idalia Rodriguez

Arbor Advisory Group

+1 203-293-3325

ir@xperi.com

Media Contact:

Tom Huntington

+1 619-743-9057

thomas.huntington@xperi.com

– Tables Follow –

SOURCE: XPERI INC.

XPER-E

# # #

XPERI INC.

CONDENSED CONSOLIDATED STATEMENTS OF OPERATIONS

(in thousands, except per share amounts)

(unaudited)

Three Months Ended June 30, | Six Months Ended June 30,
2026 | 2025 | 2026 | 2025
Revenue:
Licensing and other revenue | 99,510 | 96,207 | 206,357 | 204,229
Advertising and related revenue | 14,982 | 9,726 | 22,341 | 15,737
Total revenue | 114,492 | 105,933 | 228,698 | 219,966
Operating expenses:
Cost of licensing and other revenue, excluding depreciation and amortization of intangible assets | 19,829 | 22,128 | 41,996 | 47,067
Cost of advertising and related revenue, excluding depreciation and amortization of intangible assets | 16,241 | 11,421 | 24,954 | 16,081
Research and development | 21,806 | 29,783 | 48,889 | 69,332
Selling, general and administrative | 41,463 | 41,142 | 83,250 | 89,840
Depreciation expense | 3,951 | 3,448 | 8,212 | 6,353
Amortization expense | 8,092 | 9,144 | 16,136 | 18,866
Impairment of long-lived assets | 197 | — | 197 | —
Total operating expenses | 111,579 | 117,066 | 223,634 | 247,539
Income (loss) from operations | 2,913 | (11,133 | 5,064 | (27,573
Interest and other income, net | 1,097 | 1,747 | 1,916 | 4,042
Interest expense - debt | (684 | (759 | (1,362 | (1,491
Income (loss) before taxes | 3,326 | (10,145 | 5,618 | (25,022
Provision for income taxes | 4,826 | 4,636 | 14,944 | 8,125
Net loss | (1,500 | (14,781 | (9,326 | (33,147
Net loss per share - basic and diluted | (0.03 | (0.32 | (0.19 | (0.73
Weighted-average number of shares used in computing net loss per share - basic and diluted | 48,421 | 45,846 | 47,890 | 45,313

XPERI INC.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-26_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

Business Overview

We are a leading media and entertainment technology company. Our technologies are integrated into consumer devices, connected cars, and a variety of media platforms worldwide, enabling our unique audiences to connect with entertainment content in a more intelligent, immersive, and personal way. As our audiences engage with content on our platform, we operate a global, cross-screen advertising solution that enables brands to reach millions of engaged consumers across our rapidly expanding digital entertainment ecosystem, driving increased value for our partners, customers, and consumers. We operate in one reportable business segment and group our revenue into four categories: Pay-TV, Consumer Electronics, Connected Car and Media Platform. Headquartered in Silicon Valley with operations around the world, we have approximately 1,460 employees and more than 35 years of operating experience.

Divestitures

In December 2023, we entered into a definitive agreement with Tobii AB, an eye tracking and attention computing company, pursuant to which we agreed to sell our AutoSense in-cabin safety business and related imaging solutions (the "AutoSense Divestiture"). The AutoSense Divestiture was completed in January 2024 and has streamlined our business and further enhanced our focus on entertainment markets.

In August 2024, we entered into an Asset Purchase Agreement with Amazon.com Services LLC to sell substantially all of the assets and certain liabilities of Perceive Corporation ("Perceive", later known as Xperi Pylon Corporation and subsequently dissolved in December 2024), a subsidiary focused on edge inference hardware and software technologies, for a gross amount of $80.0 million in cash, including a holdback of $12.0 million to be held for 18 months after the closing of the transaction (the "Perceive Transaction") to secure our and Perceive's indemnification obligations. The Perceive Transaction was completed in October 2024, allowing us to be fully focused on entertainment-based solutions to grow our independent media platform and licensing businesses.

Macroeconomic Conditions

Macroeconomic conditions—including rising inflation and interest rates, recessionary concerns, financial and credit market volatility, shifts in economic policy, reduced discretionary spending by consumers and businesses, tariffs, and global supply chain disruptions—have adversely affected, and may continue to affect, our business and that of our customers. While we remain committed to closely monitoring these macroeconomic developments and intend to adapt our business strategies as needed, the ultimate impact on our business, operating results, and financial condition remains uncertain.

Restructuring Activities

In November 2025, we approved a restructuring plan designed to improve cost efficiency and better align our operating structure with our long-term strategies and prevailing market conditions. The plan involved a reduction of approximately 250 employees across all business and functional areas and became effective immediately. In connection with this plan, we incurred restructuring and related charges of $13.9 million in 2025, substantially all of which consisted of employee severance and related costs. These charges are reflected within cost of revenue (excluding depreciation and amortization of intangible assets),

research and development, and selling, general and administrative expenses in our Consolidated Statements of Operations. We expect to substantially complete the restructuring activities by the end of the first half of 2026. Upon completion, we estimate that the reductions will generate annualized savings in the range of approximately $30 million to $35 million. For further information, refer to Note 15— Restructuring Activities of the Notes to Consolidated Financial Statements .

Results of Operations

The following table presents our historical operating results for the periods indicated as a percentage of revenue:

Year Ended December 31,
2025 | 2024
Revenue | 100 | % | 100 | %
Operating expenses:
Cost of revenue, excluding depreciation and amortization of intangible assets | 28 | 23
Research and development | 30 | 39
Selling, general and administrative | 41 | 44
Depreciation expense | 3 | 3
Amortization expense | 8 | 9
Impairment of long-lived assets | — | —
Total operating expenses | 110 | 118
Operating loss | (10 | (18
Interest and other income, net | 2 | 1
Interest expense - debt | (1 | (1
Gain on divestitures | — | 20
(Loss) income before taxes | (9 | 2
Provision for income taxes | 4 | 2
Net loss | (13 | )% | — | %

Comparison of Fiscal Years Ended December 31, 2025 and 2024

Revenue

We derive the majority of our revenue from licensing our technologies and solutions to customers. For our revenue recognition policy including descriptions of revenue-generating activities, refer to Note 3— Revenue of the Notes to Consolidated Financial Statements.

The following table sets forth our revenue by year:

Year Ended December 31,
2025 | 2024 | $ Change | % Change
(dollars in thousands)
Revenue | 448,105 | 493,688 | (45,583 | (9 | )%

Revenue decreased by $45.6 million, or 9%, for the year ended December 31, 2025 compared to the prior year, primarily due to a $54.0 million decline in Pay‑TV revenue and the impact of the AutoSense and Perceive divestitures. The decrease in Pay‑TV revenue was driven by lower revenue from core guide products, principally due to higher minimum guarantee ("MG") revenue recognized in the prior year, as well as lower consumer hardware and related subscription revenue as certain products reached end of life in 2025. These decreases were partially offset by continued growth in IPTV solutions.

The overall decline was partially mitigated by a $13.2 million increase in Connected Car revenue, primarily reflecting higher MG and licensing revenue related to HD Radio. This increase was offset in part by a reduction in Audio Solutions revenue due to the absence of certain MG revenue recognized in the prior year.

Operating Expenses

Year Ended December 31,
2025 | 2024 | $ Change | % Change
(dollars in thousands)
Cost of revenue, excluding depreciation and amortization of intangible assets | 126,648 | 113,756 | 12,892 | 11 | %
Research and development | 135,054 | 191,352 | (56,298 | (29 | )%
Selling, general and administrative | 181,869 | 218,106 | (36,237 | (17 | )%
Depreciation expense | 13,426 | 12,638 | 788 | 6 | %
Amortization expense | 34,839 | 43,376 | (8,537 | (20 | )%
Impairment of long-lived assets | — | 1,535 | (1,535 | (100 | )%
Total operating expenses | 491,836 | 580,763 | (88,927 | (15 | )%

Cost of Revenue, Excluding Depreciation and Amortization of Intangible Assets

Cost of revenue, excluding depreciation and amortization of intangible assets, consists primarily of employee-related costs, royalties paid to third parties, hardware product-related costs, content and data costs, hosting fees, maintenance costs and an allocation of facilities costs, as well as service center and other expenses related to providing our offerings, and non-recurring engineering ("NRE") services.

Cost of revenue, excluding depreciation and amortization of intangible assets, for the year ended December 31, 2025 was $126.6 million, as compared to $113.8 million for the year ended December 31, 2024, an increase of $12.8 million, or 11%. The increase was primarily driven by higher costs associated with advertising revenue and increased personnel-related expenses.

Research and Development

Research and development ("R&D") costs consist primarily of employee-related costs, stock-based compensation ("SBC") expense, engineering consulting expenses associated with new product and technology development, product commercialization, quality assurance and testing costs, as well as other costs related to patent applications and examinations, materials, supplies, and an allocation of facilities costs. Other than certain software development costs that are capitalized, all research and development costs are expensed as incurred.

R&D expense for the year ended December 31, 2025 was $135.1 million as compared to $191.4 million for the year ended December 31, 2024, a decrease of $56.3 million, or 29%. The decrease was primarily attributable to a reduction in R&D headcount, reduced expenses associated with the Perceive Transaction, lower SBC and outside services costs, and lower R&D spending in the AutoSense in-cabin safety business and related imaging solutions following the AutoSense Divestiture.

Selling, General and Administrative

Selling expenses consist primarily of compensation and related costs (including SBC expense) for sales and marketing personnel engaged in sales and licensee support, marketing programs, public relations, promotional materials, travel, and trade shows. General and administrative expenses consist primarily of compensation and related costs (including SBC expense) for management, information technology, finance and legal personnel, legal fees and related expenses, facilities costs, and professional services. Our general and administrative expenses, other than facilities-related expenses and fringe benefits, are not allocated to other expense line items.

Selling, general and administrative expenses for the year ended December 31, 2025 were $181.9 million as compared to $218.1 million for the year ended December 31, 2024, a decrease of $36.2 million, or 17%. This decrease was primarily driven by reduced employee headcount, lower SBC and outside services expenses, and a reduction in certain one-time transaction costs.

Depreciation Expense

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-26_item1_business.md)

Item 1. B usiness

Corporate Information

The principal executive offices of Xperi Inc. ("we," "our," the "Company," or "Xperi") are located at 2190 Gold Street, San Jose, California 95002 USA. Our telephone number is +1 (408) 519-9100. We maintain a corporate website at www.xperi.com. The reference to our website address does not constitute incorporation by reference of the information contained on this website. Xperi, the Xperi logo, TiVo, the TiVo logo, DTS, the DTS logo, DTS HD, DTS Audio Processing, DTS:X Ultra, DTS Virtual:X, DTS Headphone:X, DTS Play-Fi, DTS:X, HD Radio, DTS AutoStage, DTS AutoStage Video Service Powered by TiVo, TiVo OS and TiVo+ are trademarks or registered trademarks of Xperi or its affiliated companies in the United States and other countries. All other company, brand and product names may be trademarks or registered trademarks of their respective companies.

Overview

We are a leading media and entertainment technology company. Our technologies are integrated into consumer devices, connected cars, and a variety of media platforms worldwide, enabling our unique audiences to connect with entertainment content in a more intelligent, immersive, and personal way. As our audiences engage with content on our platform, we operate a global, cross-screen advertising solution that enables brands to reach millions of engaged consumers across our rapidly expanding digital entertainment ecosystem, driving increased value for our partners, customers, and consumers. We operate in one reportable business segment and group our revenue into four categories: Pay-TV, Consumer Electronics, Connected Car and Media Platform. Headquartered in Silicon Valley with operations around the world, we have approximately 1,460 employees and more than 35 years of operating experience.

In November 2025, we approved a restructuring plan designed to improve cost efficiency and better align our operating structure with our long-term strategies and prevailing market conditions that included a reduction of approximately 250 employees across all business and functional areas. For further information, refer to Note 15— Restructuring Activities of the Notes to Consolidated Financial Statements.

Market Opportunity

Consumer behaviors around media consumption are undergoing a significant transformation, driven by new platforms for content delivery, greater content diversity, and an increase in time spent consuming video content. Video content delivery is rapidly shifting from linear broadcast to over-the-top streaming platforms, impacting not just how users consume content, but also the ad-supported programming ecosystem and commercial model. Our technologies sit at the forefront of this transformation, enhancing experiences where consumers spend the most time – in their homes and in their cars.

•
Shift to Streaming : Streaming has rapidly become a mainstream content delivery mechanism through a wide variety of providers such as Netflix, Disney+ and YouTube. Streaming media now accounts for roughly 54% of U.S. weekly video viewing for adults ages 18 and older. The proliferation of streaming content has created the need for a new generation of entertainment products that are centered on the streaming viewing experience. Consumers are increasingly looking for solutions that allow them to navigate across the fragmented and complex entertainment landscape of streaming content.

•
Advertising Monetization : The shift to streaming has not only impacted user needs for entertainment devices but also disrupted the ad-based programming model that was centered on linear TV programming. While delivering ad-based programming to streaming audiences has presented new challenges, it has also created opportunities for advertisers to deliver personalized, highly relevant, and targeted ad content to a rapidly growing audience. Since the majority of video advertising dollars are currently allocated toward linear TV, we believe the streaming advertising market is positioned for significant growth in the next 3 to 5 years as advertisers continue to follow the viewing audience as it shifts viewing habits from traditional linear television to streaming. At the same time, there is a new set of industry participants that are looking for ways to monetize the ad-based streaming video ecosystem, including consumer electronics manufacturers, Smart TV OEMs, automotive manufacturers, and video-over-broadband ("IPTV") operators that have historically not participated in the streaming advertising value chain. Thus, we believe there is a significant market opportunity for an independent media platform that enables participants to monetize their products through recurring revenue streams across the lifecycle of the device rather than just a one-time monetization opportunity at the point-of-sale.

•
Market Need for an Independent Media Platform : Roughly half of all Smart TVs each year are shipped into Western Europe and North America by leading electronics manufacturers who do not currently support the technology, content, and monetization capabilities of a proprietary Smart TV OS and streaming media platform. The same situation is also true for automotive manufacturers. This creates a unique opportunity for an independent media platform that allows Smart TV OEMs to brand the experience to maintain the customer relationship, provide the necessary scale to secure top content streaming providers, and participate in the long-term monetization throughout the typical 5- to 7-year lifecycle of TV ownership.

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

**Present:** meta.json, form4_summary.md, 8-K_2026-08-05_2-02-results.md, 10-K_2026-02-26_item7_mdna.md, 10-K_2026-02-26_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
