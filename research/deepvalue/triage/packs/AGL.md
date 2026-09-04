# Triage pack — AGL · agilon health, inc.

_Generated 2026-09-04 21:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** AGL · **Name:** agilon health, inc.
- **CIK:** 0001831097
- **SIC:** 8090 — Services-Misc Health & Allied Services, NEC
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/AGL

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** agilon health, inc.
- **CIK:** 1,831,097 · **SIC:** 8090 (Services-Misc Health & Allied Services, NEC) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 86.48 |
| mktcap | $1.5B |
| ev | $1.4B |
| ev_ebit | n/a |
| fcf | -$119.0M |
| fcf_yield | -8.2% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | -$91.8M |
| net_debt_ebit | n/a |
| cash | $107.2M |
| ltd | $15.4M |
| equity | n/a |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $5.9B |
| revenue_prior | $6.1B |
| rev_growth | -2.1% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$463.2M |
| net_income | -$391.3M |
| cfo | -$105.8M |
| capex | $13.2M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -95.9% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 16,791,210 |
| shares_py | 414,423,149 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 259.5% |
| r6m | 420.2% |
| off_52w_high | -33.4% |
| adv20 | $23.8M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.09 |
| r_ev_ebit | 0.00 |
| r_roic | 0.50 |
| r_rev_growth | 0.27 |
| r_buyback | 0.99 |
| score | 0.42 |

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
| rank | 310 |

**Screen rationale:** buying back stock -95.9%; 12-1 momentum 259.5%


## 3. Share count trend

- Shares outstanding: **16,791,210** (CY2026Q2I) vs **414,423,149** prior year (CY2025Q2I)
- Change: **-95.9%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-22** — Item 5.02 (officer / director change or comp arrangement): On July 17, 2026, agilon health, inc. (the "Company") provided notice to Girish Venkatachaliah, the Company's Chief Technology Officer, that Mr. Venkatachaliah's employment with the Company will terminate effective August 1, 2026 (the "Separation Date").
- **2026-04-27** — Item 5.02 (officer / director change or comp arrangement): On April 24, 2026, agilon health, inc. (the "Company") entered into an Employment Agreement (the "Employment Agreement") with Tim O'Rourke, pursuant to which Mr. O'Rourke will serve as the Company's Chief Executive Officer and President, reporting to the...

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 13 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 8 |
| F | 5 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-05_2-02-results.md)

_Extraction: started at the first release heading, 'agilon health Reports Second Quarter 2026 Results'; skipped 5 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (agl-20260630xexx991.htm)

agilon health Reports Second Quarter 2026 Results

Revenue increase 7% to $1.49 billion

Raises Full-Year 2026 Total Revenues, Medical Margin, and Adjusted EBITDA Guidance

Westerville, O.H., August 5, 2026 – agilon health, inc. (NYSE: AGL), the trusted partner empowering physicians to transform health care in our communities, today announced results for the second quarter ended June 30, 2026. In addition, the company increased full-year 2026 guidance for total revenues, medical margin, and Adjusted EBITDA.

"Our second quarter results exceeded our expectations, demonstrating meaningful progress across agilon's strategic initiatives and reinforcing our confidence in the strength of our Total Care Model," said Tim O'Rourke, Chief Executive Officer of agilon health. "We are raising our full-year 2026 outlook which reflects stronger burden of illness execution, favorable medical cost trends, and continued operating discipline. As I have engaged with our physician partners, payors, and the agilon team, I am even more convinced about the strength and long-term growth potential of the agilon model and its positioning at the center of where value-based care is going."

Second Quarter 2026 Results:

• Total members on the agilon platform decreased to 549,000 as of June 30, 2026, including 437,000 Medicare Advantage members and 112,000 ACO model beneficiaries. Year-over-year changes to membership primarily reflect a disciplined approach to contracting focused on profitability, previously disclosed market exits, and a measured approach to growth.

• Total revenue of $1.49 billion in the second quarter 2026 increased 7% compared to $1.39 billion in the second quarter 2025. Revenue was favorable due to higher than expected burden of illness performance, payor contracting, and improved pricing partially offset by lower year-over-year membership.

• Gross profit was $107 million in the second quarter 2026 compared to gross loss of $52 million in the second quarter 2025. Net income was $18 million in the second quarter 2026 compared to net loss of $104 million in the second quarter 2025.

• Medical margin was $197 million during the second quarter 2026, compared to negative $53 million in the second quarter 2025. Medical margin includes favorable first quarter 2026 and prior year claims development.

