# Triage pack — WBTN · WEBTOON Entertainment Inc.

_Generated 2026-09-05 03:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** WBTN · **Name:** WEBTOON Entertainment Inc.
- **CIK:** 0001997859
- **SIC:** 2741 — Miscellaneous Publishing
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/WBTN

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** WEBTOON Entertainment Inc.
- **CIK:** 1,997,859 · **SIC:** 2741 (Miscellaneous Publishing) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 9.99 |
| mktcap | $1.4B |
| ev | $772.6M |
| ev_ebit | n/a |
| fcf | $3.6M |
| fcf_yield | 0.3% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -8.6% |
| net_debt | -$583.1M |
| net_debt_ebit | n/a |
| cash | $583.1M |
| ltd | $0.00 |
| equity | $1.2B |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $1.4B |
| revenue_prior | $1.3B |
| rev_growth | 2.5% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$63.5M |
| net_income | -$373.4M |
| cfo | $11.2M |
| capex | $7.6M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 3.9% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 135,711,070 |
| shares_py | 130,608,276 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -36.6% |
| r6m | -3.8% |
| off_52w_high | -53.1% |
| adv20 | $4.4M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.22 |
| r_ev_ebit | 0.00 |
| r_roic | 0.14 |
| r_rev_growth | 0.43 |
| r_buyback | 0.22 |
| score | 0.20 |

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
| rank | 464 |

**Screen rationale:** debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **135,711,070** (CY2026Q2I) vs **130,608,276** prior year (CY2025Q2I)
- Change: **3.9%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-10** — Item 1.01 (Entry into a Material Definitive Agreement): On August 6, 2026, WEBTOON Entertainment Inc., a Delaware corporation (the "Company"), entered into a Share Purchase Agreement (the "Purchase Agreement") with Redice & Company, Inc., a joint-stock company established under the laws of the Republic of Korea...
- **2026-04-13** — Item 5.02 (officer / director change or comp arrangement): On April 13, 2026, WEBTOON Entertainment Inc. (the "Company") announced a number of executive leadership changes.
- **2026-03-30** — Item 5.02 (officer / director change or comp arrangement): On March 26, 2026, the Board of Directors (the "Board") of WEBTOON Entertainment Inc. (the "Company") approved a housing assistance policy (the "Housing Assistance Policy") for the Company's Chief Executive Officer (the "CEO") in connection with the...
- **2026-03-30** — Item 5.02 (officer / director change or comp arrangement): On March 5, 2026, WEBTOON Entertainment Inc. (the "Company") filed a Current Report on Form 8-K (the "Initial Report") with the Securities and Exchange Commission to report, among other things, the appointment of Yongsoo Kim as the President of the Company.

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 12 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 4 |
| F | 8 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-05-11_2-02-results.md)

_Extraction: started at the first release heading, 'WEBTOON Entertainment Inc. Reports First Quarter 2026 Financial Result'; skipped 10 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (wbtn-20260511xexx991.htm)

WEBTOON Entertainment Inc. Reports First Quarter 2026 Financial Results

Delivered Revenue Within Guidance Range and Adjusted EBITDA Well Above the High-End of Guidance Range

First Quarter Revenue Decline of 1.5% Year-Over-Year; Revenue Growth on a Constant Currency Basis of 0.2%

Net Loss of $8.8 million; Adjusted EBITDA of $9.5 million

Strong Balance Sheet With Cash and Cash Equivalents of Approximately $594.9 million and No Debt

LOS ANGELES, May 11, 2026 (GLOBE NEWSWIRE) -- WEBTOON Entertainment Inc. (Nasdaq: WBTN) ("WEBTOON Entertainment" or "the Company"), a leading global entertainment company and home to some of the world's largest storytelling platforms, today announced results for its first quarter ended March 31, 2026. More information about these results can be found in the Company's shareholder letter on the investor relations section of its website.

First Quarter 2026 Highlights (vs. First Quarter 2025)

