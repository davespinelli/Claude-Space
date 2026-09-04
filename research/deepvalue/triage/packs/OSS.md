# Triage pack — OSS · ONE STOP SYSTEMS, INC.

_Generated 2026-09-04 22:10 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** OSS · **Name:** ONE STOP SYSTEMS, INC.
- **CIK:** 0001394056
- **SIC:** 3571 — Electronic Computers
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/OSS

**Fetcher warnings for this ticker:** 10-K 2026-03-18: heading split missed Item 1A - Risk Factors

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** ONE STOP SYSTEMS, INC.
- **CIK:** 1,394,056 · **SIC:** 3571 (Electronic Computers) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

> **EARNINGS QUALITY FLAG — one-off items likely.**
> net income more than 3x operating income.
> Reported net income is not supported by the operating engine that is supposed to produce it (typical causes: gains on sale, legal settlements, deferred-tax valuation-allowance releases, bargain-purchase gains). Reconcile net income to operating income in the earnings release (section 7) before treating any earnings-based metric here as repeatable.

**Valuation**

| metric | value |
|---|---|
| price | 9.76 |
| mktcap | $243.4M |
| ev | $226.1M |
| ev_ebit | n/a |
| fcf | -$223k |
| fcf_yield | -0.1% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | -$17.3M |
| net_debt_ebit | n/a |
| cash | $17.3M |
| ltd | $0.00 |
| equity | n/a |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $32.2M |
| revenue_prior | $24.6M |
| rev_growth | 31.2% |
| rev_growth_note | n/a |
| eq_flag | net income more than 3x operating income |
| ebit | -$3.4M |
| net_income | $5.1M |
| cfo | -$108k |
| capex | $115k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 13.8% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 24,940,130 |
| shares_py | 21,924,818 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 129.0% |
| r6m | 15.1% |
| off_52w_high | -51.1% |
| adv20 | $9.3M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.20 |
| r_ev_ebit | 0.00 |
| r_roic | 0.50 |
| r_rev_growth | 0.90 |
| r_buyback | 0.10 |
| score | 0.39 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | n/a |
| shares_period | CY2026Q2I |
| shares_py_period | CY2025Q2I |
| capex_missing | False |
| ltd_missing | True |

**Other screen columns**

| metric | value |
|---|---|
| rank | 330 |

**Screen rationale:** revenue +31.2%; debt data missing (net cash unverified); 12-1 momentum 129.0%; EARNINGS QUALITY: net income more than 3x operating income — one-off items likely


## 3. Share count trend

- Shares outstanding: **24,940,130** (CY2026Q2I) vs **21,924,818** prior year (CY2025Q2I)
- Change: **13.8%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-05** — Item 1.01 (Entry into a Material Definitive Agreement): The information set forth in Item 5.02 of this Current Report on Form 8-K (this "Current Report") regarding the Employment Agreement and the Consulting Agreement (as defined in Item 5.02, below) is incorporated by reference into this Item 1.01.
- **2026-08-05** — Item 5.02 (officer / director change or comp arrangement): On July 31, 2026, One Stop Systems, Inc. (the "Company") entered into an amended and restated employment agreement with Robert Kalebaugh (the "Employment Agreement"), the Company's VP of Sales in connection with his retirement.
- **2026-05-19** — Item 5.02 (officer / director change or comp arrangement): As described in Item 5.07 below, on May 13, 2026, at the 2026 Annual Meeting of Stockholders (the "Annual Meeting") of One Stop Systems, Inc. (the "Company"), the Company's stockholders approved an amendment (the "Plan Amendment") to the Company's 2017 Equity...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 21,000 sh / $369,380 -> net $-369,380 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 23 (open-market buys 0, sales 3).

| code | rows |
|---|---|
| A | 8 |
| F | 8 |
| G | 4 |
| S | 3 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-05-08_2-02-results.md)

_Extraction: started at the first release heading, 'One Stop Systems Reports Q1 2026 Results'; skipped 8 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (oss-ex99_1.htm)

One Stop Systems Reports Q1 2026 Results

First quarter of 2026 revenue increased 55.0% year-over-year to $8.1 million,

with gross margin increasing 610-basis points to 51.6%

Net cash provided by continuing operating activities of $4.0 million for first quarter of 2026

First quarter book-to-bill of 1.8x, supporting a TTM book-to-bill above 1.2x