• Adjusted EBITDA was $70 million in the second quarter 2026 compared to negative $83 million in the second quarter 2025.

Key Financial and Operating Metrics ($M):

(Second Quarter 2026 vs. 2025)

Three Months Ended June 30, | Change
2026 | 2025 | % YoY
Medicare Advantage Members 1 | 437,000 | 498,000 | (12%)
ACO Model Members 1,2 | 112,000 | 116,000 | (3%)
Total Members Live on Platform 1,2 | 549,000 | 614,000 | (10%)
Avg. Medicare Advantage Members | 447,000 | 498,000 | (10%)
Total Revenues | $1,495 | $1,395 | 7%
Gross Profit (Loss) | $107 | $(52) | NM
Medical Margin | $197 | $(53) | NM
Net Income (Loss) | $18 | $(104) | NM
Adjusted EBITDA 3 | $70 | $(83) | NM
Geography Entry Costs | $4 | $5 | (20%)

1. Membership metrics reflect end of period results.

2. agilon's ACO model entities are not included within its consolidated financial results.

3. agilon's ACO model entities contributed $7 million and $10 million to Adjusted EBITDA during the second quarter 2026 and second quarter 2025, respectively.

Capital Position and Balance Sheet

agilon health's balance sheet as of June 30, 2026 included cash, cash equivalents and marketable securities of $257 million and total debt of $32 million. At the end of the quarter, agilon health had $83 million of cash associated with the Company's unconsolidated ACO model entities.

Third Quarter and Revised Fiscal Year 2026 Guidance and Assumptions

Guidance for Fiscal Year 2026 ($M) :

Year Ended December 31, 2026
Updated Guidance | Previous Guidance as of First Quarter 2026
Low | High | Low | High
Medicare Advantage Members 1 | 435,000 | 445,000 | 425,000 | 435,000
ACO REACH Members 1,2 | 100,000 | 105,000 | 100,000 | 105,000
Total Members Live on Platform 1 | 535,000 | 550,000 | 525,000 | 540,000
Avg. Medicare Advantage Members | 438,000 | 443,000 | 430,000 | 437,000
Total Revenues | $5,775 | $5,860 | $5,680 | $5,805
Medical Margin | $465 | $505 | $350 | $400
Adjusted EBITDA 3 | $75 | $95 | $10 | $40
Geography Entry Costs 4 | $15 | $15 | $15 | $15

1. Membership reflects management's outlook for end of period.

2. agilon's partnered ACO model entities are not consolidated within its financial results.

3. Adjusted EBITDA contribution from ACO model entities is expected to be approximately $25-$30 million for fiscal year 2026.

4. Geography Entry Costs represent the corresponding expense included in the low-end and high-end of management's outlook for Adjusted EBITDA.

Guidance for Third Quarter 2026 ($M) :

Quarter Ended September 30, 2026
Low | High
Medicare Advantage Members 1 | 433,000 | 443,000
ACO REACH Members 1,2 | 106,000 | 109,000
Total Members Live on Platform 1 | 539,000 | 552,000
Avg. Medicare Advantage Members | 445,000 | 455,000
Total Revenues | $1,445 | $1,475
Medical Margin | $105 | $115
Adjusted EBITDA | ($5) | $5
Geography Entry Costs 3 | $6 | $6

1. Membership reflects management's outlook for end of period.

2. agilon's partnered ACO model entities are not consolidated within its financial results.

3. Geography Entry Costs represent the corresponding expense included in the low-end and high-end of management's outlook for Adjusted EBITDA.

Full-year revised guidance reflects:

• Second quarter 2026 performance;

• An expected increase year-over-year in member risk scores of 3% net of v28; and

• Estimated cost trends in the low 7% range for the remainder of the year.

The Company has not reconciled guidance for medical margin to gross profit (loss) or Adjusted EBITDA to net income (loss), the most comparable GAAP measures, and has not provided forward-looking guidance for gross profit (loss) or net income (loss) in each case because of the uncertainty around certain items that may impact gross profit (loss) or net income (loss), including non-cash stock-based compensation, which cannot be predicted without unreasonable effort.

Webcast and Conference Call

agilon health will host a conference call to discuss second quarter 2026 results on Wednesday, August 5, 2026, at 4:30 PM Eastern Time. The conference call can be accessed by dialing (833) 439-1904 for U.S. participants and +1 (585) 542-9983 for international participants and referencing participant code 372460207. A simultaneous listen-only, live webcast can be accessed by visiting the "Events & Presentations" section of agilon's Investor Relations website at https://investors.agilonhealth.com . A replay of the call will be available via webcast for on-demand listening shortly after the completion of the call.