• Total revenue of $320.9 million declined 1.5%, driven by declines in IP Adaptations and Advertising, partially offset by growth in Paid Content.

• Revenue on a constant currency basis was $326.4 million, growing 0.2%, driven by growth in Paid Content and Advertising, offset by a decline in IP Adaptations.

• Net Loss was $8.8 million, compared to $22.0 million in the prior year, driven primarily by better gross profit.

• Adjusted EBITDA was $9.5 million, compared to $4.1 million in the prior year, due to effective cost controls. Adjusted EBITDA Margin was 3.0%, compared to 1.3% in the prior year.

• Diluted loss per share was $0.07, compared to diluted loss per share of $0.17 in the prior year.

• Adjusted Earnings Per Share was $0.07, compared to $0.03 in the prior year.

• Cash and cash equivalents of approximately $594.9 million plus another $11.1 million of short-term deposits included in prepaid expenses and other current assets.

• Cash outflow from operations was $11.8 million, compared to a cash outflow of $18.7 million in the prior year.

Junkoo Kim, Founder and CEO, said, "We are pleased to share our solid first quarter results with constant currency revenue of $326.4 million, in line with our expectations, and a significant Adjusted EBITDA increase of 132% year-over-year."

Kim continued, "Importantly, we are continuing to strategically invest across our flywheel. We remain focused on expanding our creator ecosystem, and will introduce major updates to our amateur CANVAS platform throughout the year, positioning us well to produce even more diverse content that our users love. As we look to the rest of the year, we will remain focused on investing in the business to drive further innovation and long-term growth."

Second Quarter 2026 Outlook

For the second quarter 2026, the Company expects:

• Revenue growth on a constant currency basis in the range of 1.7%-4.6%. This represents revenue in the range of $332-$342 million, based on current FX rates.

• Adjusted EBITDA in the range of $0.0-$5.0 million, representing an Adjusted EBITDA Margin in the range of 0.0%-1.5%.

Conference Call & Webcast Details

As previously disclosed, the Company will host a webcast and conference call on May 11, 2026, at 4:30 p.m. Eastern Time, to discuss the Company's financial results for its first quarter ended March 31, 2026.

A live webcast of the conference call will be available online at https://ir.webtoon.com/.

For those unable to listen to the live webcast, an archived version will be available at the same location for up to one year.

About WEBTOON Entertainment Inc.

WEBTOON Entertainment is a leading global entertainment company and home to some of the world's largest storytelling platforms. As the global leader and pioneer of the mobile webcomic format, WEBTOON Entertainment has transformed comics and visual storytelling for fans and creators.

With its CANVAS UGC platform empowering anyone to become a creator, and a growing roster of superstar WEBTOON Originals creators and series, WEBTOON Entertainment's passionate fandoms are the new face of pop culture. WEBTOON Entertainment adaptations are available on Netflix, Prime Video, Crunchyroll, and other screens around the world, and the company's content partners have included Warner Bros. Animation, Discord, HYBE, and Duolingo, among many others.

With approximately 145 million monthly active users, WEBTOON Entertainment's IP & Creator Ecosystem of aligned brands and platforms include WEBTOON, Wattpad--the world's leading webnovel platform--WEBTOON Productions, Studio N, Studio LICO, WEBTOON Unscrolled, LINE MANGA, and eBookJapan, among others.

Adjusted Earnings Per Share (Adjusted EPS): We define Adjusted Earnings Per Share as Earnings Per Share before interest expense, interest income, income tax expense (benefit) and depreciation and amortization with further adjustments to eliminate the effects of loss on equity method investments, effect of applying the valuation method of fair value through profit or loss, impairment of goodwill, non-cash stock-based compensation and certain other non-recurring costs. We calculate Adjusted Earnings Per Share by making the adjustments described herein from Net Income (Loss) and dividing by basic and diluted weighted average shares of common stock outstanding, respectively, for the applicable period.