ESCONDIDO, Calif. – May 6, 2026 – One Stop Systems, Inc. ("OSS" or the "Company") (Nasdaq: OSS), a leader in rugged Enterprise Class compute for artificial intelligence (AI), machine learning (ML), autonomy and sensor processing at the edge, reported results for the first quarter ended March 31, 2026. First quarter comparisons are to the same year-ago periods unless otherwise noted. On December 30, 2025, the Company closed a definitive agreement to sell all assets and operations of Bressner Technology GmbH. All operations, assets, and liabilities associated with the sale of Bressner have been classified as discontinued operations.

"Positive momentum continued into 2026, driven by significant year-over-year revenue growth, disciplined execution across the business, and continued expansion in profitability," stated OSS President and CEO, Mike Knowles. "We are seeing increased demand for our enterprise-class, ruggedized compute platforms across both defense and commercial markets, which we believe supports OSS's role as a critical enabler of next-generation AI, autonomy, and sensor-driven applications at the edge."

"Importantly, higher demand is translating into tangible growth, with nearly $15 million in bookings during the first quarter, representing one of the strongest quarters of new bookings in our history. This produced a book-to-bill ratio of 1.8x, supporting our goal of maintaining a trailing twelve-month book-to-bill ratio above 1.2x. We are seeing an expansion in our pipeline and increased customer engagement, as a growing number of organizations turn to OSS for enterprise-class, deployable compute solutions. We believe this positions us to scale alongside some of the most advanced commercial and defense programs and reinforces our confidence in sustained, multi-year growth," continued, Mr. Knowles.

"We also generated record free cash flow in the quarter from continuing operations, strengthening our balance sheet, and providing flexibility to pursue both organic and inorganic growth opportunities. As a result, we believe OSS is well positioned to capitalize on a multi-year growth opportunity as demand for enterprise class, ruggedized compute at the edge remains strong," concluded Mr. Knowles.

2026 First-Quarter Financial Summary

Total revenue from continuing operations increased 55.0% to $8.1 million, from $5.2 million in the first quarter of 2025. The increase was primarily due to higher sales to a defense prime customer of data storage products to support the P-8A, higher sales to a medical imaging OEM of liquid-cooled server

products, and sales to a defense prime customer related to the design, development, and delivery of prototype compute systems for an enhanced vision system for combat vehicles.

Gross margin from continuing operations was 51.6% for the three months ended March 31, 2026, compared to 45.5% in the prior year quarter. The increase in gross margin was primarily due to a more profitable mix of revenue, engineering efficiencies in customer-funded development programs and improved manufacturing absorption due to higher production volume.

Total operating expenses from continuing operations increased 2.5% to $4.8 million. This increase was predominantly attributable to higher general and administrative expenses partially offset by lower marketing and selling and R&D expenses.

The Company reported a net loss from continuing operations of $0.4 million, or $(0.01) per diluted share for the three months ended March 31, 2026, as compared to a net loss from continuing operations of $2.3 million, or $(0.11) per share, in the prior year period. The Company reported non-GAAP net income from continuing operations of $0.3 million, or $0.01 per diluted share, compared to non-GAAP net loss of $1.7 million, or $(0.08) per share, in the prior year period.

Adjusted EBITDA, from continuing operations, a non-GAAP metric, was $0.2 million for the three months ended March 31, 2026, compared to an adjusted EBITDA loss, from continuing operations, of $1.6 million in the prior year period.

Net cash provided by continuing operations for the three months ended March 31, 2026, was $4.0 million, compared to net cash used in continuing operations of $1.5 million in the prior year period.

As of March 31, 2026, the Company reported cash, cash equivalents, and short-term investments of $34.4 million, restricted cash of $2.2 million, and total working capital of $44.7 million, compared to cash, cash equivalents, and short-term investments of $31.2 million, restricted cash of $2.2 million and total working capital of $45.3 million at December 31, 2025.

Income from Discontinued Operations, net of Income Taxes

Income from discontinued operations consists of income from the Company's Bressner Technologies subsidiary, which was sold on December 30, 2025. Income from discontinued operations also includes the gain recognized on the sale.

Loss from discontinued operations, net of income taxes, was $0.2 million for the three months ended March 31, 2026, compared to income of $0.3 million in the prior year. The loss in the current year period was due to post-transaction adjustments to the gain on sale of the Bressner business for final net working capital balances.

2026 Full Year Outlook