About agilon health

agilon health is the trusted partner empowering physicians to transform health care in our communities. Through our partnerships and purpose-built platform, agilon is accelerating at scale how physician groups and health systems transition to a value-based Total Care Model for their senior patients. agilon provides the technology, people, capital, process, and access to a peer network of approximately 2,300 primary care physicians (PCPs) that allow its physician partners to maintain their independence and focus on the total health of their most vulnerable patients. Together, agilon and its physician partners are creating the healthcare system we need – one built on the value of care, not the volume of fees. The result: healthier communities and empowered doctors. agilon is the trusted partner in approximately 30 communities and is here to help more of our nation's leading physician groups and health systems have a sustained, thriving future. For more information visit www.agilonhealth.com and connect with us on LinkedIn .

June 30, 2026 | December 31, 2025
(unaudited)
ASSETS
Current assets:
Cash and cash equivalents | 107,184 | 173,713
Restricted cash and equivalents | 71,627 | —
Marketable securities | 78,443 | 111,429
Receivables, net | 1,059,786 | 673,793
Prepaid expenses and other current assets, net | 101,494 | 137,762
Total current assets | 1,418,534 | 1,096,697
Property, equipment, and capitalized software, net | 24,513 | 25,417
Intangible assets, net | 60,132 | 65,725
Other assets | 88,157 | 83,451
Total assets | 1,591,336 | 1,271,290
LIABILITIES AND STOCKHOLDERS' EQUITY (DEFICIT)
Current liabilities:
Medical claims and related payables | 1,022,506 | 929,770
Accounts payable and accrued expenses | 274,928 | 127,477
Current debt | 14,915 | 19,238
Total current liabilities | 1,312,349 | 1,076,485
Long-term debt | 15,377 | 15,750
Other liabilities | 36,083 | 52,321
Total liabilities | 1,363,809 | 1,144,556
Commitments and contingencies
Stockholders' equity (deficit):
Common stock, $0.01 par value: 2,000,000 shares authorized; 16,785 and 16,589 shares issued and outstanding, respectively | 168 | 166
Additional paid-in capital | 2,138,657 | 2,103,976
Accumulated deficit | (1,911,452) | (1,978,324)
Accumulated other comprehensive income (loss) | 154 | 916
Total stockholders' equity (deficit) | 227,527 | 126,734
Total liabilities and stockholders' equity (deficit) | 1,591,336 | 1,271,290

agilon health, inc.

Condensed Consolidated Statements of Operations

In thousands, except per share data

(unaudited)

Three Months Ended June 30, | Six Months Ended June 30,
2026 | 2025 | 2026 | 2025
Revenues:
Medical services revenue | 1,492,921 | 1,392,039 | 2,911,470 | 2,921,918
Other operating revenue | 1,822 | 2,943 | 3,733 | 5,846
Total revenues | 1,494,743 | 1,394,982 | 2,915,203 | 2,927,764
Expenses:
Medical services expense | 1,296,235 | 1,445,245 | 2,565,863 | 2,847,112
Other medical expenses | 91,369 | 2,164 | 177,186 | 82,357
General and administrative | 88,505 | 56,281 | 142,736 | 122,237
Depreciation and amortization | 6,864 | 7,319 | 13,651 | 14,195
Total expenses | 1,482,973 | 1,511,009 | 2,899,436 | 3,065,901
Income (loss) from operations | 11,770 | (116,027) | 15,767 | (138,137)
Other income (expense):
Income (loss) from equity method investments | (7,596) | 5,412 | 4,137 | 18,084
Other income (expense), net | 15,015 | 7,879 | 31,040 | 17,140
Interest expense | (1,608) | (1,572) | (3,419) | (3,087)
Income (loss) before income taxes | 17,581 | (104,308) | 47,525 | (106,000)
Income tax benefit (expense) | 375 | (62) | 347 | (258)
Income (loss) from continuing operations | 17,956 | (104,370) | 47,872 | (106,258)
Discontinued operations:
Adjustments on sale of assets, net | — | — | 19,000 | 14,000
Net income (loss) | 17,956 | (104,370) | 66,872 | (92,258)
Basic earnings per common share:
Continuing operations | 1.07 | (6.31) | 2.88 | (6.43)
Discontinued operations | — | — | 1.14 | 0.85
Net income (loss) | 1.07 | (6.31) | 4.02 | (5.58)
Diluted earnings per common share:
Continuing operations | 1.04 | (6.31) | 2.84 | (6.43)
Discontinued operations | — | — | 1.12 | 0.85
Net income (loss) | 1.04 | (6.31) | 3.96 | (5.58)
Weighted average shares outstanding
Basic | 16,705 | 16,553 | 16,653 | 16,535
Diluted | 17,213 | 16,553 | 16,884 | 16,535