Revenue on a Constant Currency Basis: We define revenue on a constant currency basis as revenue adjusted to remove the impact of foreign currency rate fluctuations and the impact of deconsolidated and transferred operations. We calculate revenue on a constant currency basis in a given period by applying the average currency exchange rates in the comparable period of the prior year to the local currency revenue in the current period. We calculate revenue on a constant currency basis in each of our revenue streams – Paid Content, Advertising and IP Adaptations – using the same method as laid out herein.

Revenue Growth on a Constant Currency Basis: We define revenue growth on a constant currency basis as period-over-period growth rates of revenue, adjusted to remove the impact of foreign currency rate fluctuations and the impact of deconsolidated and transferred operations. We calculate revenue growth (as a percentage) on a constant currency basis by determining the increase in current period revenue over prior period revenue, where current period foreign currency revenue is translated using prior period average currency exchange rates.

Financial Statements

WEBTOON Entertainment Inc.

Consolidated Balance Sheets

(unaudited)

(in thousands of USD, except share and per share data)

As of
March 31, 2026 | December 31, 2025
Assets
Current assets:
Cash and cash equivalents | 594,852 | 581,806
Receivables 1 , net of allowance for credit losses of $1,703 and $3,378 at March 31, 2026 and December 31, 2025 respectively | 182,781 | 176,779
Prepaid expenses and other current assets, net 2 | 73,369 | 72,647
Total current assets | 851,002 | 831,232
Property and equipment, net | 10,594 | 8,339
Operating lease right-of-use assets | 20,510 | 23,705
Debt and equity securities | 64,348 | 69,669
Intangible assets, net | 150,923 | 157,804
Goodwill, net | 330,832 | 336,825
Equity method investments | 76,212 | 80,440
Deferred tax assets | 23,643 | 22,302
Other non-current assets, net 3 | 65,681 | 65,194
Total assets | 1,593,745 | 1,595,510
Liabilities and equity
Current liabilities:
Accounts payable 4 | 137,695 | 136,962
Accrued expenses 5 | 53,837 | 66,690
Current portion of operating lease liabilities 6 | 8,679 | 9,617
Contract liabilities | 94,640 | 89,994
Taxes payable | 7,000 | 4,136
Provisions and defined pension benefits | 7,013 | 8,766
Other current liabilities | 3,913 | 2,457
Total current liabilities | 312,777 | 318,622
Non-current liabilities:
Long-term operating lease liabilities 7 | 11,673 | 14,055
Defined severance benefits | 24,502 | 25,069
Deferred tax liabilities | 5,879 | 5,755
Other non-current liabilities | 3,683 | 3,737
Total liabilities | 358,514 | 367,238
Commitments and Contingencies (Note 8)
Redeemable non-controlling interest in subsidiary | 24,336 | 24,540
Stockholders' equity:
Common stock, $0.0001 par value (2,000,000,000 authorized, 134,635,086 shares and 130,776,161 shares issued and outstanding as of March 31, 2026, and December 31, 2025, respectively) | 13 | 13
Additional paid-in capital | 2,177,445 | 2,137,926
Accumulated other comprehensive loss | (137,007) | (114,363)
Accumulated deficit | (862,579) | (853,124)
Total stockholders' equity attributable to WEBTOON Entertainment Inc. | 1,177,872 | 1,170,452
Non-controlling interests in consolidated subsidiaries | 33,023 | 33,280

Total equity | 1,210,895 | 1,203,732
Total liabilities, redeemable non-controlling interest, and equity | 1,593,745 | 1,595,510

1. Includes amounts due from related parties of $54,303 and $55,156 as of March 31, 2026, and December 31, 2025, respectively.

2. Includes amounts due from related parties of $4,053 and $4,730 as of March 31, 2026, and December 31, 2025, respectively.

3. Includes amounts due from related parties of $33,786 and $33,913 as of March 31, 2026, and December 31, 2025, respectively.