The Company is executing a strategic plan targeting both commercial and defense markets, aiming to provide integrated solutions and establish OSS as a platform incumbent on large, multi-year programs. This approach is expected to drive long-term value by increasing predictable, recurring revenue and building a strong, multi-year backlog.

The Company's expectations for 2026 take into consideration the following: continued growth in core defense and commercial markets, higher customer funded development sales compared to 2025 levels, the potential impacts of supply chain issues for certain components such as memory, and the current outlook for the federal government budget. Changes in these assumptions could positively or negatively impact OSS's results in 2026.

For the full year of 2026, OSS expects:

Revenue growth of 20% to 25%

Gross margin of approximately 40%

Positive EBITDA and adjusted EBITDA

Conference Call

OSS will hold a conference call to discuss its results for the first quarter of 2026, followed by a question-and-answer period.

Date: Wednesday, May 6, 2026

Time: 10:00 a.m. ET (7:00 a.m. PT)

Toll-free dial-in: 1-800-717-1738

International dial-in: 1-646-307-1865

Conference ID: 21430 (required for entry)

Webcast: https://viavid.webcasts.com/starthere.jsp?ei=1756447&tp_key=f17a290f0f

A replay of the call will be available after 1:00 p.m. ET on May 6, 2026, through May 20, 2026.

Toll-free replay: 1-844-512-2921

International replay: 1-412-317-6671

Passcode: 1121430

About One Stop Systems

One Stop Systems, Inc. (Nasdaq: OSS) is a leader in AI enabled solutions for the demanding 'edge.' OSS designs and manufactures Enterprise Class compute and storage products that enable rugged AI, sensor fusion and autonomous capabilities without compromise. These hardware and software platforms bring the latest data center performance to harsh and challenging applications, whether they are on land, sea or in the air.

OSS products include ruggedized servers, compute accelerators, flash storage arrays, and storage acceleration software. These specialized compact products are used across multiple industries and applications, including autonomous trucking and farming, as well as aircraft, drones, ships and vehicles within the defense industry.

OSS solutions address the entire AI workflow, from high-speed data acquisition to deep learning, training and large-scale inference, and have delivered many industry firsts for industrial OEM and government customers.

As the fastest growing segment of the multi-billion-dollar edge computing market, AI enabled solutions require—and OSS delivers—the highest level of performance in the most challenging environments without compromise.

OSS products are available directly or through global distributors. For more information, go to www.onestopsystems.com . You can also follow OSS on X , YouTube , and LinkedIn .

Non-GAAP Financial Measures

We believe that the use of adjusted earnings before interest, taxes, depreciation and amortization, or adjusted EBITDA, is helpful for an investor to assess the performance of the Company. The Company defines adjusted EBITDA as income (loss) before interest, taxes, depreciation, amortization, acquisition expense, impairment of long-lived assets, financing costs, government funded programs, fair value adjustments from purchase accounting, stock-based compensation expense, and expenses related to discontinued operations.

Adjusted EBITDA is not a measurement of financial performance under generally accepted accounting principles in the United States, or GAAP. Because of varying available valuation methodologies, subjective assumptions and the variety of equity instruments that can impact a company's non-cash operating expenses, we believe that providing a non-GAAP financial measure that excludes non-cash and non-recurring expenses allows for meaningful comparisons between our core business operating results and those of other companies, as well as providing us with an important tool for financial and operational decision making and for evaluating our own core business operating results over different periods of time.

Our adjusted EBITDA measure may not provide information that is directly comparable to that provided by other companies in our industry, as other companies in our industry may calculate non-GAAP financial results differently, particularly related to non-recurring and unusual items. Our adjusted EBITDA is not a measurement of financial performance under GAAP and should not be considered as an alternative to operating income or as an indication of operating performance or any other measure of performance derived in accordance with GAAP. We do not consider adjusted EBITDA to be a substitute for, or superior to, the information provided by GAAP financial results.

(Dollars may not calculate due to rounding)

Adjusted EPS excludes the impact of certain items and, therefore, has not been calculated in accordance with GAAP. We believe that exclusion of certain selected items assists in providing a more complete understanding of our underlying results and trends and allows for comparability with our peer company index and industry. We use this measure along with the corresponding GAAP financial measures to manage our business and to evaluate our performance compared to prior periods and the marketplace. The Company defines non-GAAP income (loss) as income or (loss) before amortization, government funded programs, impairment of long lived assets, stock-based compensation, expenses related to discontinued operations, and acquisition costs. Adjusted EPS expresses adjusted income (loss) on a per share basis using weighted average diluted shares outstanding.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-18_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