agilon health, inc.

Condensed Consolidated Statements of Cash Flows

In thousands

(unaudited)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-25_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview and Recent Developments

Our business is transforming healthcare by empowering the PCP to be the agent for change in the communities they serve. We believe that PCPs, with their intimate patient-physician relationships, are best positioned to drive meaningful change in quality, cost, and patient experience when provided with the right infrastructure and payment model. Through our combination of the agilon platform, a long-term partnership model with existing physician groups and a growing network of like-minded physicians, we believe we are poised to revolutionize healthcare for seniors across communities throughout the United States. We believe our purpose-built model provides the necessary capabilities, capital and business model for existing physician groups to create a Medicare-centric, globally capitated line of business. Our model operates by forming RBEs within local geographies, that enter into arrangements with payors providing for monthly or quarterly payments to manage the total healthcare needs of our physician partners' attributed patients (or, global capitation arrangements). The RBEs also contract with agilon to perform certain functions and enter into long-term professional service agreements with one or more anchor physician groups pursuant to which the anchor physician groups receive a base compensation rate and share in the savings from successfully improving quality of care and reducing costs.

Our business model is differentiated by its focus on existing community-based physician groups and is built around three key elements: (1) agilon's platform; (2) agilon's long-term physician partnership model; and (3) agilon's network. With our model, our goal is to remove the barriers that prevent community-based physicians from evolving to a Total Care Model, where the physician is empowered to manage health outcomes and the total healthcare needs of their attributed Medicare patients.

2025 Results:

• MA members of approximately 511,000 as of December 31, 2025 decreased 3% from 2024.

• The CMS ACO Models attributed beneficiaries of approximately 114,000 as of December 31, 2025 decreased 13% from 2024.

• Total revenue of $5.93 billion decreased 2% from 2024.

• Gross loss of $160.0 million, compared to gross profit of $4.8 million in 2024.

• Medical margin was negative $56.6 million, compared to earnings of $205.2 million in 2024.

• Net loss of $391.3 million, compared to net loss of $260.1 million in 2024.

• Adjusted EBITDA loss of $296.2 million, compared to Adjusted EBITDA loss of $154.2 million in 2024.

Platform Membership Details

MA members decreased 3% during 2025, which was primarily attributable to partnership exits during 2024. Total members live on the agilon platform include 511,000 MA members and 114,000 attributed CMS ACO Models beneficiaries. Average MA membership during 2025 was approximately 510,000.

Reverse Stock Split

On February 6, 2026, we filed a preliminary proxy statement indicating our intent to seek stockholder approval at a special meeting of stockholders to be held on March 17, 2026 for the purpose of seeking: (i) an amendment to our Amended and Restated Certificate of Incorporation to effect a reverse stock split of our common stock at a ratio of one-for-five to one-for-twenty-five, with the exact ratio to be set within this range by the Board in its sole discretion without further stockholder approval, and (ii) authority to adjourn the special meeting, if necessary, to solicit additional proxies if there are insufficient votes to approve the amendment. See the risk factor titled " The listing of shares of our common stock does not currently comply with the continued listing requirements of the NYSE, and if the NYSE delists our common stock, it could have an adverse impact on the trading, liquidity and market price of our common stock " in Item 1A. Risk Factors included in this Report.

Key Financial and Operating Metrics

All of our key metrics exclude historical results from our Hawaii operations (which are included as discontinued operations in our consolidated financial statements).

We monitor the following key financial and operating metrics to help us evaluate our business, identify trends affecting our business, formulate business plans and make strategic decisions. We believe the following key metrics are useful in evaluating our business (dollars in thousands):

As of and for the
Year Ended December 31,
2025 | 2024 | 2023
MA members | 511,000 | 526,500 | 388,400
Medical services revenue | 5,921,341 | 6,047,715 | 4,307,350
Gross profit (loss) | (160,021) | 4,841 | 69,670
Medical margin (1) | (56,565) | 205,185 | 298,691
Platform support costs | 159,986 | 169,402 | 163,652
Net income (loss) | (391,347) | (260,101) | (262,803)
Adjusted EBITDA (1) | (296,155) | (154,215) | (95,001)