4. Includes amounts due to related parties of $24,207 and $18,765 as of March 31, 2026, and December 31, 2025, respectively.

5. Includes amounts due to related parties of $6,048 and $6,849 as of March 31, 2026, and December 31, 2025, respectively.

6. Includes amounts due to related parties of $4,953 and $5,221 as of March 31, 2026, and December 31, 2025, respectively.

7. Includes amounts due to related parties of $3,933 and $5,371 as of March 31, 2026, and December 31, 2025, respectively.

WEBTOON Entertainment Inc.

Consolidated Statements of Operations and Comprehensive Loss

(unaudited)

(in thousands of USD, except share and per share data)

Three Months Ended
March 31, 2026 | March 31, 2025
Revenue 1 | 320,872 | 325,707
Cost of revenue 2 | (237,824) | (254,096)
Marketing 3 | (30,520) | (31,543)
General and administrative expenses 4 | (60,559) | (66,702)
Operating income (loss) | (8,031) | (26,634)
Interest income | 4,374 | 5,113
Interest expense | (17) | (2)
Gain (loss) on equity method investments, net | (446) | (569)
Other income (loss), net 5 | (2,005) | 2,670
Income (loss) before income tax | (6,125) | (19,422)
Income tax expense | (2,672) | (2,547)
Net income (loss) | (8,797) | (21,969)
Net income (loss) attributable to WEBTOON Entertainment Inc. | (9,455) | (22,389)
Net income (loss) attributable to non-controlling interests and redeemable non-controlling interests | 658 | 420
Other comprehensive income (loss):
Foreign currency translation adjustments, net of tax | (23,747) | 6,572
Share of other comprehensive loss of equity method investments, net of tax | (15) | (143)
Total other comprehensive income (loss), net of tax | (23,762) | 6,429
Total comprehensive income (loss) | (32,559) | (15,540)
Total comprehensive income (loss) attributable to WEBTOON Entertainment Inc. | (32,099) | (15,999)
Total comprehensive income (loss) attributable to non-controlling interests and redeemable non-controlling interests | (460) | 459
Weighted average shares outstanding
Basic | 133,618,587 | 129,598,942
Diluted | 133,618,587 | 129,598,942
Income (loss) per share attributable to WEBTOON Entertainment Inc.
Basic | (0.07) | (0.17)
Diluted | (0.07) | (0.17)

1. Includes amounts earned from related parties of $18,243 and $17,713 for the three months ended March 31, 2026, and March 31, 2025, respectively.

2. Includes amounts incurred from related parties of $27,071 and $28,131 for the three months ended March 31, 2026, and March 31, 2025, respectively.

3. Includes amounts incurred from related parties of $(1,729) and $(2,581) for the three months ended March 31, 2026, and March 31, 2025, respectively.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-05_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

WEBTOON is a global storytelling platform where a vibrant community of creators and users discover, create and share new content. We have pioneered a cultural movement by revolutionizing the storytelling format and democratizing content creation and publication. WEBTOON empowers creators, by enabling them to participate economically in their own creation, and users, by offering an endless library of content.

Content on our platform tells stories, across formats. On our platform, creators tell long-form stories through serialized narratives in the form of short-form, bite-sized episodes, creating a habitual behavior with an engaged user base. These stories are primarily told in two ways—web-comics, a graphical comic-like medium, and web-novels, which are text-based stories. The web-comic medium tells stories using a continuous vertical-scroll format that is easily read on mobile devices. We are able to extend the reach, impact and monetization of our content by adapting it into other media formats such as film, streaming series, games, merchandise and print books.

Creators power our content engine by authoring immersive visual stories, developing imaginative new characters and inspiring fandoms. Our creator base ranges from the individual enthusiast with a love of storytelling to the professional author building a brand and an enterprise on our platform. WEBTOON provides creators with an opportunity to monetize their creativity through various means, including Paid Content, advertising and IP Adaptations.