The Company designs, manufactures, and markets specialized enterprise class high-performance compute, high speed switch fabrics, and storage hardware and software, which are designed to target edge applications for AI/ML, sensor processing, sensor fusion, and autonomy. Edge computing is a form of computing that is done on platform or on site, connected with the data source or the user, rather than in the cloud, minimizing the need for data to be processed remotely. This growing trend increases computing performance and security, as the data does not have to travel to distant datacenter locations. Edge computing is most recognizable in applications such as sensor processing, sensor fusion, autonomy, and AI/ML. To meet the demands at the edge, we offer specialized products and system solutions that consist of computers, switch fabrics, and storage products that incorporate the latest state-of-the art components with embedded proprietary software. Such products and systems allow us to offer high-end solutions to be integrated into edge platforms in our target markets.

The global increase in load on cloud infrastructure and increase in AI applications are the primary factors driving the growth of the edge computing market. We market our products to manufacturers of automated equipment used for medical, industrial, and military applications. Our customer applications often require connection to a wide array of data sources and sensors, ultra-fast processing power, and the ability to quickly access and store large and ever-growing data sets at their physical location (rather than in the cloud). This equipment requires datacenter class performance optimized for deployment at the edge in challenging environments. Many of these edge applications have unique requirements, including special and compact form factors ruggedized for harsh conditions, which cannot be accommodated by traditional controlled air-conditioned datacenters.

We believe that we are uniquely positioned as a specialized provider to address the needs of this market, providing custom servers, data acquisition platforms, compute accelerators, solid-state storage arrays, and system I/O expansion systems. Our systems also offer industry leading capabilities that occupy less physical space and require less power consumption. We deliver this high-end technology to our customers through the sale of equipment and embedded software.

Recent Developments

Sale of Bressner Technology GmbH

On December 30, 2025, the Company signed and closed a Shares Purchsase Agreement ("SPA") pursuant to which the Company sold 100% of the issued and outstanding limited liability company interests of OSS GmbH, the sole owner of Bressner GmbH, to Hiper Euro GmbH ("Buyer"). The consummation of this transaction represented a strategic shift and prioritization of the Company's core business developing and manufacturing deployable edge computing systems for mission critical applications. At closing, the Company recognized a gain of $6,707,021.This gain is net of transaction costs that were determined to be directly attributable to the sale transaction. The base purchase price and associated gain is subject to adjustment for (i) a comparison of actual closing net working capital to a target amount, (ii) closing cash relative to a minimum cash amount (iii) closing indebtedness and (iv) seller transaction expenses. The Buyer is required to deliver a closing statement within 90 days following the closing. Any disputes regarding the adjustment are subject to resolution by an independent accounting firm. Any amounts payable to the Buyer will be satisfied first from the escrow account, with any remaining escrow balance released to the Company following final determination of the adjustment. All operations, assets, and liabilities of the divested business - including the gain recognized on the sale - have been classified as discontinued operations.

Registered Direct Offering of Common Stock

On September 29, 2025, the Company entered into a Securities Purchase Agreement (the "Purchase Agreement") with institutional investors (the "Investors"), pursuant to which the Company agreed to issue and sell to the Investors in a registered direct offering (the "Offering") 2,500,000 shares of the Company's Common Stock (the "Common Stock"), par value $0.0001 per share. The Common Stock was sold pursuant to a prospectus supplement, filed on October 1, 2025 to the Registration Statement on Form S-3, originally filed on August 18, 2023 with the SEC (File No. 333-274073), and declared effective by the SEC on August 25, 2023. Net proceeds of the offering were $11,565,146, which is comprised of gross proceeds of $12,500,000 less Offering expenses of $934,854. The Offering closed on October 1, 2025.

Management and Board Changes

During 2025, the composition of the Company's Board of Directors changed. On April 12, 2025, Ms. Gioia Messinger notified the board of directors of her resignation from and decision to not stand for re-election for the board of directors, effective as of the date of the Annual Meeting on May 14, 2025 ("2025 Annual Meeting"). Her decision to resign from the board of directors was not related to any disagreement with the Company on any matter relating to its operations, policies, or practices.

On April 16, 2025, Mr. Joe Manko submitted a letter to the board of directors, resigning from the board of directors, effective April 16, 2025. In the resignation letter, Mr. Manko cited certain disagreements with the Company's governance practices and the composition and leadership of the board.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The following tables set forth our results of operations for the years ended December 31, 2025 and 2024, respectively, presented in dollars and as a percentage of revenue.