(1) Medical margin and Adjusted EBITDA are non-GAAP financial measures. Gross profit (loss) is the most directly comparable financial measure calculated in accordance with accounting principles generally accepted in the United States of America ("U.S. GAAP") to medical margin. Net income (loss) is the most directly comparable financial measure calculated in accordance with U.S. GAAP to Adjusted EBITDA. See "—Non-GAAP Financial Measures" below for additional information.

Medicare Advantage Members

Our MA members include all individuals enrolled in an MA plan that are attributed to the PCPs on our platform at the end of a given period.

Medical Services Revenue

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The following table summarizes key components of our results of operations (dollars in thousands):

Year Ended December 31,
2025 | 2024 | 2023
Revenues:
Medical services revenue | 5,921,341 | 6,047,715 | 4,307,350
Other operating revenue | 11,235 | 12,815 | 9,013
Total revenues | 5,932,576 | 6,060,530 | 4,316,363
Expenses:
Medical services expense | 5,977,906 | 5,842,530 | 4,008,659
Other medical expenses | 114,691 | 213,159 | 238,034
General and administrative | 238,536 | 268,912 | 285,760
Depreciation and amortization | 28,594 | 24,463 | 16,043
Impairments | 36,085 | 3,596 | —
Total expenses | 6,395,812 | 6,352,660 | 4,548,496
Income (loss) from operations | (463,236) | (292,130) | (232,133)
Other income (expense):
Income (loss) from equity method investments | (1,835) | 14,992 | 16,489
Other income (expense), net | 67,616 | 34,489 | 27,840
Interest expense | (6,641) | (6,177) | (6,658)
Income (loss) before income taxes | (404,096) | (248,826) | (194,462)
Income tax benefit (expense) | (1,251) | (1,451) | (791)
Income (loss) from continuing operations | (405,347) | (250,277) | (195,253)
Discontinued operations:
Income (loss) before gain (loss) on sales | — | (1,061) | (20,002)
Gain (loss) and adjustments on sales of assets, net | 14,000 | (8,763) | (47,548)
Total discontinued operations | 14,000 | (9,824) | (67,550)
Net income (loss) | (391,347) | (260,101) | (262,803)
Noncontrolling interests' share in (earnings) loss | — | (50) | 207
Net income (loss) attributable to common shares | (391,347) | (260,151) | (262,596)

The following table summarizes our results of operations as a percentage of total revenues:

Year Ended December 31,
2025 | 2024 | 2023
Revenues:
Medical services revenue | 100 | % | 100 | % | 100 | %
Other operating revenue | — | — | —
Total revenues | 100 | 100 | 100
Expenses:
Medical services expense | 101 | 96 | 93
Other medical expenses | 2 | 4 | 6
General and administrative | 4 | 4 | 7
Depreciation and amortization | — | — | —
Impairments | 1 | — | —
Total expenses | 108 | 105 | 105
Income (loss) from operations | (8) | (5) | (5)
Other income (expense):
Income (loss) from equity method investments | — | — | —
Other income (expense), net | 1 | 1 | 1
Interest expense | — | — | —
Income (loss) before income taxes | (7) | (4) | (5)
Income tax benefit (expense) | — | — | —
Income (loss) from continuing operations | (7) | (4) | (5)
Discontinued operations:
Income (loss) before gain (loss) on sales | — | — | —
Gain (loss) and adjustments on sales of assets, net | — | — | (1)
Total discontinued operations | — | — | (2)
Net income (loss) | (7) | (4) | (6)
Noncontrolling interests' share in (earnings) loss | — | — | —
Net income (loss) attributable to common shares | (7) | % | (4) | % | (6) | %

Comparison of Year Ended December 31, 2025 and 2024

The following discussion should be read in conjunction with "Cautionary Language Regarding Forward-Looking Statements," Part I, Item 1 "Business," Part I, Item 1A "Risk Factors," and our consolidated financial statements and related notes included under Item 8 of this Report. In Item 7, we generally discuss 2025 and 2024 items and year-to-year comparisons between 2025 and 2024. For a discussion of the financial condition and results of operations for 2024 compared to 2023, see Part II, Item 7. "Management's Discussion and Analysis of Financial Condition and Results of Operations" in our Annual Report on Form 10-K for the year ended December 31, 2024, filed with the SEC on February 25, 2025.

Medical Services Revenue