Users come to our platform to discover and consume engaging and immersive content. Our creators tell stories that are relatable to global audiences, attracting users across age groups, geographies and genders. Our primary user base is Gen Z and millennials. WEBTOON helps fans discover engaging content across genres, with fresh, weekly releases.

Community reinforces the benefits to creators and users on our platform. We help users and creators build relationships and engage with one another over content. As users, or "fans," often develop a personal connection to the titles on our platform, they relish the direct engagement with creators through both our comments section at the end of each episode and the "Creator Profile" section, where creators can post messages and users can respond directly. Fans also appreciate the ability to potentially influence how stories unfold and how their favorite characters evolve, as creators may choose to incorporate fans' feedback. This enables a positive feedback loop for content creation and user engagement. This community engagement powers a flywheel of user engagement and creator readership, which in turn drives WEBTOON's success.

Our platform continuously empowers and incentivizes creators to drive creation of unique long-form stories. These stories are enjoyed on our platform by a growing base of loyal fans and importantly, enable us to expand the audience base off-platform over time. This continuous cycle results in successful and durable franchises within our ever-growing content library, empowering us with a multitude of monetization opportunities through IP Adaptations.

Key Business Metrics

We believe our performance is dependent upon many factors, including the key metrics described below that we track and review to measure our performance, identify trends, formulate financial projections, and make strategic decisions.

Our offerings include WEBTOON, LINE MANGA, NAVER SERIES, eBookJapan, Munpia and Wattpad. We manage our business by tracking several operating metrics, including: monthly active users, or MAU; monthly paying users, or MPU; and Paid Content Average Revenue per Paying User, or ARPPU. For a definition of these operating

metrics, please see the "Glossary." As a management team, we believe each of these operating metrics provides useful information to investors and others.

Our year-over-year activity and quarter-over-quarter growth trends may fluctuate subject to various internal and external factors including (i) seasonality of our business where we see increased activity during holiday season, (ii) magnitude of our marketing campaigns, (iii) hiatus/return of creators and key titles on our platforms, (iv) TV shows, films, and/or gaming release based on our content as part of our IP Adaptation business, (v) our strategic decision to direct traffic to our mobile application may lead to fluctuations in trends as web users who view in both mediums may choose to continue to consume on our mobile application only and (vi) external factors impacting the global economy, our industry and our company.

Geographic Tracking

We review each metric by geography where our products are available and accessible. We categorize geographies into Korea, Japan, and Rest of World ("ROW") based on the location of our users:

• Korea includes WEBTOON Korea, NAVER SERIES, and Munpia where our content is in Korean and targeted at Korean speaking users.

• Japan includes LINE MANGA and eBookJapan where our content is in Japanese and targeted at Japanese speaking users.

• Rest of World includes WEBTOON in all other languages including English, Spanish, and more, as well as Wattpad, where our content is targeted at global users outside of Korea and Japan.

In particular, as a proxy for tracking our performance in North America, which we consider to be a key market, amongst Rest of World, we track users who consume WEBTOON offered in English in the U.S. and Canada based on such user's Internet Protocol (IP) addresses (collectively "WEBTOON North America"). For clarity, the following cases are not counted as part of WEBTOON North America but counted as part of Rest of World: (i) where users consume non-English (e.g., Spanish) WEBTOON content while they are physically based in North America and (ii) where users consume non-WEBTOON products (e.g., Wattpad) while they are physically based in North America.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Consolidated Statements of Operations and Comprehensive Loss

The following table sets forth our consolidated statement of operations for 2025 and 2024. This data should be read in conjunction with our audited consolidated financial statements. Historical results are not necessarily indicative of the results that may be expected in the future.