For the Year Ended December 31,
2025 | 2024
Revenue:
Product | 30,498,162 | 20,867,800
Customer funded development | 1,717,338 | 3,691,009
32,215,500 | 24,558,809
Cost of revenue:
Product | 15,353,945 | 19,913,178
Customer funded development | 879,072 | 4,022,707
16,233,017 | 23,935,885
Gross profit | 15,982,483 | 622,924
Operating expenses:
General and administrative | 7,357,357 | 7,203,628
Marketing and selling | 6,566,701 | 5,616,704
Research and development | 5,437,537 | 3,466,077
Total operating expenses | 19,361,595 | 16,286,409
Loss from operations | (3,379,112 | (15,663,485
Other income (expense), net:
Interest income | 278,788 | 477,745
Interest expense | (2,523 | (4,027
Other income, net | 16,309 | 24,040
Total other income, net | 292,574 | 497,758
Loss from continuing operations before income taxes | (3,086,538 | (15,165,727
Provision for income taxes | 11,310 | 2,560
Loss from continuing operations | (3,097,848 | (15,168,287
Income from discontinued operations, net of income taxes | 8,185,542 | 1,533,954
Net income (loss) | 5,087,694 | (13,634,333

For the Year Ended December 31,
2025 | 2024
Revenue:
Product | 94.7 | % | 85.0 | %
Customer funded development | 5.3 | % | 15.0 | %
100.0 | % | 100.0 | %
Cost of revenue:
Product | 47.7 | % | 81.1 | %
Customer funded development | 2.7 | % | 16.4 | %
50.4 | % | 97.5 | %
Gross profit | 49.6 | % | 2.5 | %
General and administrative | 22.8 | % | 29.3 | %
Marketing and selling | 20.4 | % | 22.9 | %
Research and development | 16.9 | % | 14.1 | %
Total operating expenses | 60.1 | % | 66.3 | %
Loss from operations | -10.5 | % | -63.8 | %
Other income (expense), net:
Interest income | 0.9 | % | 1.9 | %
Interest expense | 0.0 | % | 0.0 | %
Other income, net | 0.1 | % | 0.1 | %
Total other income, net | 0.9 | % | 2.0 | %
Loss from continuing operations before income taxes | -9.6 | % | -61.8 | %
Provision for income taxes | 0.0 | % | 0.0 | %
Loss from continuing operations | -9.6 | % | -61.8 | %
Income from discontinued operations, net of income taxes | 25.4 | % | 6.2 | %
Net income (loss) | 15.8 | % | -55.5 | %

Comparison of the Years Ended December 31, 2025 and 2024 from Continuing Operations:

Revenue

For the year ended December 31, 2025, our revenue increased $7,656,691, or 31.2%, as compared to the same period in 2024. This increase is primarily attributable to: 1) higher sales to the US Navy and a defense prime customer of data storage products to support the P-8A Poseidon Reconnaissance Aircraft; 2) higher sales to a defense end customer of custom server products, PCIe accelerators, and expansion products for a classified mobile intelligence platform; and 3) higher sales to a medical imaging OEM of liquid-cooled server products to support a breast cancer screening application. These increases were partially offset by lower sales to commercial aerospace customers as compared to the prior year.

Gross Profit and Gross Margin

Gross profit increased $15,359,559 for the year ended December 31, 2025 as compared to the same period in 2024. Gross margin percentage was 49.6% for 2025, compared to 2.5% for 2024. The improvement in gross margin was driven by 1) a more favorable mix of products shipped within 2025 and favorable pricing on new contracts entered into during 2025; 2) the non-recurrence of $7,088,114 of inventory adjustments and allowances recognized in 2024; 3) the non-recurrence of a $1,222,085 contract loss provision recognized in 2024 related to a customer-funded development contract entered into in 2022; and 3) more favorable manufacturing absorption within 2025 due to both production headcount reductions and a higher volume of production revenue.

Operating expenses

General and administrative expense

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-18_item1_business.md)

ITEM 1. B USINESS.

Company History

One Stop Systems, Inc. ("we," "our," "OSS," or the "Company") was originally incorporated as a California corporation in 1999, after initially being formed as a California limited liability company in 1998. On December 14, 2017, the Company was reincorporated as a Delaware corporation in connection with its initial public offering. The Company designs, manufactures, and markets specialized rugged high-performance compute ("HPC"), high speed switch fabrics, and storage systems, which are designed to target edge applications for artificial intelligence ("AI") / machine learning ("ML"), sensor processing, sensor fusion, and autonomy. The Company markets its products to manufacturers of equipment and platforms used for autonomous vehicles, medical, industrial, aerospace, and defense applications, with special focus on platforms that move, such as planes, unmanned aerial vehicles (UAVs), trucks, ships, submarines, and mobile datacenters or command posts where sensor processing, sensor fusion, AI, and ML are integrated to support such applications. If an application needs sensor processing, AI, and/or autonomous capabilities, and it moves, OSS aims to deliver the highest performance solutions that are designed to survive these challenging environments.

During the year ended December 31, 2015, the Company formed a wholly owned subsidiary in Germany, One Stop Systems, GmbH ("OSS GmbH"). Then, in July 2016, the Company acquired Mission Technologies Group, Inc. ("Magma") and its operations . Magma designed and manufactured PCIe expansion systems primarily for datacenter and business-to-professional consumer applications, such as the media and entertainment market.

On August 31, 2018, the Company acquired Concept Development Inc. ("CDI") located in Irvine, California. CDI specialized in the design and manufacture of custom high-performance computing systems for airborne in-flight entertainment, flight safety equipment, and networking systems. CDI's business was fully integrated into the core operations of the Company as of June 1, 2020.

On October 31, 2018, OSS GmbH acquired 100% of the outstanding stock of Bressner Technology GmbH, a limited liability company registered under the laws of Germany and located near Munich, Germany ("Bressner"). Bressner was an integrator and distributor of hardware systems and components.

On December 30, 2025, the Company signed and closed a definitive agreement to sell all Bressner through a sale of all shares of OSS GmbH. The consummation of this transaction represented a strategic shift and prioritization of the Company's core business developing and manufacturing deployable edge computing systems for mission critical applications.

Our principal executive offices are located at 2235 Enterprise Street, Suite 110, Escondido, California 92029, and our telephone number is (760) 745-9883. Our website address is www.onestopsystems.com. Information contained in, or accessible through, our website is for reference purposes only.

Business Overview

OSS designs, manufactures, and markets specialized enterprise class high-performance compute, high speed switch fabrics, and storage hardware and software, which are designed to target edge applications for AI/ML, sensor processing, sensor fusion, and autonomy. Edge computing is a form of computing that is done on platform or on site, connected with the data source or the user, rather than in the cloud, minimizing the need for data to be processed remotely. This growing trend increases computing performance and security, as the data does not have to travel to distant datacenter locations. Edge computing is most recognizable in applications such as sensor processing, sensor fusion, autonomy, and AI/ML. To meet the demands at the edge, we offer specialized products and system solutions that consist of computers, switch fabrics, and storage products that incorporate the latest state-of-the art components with embedded proprietary software. Such products and systems allow us to offer high-end solutions to be integrated into edge platforms in our target markets.

The fast-growing edge computing space consists of three major segments. The first segment is comprised of smaller datacenters located near the user - on the edge. These typically include compute and storage racks in environmentally controlled buildings, similar to large cloud datacenters. Suppliers in this space tend to be the same large server and storage manufacturers whose products are used at cloud datacenters. The second segment includes billions of Internet-of-Things ("IOT") devices that may reside in everything from home appliances to the factory

production floor. These IOT devices and applications tend not to be challenged on performance and easily communicate up to the cloud or the datacenters on the edge. OSS does not focus on either of the foregoing segments. The third segment is focused on edge platforms generally on the move or located in challenging environmental conditions. These edge platforms are primarily on land, in the air, or at sea on vehicles that need enterprise class datacenter level performance for sensor processing, sensor fusion, autonomy, and AI/ML applications. This is where OSS' vision and strategy is aligned, and where we believe that we offer the greatest unique value.

Examples of these applications range from industrial autonomous trucks, to mining equipment and smart agricultural equipment, to military land, sea, and airborne weapon system platforms. Less mobile applications that utilize High Performance Compute ("HPC") and edge computing include items such as medical applications, mobile command centers, and certain datacenters.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-18_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-18_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | **MISSING** |

**Present:** meta.json, form4_summary.md, 8-K_2026-05-08_2-02-results.md, 10-K_2026-03-18_item7_mdna.md, 10-K_2026-03-18_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