Year Ended December 31, | Change
(dollars in thousands) | 2025 | 2024 | %
Medical services revenue | 5,921,341 | 6,047,715 | (126,374) | (2) | %
% of total revenues | 100 | % | 100 | %

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-25_item1_business.md)

ITEM 1. Business

Overview

Our business is transforming healthcare by empowering the primary care physicians ("PCP") to be the agents for change in the communities they serve. We believe that PCPs, with their intimate patient-physician relationships, are best positioned to drive meaningful change in quality, cost and patient experience when provided with the right infrastructure and payment model. Through our combination of the agilon platform, a long-term partnership model with existing physician groups and a growing network of like-minded physicians, we believe we are poised to revolutionize healthcare for seniors across communities throughout the United States ("U.S."). We believe our purpose-built model provides the necessary capabilities, capital and business model for existing physician groups to create a Medicare-centric, globally capitated line of business. Our model operates by primarily forming risk-bearing entities ("RBEs") within local geographies, that enter into arrangements with payors providing for monthly payments to manage the total healthcare needs of our physician partners' attributed patients (or global capitation arrangements). The RBEs also contract with agilon to perform certain functions and enter into long-term professional service agreements with one or more anchor physician groups pursuant to which the anchor physician groups receive a base compensation rate and share in the savings from successfully improving quality of care and reducing costs.

Our company was formed in 2016, and we established our inaugural partnership with an anchor physician group in 2017. Our ability to rapidly build scaled positions in local communities has allowed us to grow to 28 anchor physician groups and 30 geographies as of December 31, 2025. As of December 31, 2025, the PCPs on our platform serve approximately 511,000 MA members and 114,000 Medicare fee-for-service ("FFS") beneficiaries through nine Accountable Care Organizations ("ACOs") through our participation in the Centers for Medicare & Medicaid Services' ("CMS") Accountable Care Organization Realizing Equity, Access, and Community Health ("ACO REACH") Model and Medicare Shared Savings Program ("MSSP," and together with ACO REACH, the "CMS ACO Models") through its equity method investments.

On November 5, 2025, we received written notice (the "Notice") from the NYSE informing us that we are no longer in compliance with Section 802.01C of the NYSE Listed Company Manual because the average closing price of our common stock was less than $1.00 per share over a consecutive 30 trading-day period ended November 4, 2025 (the "Price Criteria for Capital or Common Stock").

We can regain compliance at any time within the six-month period following receipt of the Notice if, on the last trading day of any calendar month during the cure period (or the last trading day of the cure period), we have a closing share price of at least $1.00 and an average closing share price of at least $1.00 over the prior 30 trading-day period ending on the last trading day of the applicable calendar month or the cure period. To regain compliance with the Price Criteria for Capital or Common Stock, we are pursuing a reverse stock split, subject to approval by our stockholders. We expect to seek stockholder approval at our special meeting to be held March 17, 2026. Under the NYSE Listed Company Manual, if we determine that we will cure the stock price deficiency by taking an action that will require stockholder approval, such as a reverse stock split, and we receive stockholder approval no later than our next general meeting of stockholders, the price condition will be deemed cured if, following stockholder approval and implementation of the approved action, the share price promptly exceeds $1.00 per share and the share price remains above that level for at least the following 30 trading days. See the risk entitled " The listing of shares of our common stock does not currently comply with the continued listing requirements of the NYSE, and if the NYSE delists our common stock, it could have an adverse impact on the trading, liquidity and market price of our common stock " under "Item 1A. Risk Factors" in this Report for more information.

For a description of our significant activities during 2025, see "Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations—2025 Results" in this Report.

Our business model is differentiated by its focus on existing community-based physician groups and is built around three key elements: (1) agilon's platform; (2) agilon's long-term physician partnership approach; and (3) agilon's network. With our model, our goal is to remove the barriers that prevent community-based physicians from evolving to a Total Care Model, where the physician is empowered to manage quality and health outcomes and the total healthcare needs of their attributed Medicare patients.

The agilon Platform : The agilon platform is holistic in supporting the rapid transition to a Total Care Model with technology, people, process and capital. Our purpose-built platform is comprised of an integrated set of capabilities

designed to continuously improve, helping our anchor physician groups to identify gaps in care, integrate seamlessly with payors, sustain their practices, and identify untapped opportunities for improved outcomes. Our platform is delivered to our anchor physician groups through a long-term partnership model to support the adoption and success of a Medicare-centric, globally capitated line of business.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-25_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-25_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-25_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-05_2-02-results.md, 10-K_2026-02-25_item7_mdna.md, 10-K_2026-02-25_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