Year Ended December 31,
(in thousands of USD) | 2025 | 2024 | % Change
Revenue | 1,382,705 | 1,348,478 | 2.5 | %
Cost of revenue | (1,060,524) | (1,009,410) | 5.1 | %
Marketing | (126,149) | (107,783) | 17.0 | %
General and administrative expenses | (259,543) | (331,984) | (21.8 | %)
Operating loss | (63,511) | (100,699) | (36.9) | %
Interest income | 19,170 | 15,820 | 21.2 | %
Interest expense | (56) | (45) | 24.4 | %
Impairment losses on goodwill and other intangible assets | (336,486) | (69,743) | 382.5 | %
Gain (loss) on equity method investments, net | 1,282 | (1,123) | (214.2 | %)
Other income (loss), net | (9,808) | 6,482 | (251.3) | %
Loss before income tax | (389,409) | (149,308) | 160.8 | %
Income tax benefit (expense) | 16,022 | (3,604) | (544.6 | %)
Net loss | (373,387) | (152,912) | 144.2 | %
Net income (loss) attributable to non-controlling interests and redeemable non-controlling interests | (27,460) | (9,007) | 204.9 | %
Total comprehensive loss attributable to WEBTOON Entertainment Inc. | (345,927) | (143,905) | 140.4 | %

Comparison of the Years Ended December 31, 2025 and December 31, 2024

Revenue

Year Ended December 31,
(in thousands of USD) | 2025 | 2024 | % Change
Revenue | 1,382,705 | 1,348,478 | 2.5 | %
Paid Content | 1,087,496 | 1,083,026 | 0.4 | %
Advertising | 164,257 | 166,087 | (1.1 | %)
IP Adaptations | 130,952 | 99,365 | 31.8 | %

Revenue increased by $34.2 million, or 2.5%, for the year ended December 31, 2025, as compared to the year ended December 31, 2024, primarily related to strong growth in IP Adaptations. The decrease of $1.8 million, or 1.1%, in advertising revenue was driven by declines in Korea and Rest of World, largely offset by double-digit growth in Japan.

Cost of Revenue

Year Ended December 31,
(in thousands of USD) | 2025 | 2024 | % Change
Cost of revenue | (1,060,524) | (1,009,410) | 5.1 | %

Our cost of revenue increased by $51.1 million, or 5.1%, for the year ended December 31, 2025, as compared to the year ended December 31, 2024. The increase was primarily driven by higher sales commissions and content fees paid to creators, which were commensurate with the growth in revenue. In addition, we have invested in labor to further improve our platform and drive growth.

Marketing

Year Ended December 31,
(in thousands of USD) | 2025 | 2024 | % Change
Marketing | (126,149) | (107,783) | 17.0 | %

Marketing expenses increased by $18.4 million, or 17.0%, for the year ended December 31, 2025, as compared to the year ended December 31, 2024. The increase was a result of our continued investment in marketing to drive growth in converting users to paid users.

General and Administrative Expenses

Year Ended December 31,
(in thousands of USD) | 2025 | 2024 | % Change
General and administrative expenses | (259,543) | (331,984) | (21.8 | %)

General and administrative expenses decreased by $72.4 million, or 21.8%, for the year ended December 31, 2025, as compared to the year ended December 31, 2024. The decrease was primarily driven by lower stock-based compensation expense of $30.9 million, compared to $75.2 million for the year ended December 31, 2024. In addition, the decrease was due to the base effect of a one-time bonus of $30.0 million granted to the CEO for a successful IPO and other non-recurring costs associated with our initial public offering incurred in 2024. (See Note. 11 Stock-Based Compensation for more information about our stock-based compensation expense).

Interest Income

Year Ended December 31,
(in thousands of USD) | 2025 | 2024 | % Change
Interest income | 19,170 | 15,820 | 21.2 | %

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-05_item1_business.md)

Item 1. Business

Overview

WEBTOON is a global storytelling platform where a vibrant community of creators and users discover, create and share new content. We have pioneered a cultural movement by revolutionizing the storytelling format and democratizing content creation and publication. WEBTOON empowers creators, by enabling them to participate economically in their own creation, and users, by offering an endless library of content. Our community connected 27 million creators with approximately 157 million monthly active users in over 150 countries around the world. 1

Our Platform

Our creators, users and content drive a powerful community flywheel. By creating and publishing new and diverse content, creators on our platform help drive the scale of our user base. In turn, users build relationships with creators through real-time feedback and praise on content; fandoms built around popular characters, storylines or in-story universes; and monetary support through payments for access to content. This attracts new creators to our platform, who expand our community and deepen engagement with fans, which leads to an even stronger feedback loop and encourages more content creation. We further amplify this flywheel through other monetization models, including advertising and IP Adaptations. Finally, our platform is underpinned by our foundational technology and artificial intelligence, enabling content creation and discovery and recommendation. The result is increased user engagement, creator prosperity and, ultimately, WEBTOON success.

Creators power our content engine by authoring immersive visual stories, or titles, developing imaginative new characters and inspiring fandoms. Our creator base ranges from the individual enthusiast with a love of storytelling to the professional author building a brand and an enterprise on our platform. WEBTOON provides creators with an opportunity to monetize their creativity through various means, including Paid Content, advertising and IP Adaptations. Our platform serves both amateur and professional creators, the latter defined as creators who monetize through Paid Content on our platform under formal creator agreements with Paid Content revenue sharing provisions. We consider these two groups of creators separately because their intention is often distinct: amateur creators may come to our platform simply for the love of our unique form of storytelling and to connect with an engaged and like-minded audience, and the vast majority of the 27 million creators on our platform are amateur creators. Professional creators are often building a brand and an enterprise on our platform. We believe there exists a strong potential for our amateur creator base to serve as a source of future professional creators. Particularly in markets where the creator talent base is in earlier stages of development, building a local amateur creator base will be one of the most important drivers of future professional content. A core part of our strategy in those markets is identifying high-potential amateur creators whom we promote and help start monetizing their content on our platform.

Users come to our platform to discover and consume engaging and immersive content. Our creators tell stories that are relatable to global audiences, attracting users across age groups, geographies and genders.

Content on our platform tells stories created by our creators through multiple immersive formats. On our platform, creators tell long-form stories through our iconic serialized narratives in the form of short-form, bite-sized episodes. This content format results in a habitual behavior with an engaged user base. These stories are told primarily in two ways—web-comics, a graphical comic-like medium, and web-novels, which are text-based stories. The web-comic medium tells stories using a continuous vertical-scroll format that is easily read on mobile devices. For both formats, the serialized release of content is analogous to chapters of a book. These formats are not only accessible and highly engaging for fans, but also easier for creators to create, share and monetize their stories. We are able to further extend the reach, impact and monetization of our content by adapting it into other media formats such as film, streaming series, games, merchandise and print books.

Community reinforces the benefits to creators and users on our platform. We help users and creators build relationships and engage with one another over content. As users, or "fans," often develop a personal connection to the titles on our platform, they relish the direct engagement with creators through both our comments section at the end of each episode and the "Creator Profile" section, where creators can post messages and users can respond directly. Fans also appreciate the ability to potentially influence how stories unfold and how their favorite characters evolve, as creators may choose to incorporate fans' feedback. This enables a positive feedback loop for content creation and user engagement. This

1 Metrics are as of the year ended December 31, 2025.

community engagement powers a flywheel of user engagement and creator readership, which in turn drives WEBTOON's success.

This vibrant ecosystem is amplified by our foundational technology and artificial intelligence capabilities, which enable content creation, along with our content discovery and recommendation engines. Our content creation technology helps creators enhance their storytelling skills, tailor the content to various global audiences and build more engaged, wider fan bases around the world. For users, our technology enables a personalized recommendation model and rule-based curation methodology to encourage new content discovery. These tools are highly scalable across markets and our newer markets are able to benefit from the content and platform infrastructure we have invested in and refined in Korea and Japan.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-05_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-05_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-05_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-05-11_2-02-results.md, 10-K_2026-03-05_item7_mdna.md, 10-K_2026-03-05_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
