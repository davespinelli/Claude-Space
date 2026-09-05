# Triage pack — CTKB · Cytek Biosciences, Inc.

_Generated 2026-09-05 02:09 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** CTKB · **Name:** Cytek Biosciences, Inc.
- **CIK:** 0001831915
- **SIC:** 3826 — Laboratory Analytical Instruments
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/CTKB

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Cytek Biosciences, Inc.
- **CIK:** 1,831,915 · **SIC:** 3826 (Laboratory Analytical Instruments) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 4.70 |
| mktcap | $610.9M |
| ev | $537.1M |
| ev_ebit | n/a |
| fcf | -$8.8M |
| fcf_yield | -1.4% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -12.9% |
| net_debt | -$73.8M |
| net_debt_ebit | n/a |
| cash | $73.8M |
| ltd | $0.00 |
| equity | $322.0M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $201.5M |
| revenue_prior | $200.5M |
| rev_growth | 0.5% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$40.4M |
| net_income | -$66.5M |
| cfo | -$4.7M |
| capex | $4.1M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 2.2% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 129,983,253 |
| shares_py | 127,223,778 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 6.1% |
| r6m | 7.3% |
| off_52w_high | -20.1% |
| adv20 | $3.7M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.17 |
| r_ev_ebit | 0.00 |
| r_roic | 0.10 |
| r_rev_growth | 0.36 |
| r_buyback | 0.32 |
| score | 0.24 |

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
| rank | 449 |

**Screen rationale:** debt data missing (net cash unverified); 12-1 momentum 6.1%


## 3. Share count trend

- Shares outstanding: **129,983,253** (CY2026Q2I) vs **127,223,778** prior year (CY2025Q2I)
- Change: **2.2%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-15** — Item 5.02 (officer / director change or comp arrangement): As previously disclosed, Valerie Barnett's position as Chief Legal Officer and Corporate Secretary of Cytek Biosciences, Inc. (the "Company") terminated on June 29, 2026.
- **2026-06-25** — Item 5.02 (officer / director change or comp arrangement): On June 18, 2026, Valerie Barnett and Cytek Biosciences, Inc. (the "Company") agreed that Ms. Barnett's position as Chief Legal Officer and Corporate Secretary of the Company would terminate effective as of June 29, 2026.
- **2026-06-02** — Item 5.02 (officer / director change or comp arrangement): On May 27, 2026, Philippe Busque, Ph.D. submitted his resignation from his position as the Senior Vice President, Global Sales and Services of Cytek Biosciences, Inc. (the "Company"), effective as of June 5, 2026, to pursue another career opportunity.

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 52 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 8 |
| F | 11 |
| G | 1 |
| M | 32 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-05_2-02-results.md)

_Extraction: started at the first release heading, 'Cytek Biosciences Reports Second Quarter 2026 Financial Results'; skipped 10 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (d118986dex991.htm)

Cytek Biosciences Reports Second Quarter 2026 Financial Results

FREMONT, Calif., August 5, 2026 (GLOBE NEWSWIRE) – Cytek Biosciences, Inc. ("Cytek Biosciences" or
"Cytek") (Nasdaq: CTKB), a leading cell analysis solutions company, today reported financial results for the second quarter ended June 30, 2026.

Recent Highlights

• | Total revenue for the second quarter of 2026 was $48.1 million, representing a 6% increase compared to the second quarter of 2025

• | Launched Cytek Borealis ™ , a new 7-laser full spectrum flow cytometer with new and proprietary reagents enabling high-resolution 60-color panels

• | Introduced Cytek Aurora ™ Evo instrument configurations with expanded automation capabilities for highly automated lab environments

• | Total recurring revenue, comprised of service and reagent revenues, reached $18.5 million in the second quarter. On a trailing-12-month basis, recurring revenue represented 35% of total revenue, up from 32% on a trailing-12-month basis as of the second quarter of 2025

• | Expanded to a total installed base of 3,933 Cytek instruments, adding 142 units in the second quarter of 2026

• | Updates full year 2026 total revenue guidance to $207 million to $212 million, raising the midpoint by $1 million

"Our second quarter results reflect continued execution against our strategic priorities, exemplified by strong
double-digit revenue growth in instruments in the U.S. and in China and ongoing and consistent expansion of our service business," said Wenbin Jiang, CEO of Cytek Biosciences. "Looking ahead, our priorities remain clear: accelerating
adoption of our instrument platforms, including newly launched instruments, expanding recurring revenue business and extending our technology leadership. We believe our investments in products, people, and operations position Cytek well for the
remainder of 2026 and the long-term opportunity ahead."

Second Quarter 2026 Financial Results

Total revenue for the second quarter of 2026 was $48.1 million, a 6% increase compared to the second quarter of 2025. The increase in revenue was driven
by strong instrument growth in the U.S. and in China, and continued growth in service.

GAAP gross profit was $28.3 million for the second quarter of
2026, a 19% increase compared to the second quarter of 2025. GAAP gross profit margin was 59% in the second quarter of 2026 compared to 52% in the second quarter of 2025. Adjusted gross profit margin, after adjusting for stock-based compensation
expense and amortization of acquisition-related intangibles, was 61% in the second quarter of 2026 compared to 56% in the second quarter of 2025. Excluding the impact of a one-time tariff refund, GAAP and
adjusted gross margin in the second quarter of 2026 were 53% and 56%, respectively.

Operating expenses were $39.7 million for the second quarter of 2026, a 15% increase compared to the
second quarter of 2025 due to increased research and development, sales and marketing, and general and administrative expenses.

Research and development
expenses were $9.7 million for the second quarter of 2026, a 10% increase compared to the second quarter of 2025.

Sales and marketing expenses were
$13.2 million for the second quarter of 2026, a 9% increase compared to the second quarter of 2025.

General and administrative expenses were
$16.8 million for the second quarter of 2026, a 24% increase compared to the second quarter of 2025 due to litigation-related expenses, severance and personnel costs.

Loss from operations in the second quarter of 2026 was $11.4 million compared to loss from operations of $10.6 million in the second quarter of
2025. Net loss in the second quarter of 2026 was $12.2 million compared to a net loss of $5.6 million in the second quarter of 2025.

Adjusted
EBITDA loss in the second quarter of 2026 was $1.5 million compared to positive adjusted EBITDA of $1.3 million in the second quarter of 2025, after adjusting for stock-based compensation expense, foreign currency exchange impacts and a write-off of an investment in an early-stage technology company.

Cash, cash equivalents and marketable securities
totaled $262.0 million as of June 30, 2026, compared to $262.2 million as of March 31, 2026, a decrease of $0.2 million.

2026
Outlook

Cytek Biosciences is updating its revenue outlook for the full year 2026 to be in the range of $207 million to $212 million, raising
the midpoint by $1 million, assuming no change in current foreign currency exchange rates.

Webcast Information

Cytek will host a conference call to discuss its second quarter 2026 financial results on Wednesday, August 5, 2026, at 1:30 p.m. Pacific Time / 4:30 p.m.
Eastern Time. A webcast of the conference call can be accessed at investors.cytekbio.com.

About Cytek Biosciences, Inc.

Cytek Biosciences (Nasdaq: CTKB) is a leading cell analysis solutions company advancing the next generation of cell analysis tools by delivering
high-resolution, high-content and high-sensitivity cell analysis utilizing its patented Full Spectrum Profiling ™ (FSP ® ) technology.
Cytek's novel approach harnesses the power of information within the entire spectrum of a fluorescent signal to achieve a higher level of multiplexing with precision and sensitivity. Cytek's platform includes: its core FSP instruments,
the Cytek Aurora ™ , Northern Lights ™ , Cytek Aurora ™ CS and Cytek Aurora ™ Evo systems; the Cytek Orion ™ reagent cocktail preparation system; the Enhanced Small Particle ™ (ESP ™ ) detection technology; the flow cytometers and imaging products under the
Amnis ® and Guava ® brands; and reagents, software and services to provide a comprehensive and integrated suite of solutions
for its customers. Cytek is headquartered in Fremont, California with offices and distribution channels across the globe. More information about the company and its products is available at www.cytekbio.com.

Cytek's products are for research use only and not for use in diagnostic procedures (other than
Cytek's Northern Lights-CLC system and certain reagents, which are available for clinical use only in China and the European Union).

Cytek, Full Spectrum Profiling, FSP, Cytek Aurora, Cytek Borealis, Northern Lights, Enhanced Small Particle, ESP, Cytek Orion, Amnis and Guava are trademarks
of Cytek Biosciences, Inc.

In addition to filings with the Securities and Exchange Commission (SEC), press releases, public conference calls and
webcasts, Cytek uses its website (www.cytekbio.com), LinkedIn page and X account as channels of distribution for information about the company, its products, planned financial and other announcements, attendance at upcoming investor and industry
conferences and other matters. Certain information disseminated through these channels may be material to investors, and Cytek may use these channels to disseminate such information in accordance with Regulation FD and other applicable disclosure
requirements. Therefore, investors should monitor Cytek's website, LinkedIn page, and X account in addition to following its SEC filings, news releases, public conference calls and webcasts.

Statement Regarding Use of Non-GAAP Financial Information

Cytek has presented certain financial information in accordance with generally accepted accounting principles in the United States ("U.S. GAAP")
and also on a non-GAAP basis for the three-month period ended June 30, 2026 and June 30, 2025. Management believes that non-GAAP financial measures, including
"Adjusted gross profit," "Adjusted gross profit margin," "Adjusted EBITDA" and "Adjusted EBITDA excluding investment income," referenced in this release, taken in conjunction with GAAP financial
measures, provide useful information for both management and investors by excluding certain non-cash and other expenses that are not indicative of the company's core operating results. Management uses non-GAAP measures to compare the company's performance relative to forecasts and strategic plans and to benchmark the company's performance externally against competitors.
Non-GAAP information is not prepared under a comprehensive set of accounting rules and should only be used to supplement an understanding of the company's operating results as reported under U.S. GAAP.
Cytek encourages investors to carefully consider its results under GAAP, as well as its supplemental non-GAAP information and the reconciliation between these presentations, to more fully understand its
business. Reconciliations between GAAP and non-GAAP operating results are presented in the accompanying tables of this release.

Cytek Biosciences

mmeehan@cytekbio.com

Cytek Biosciences, Inc.

Consolidated Balance Sheets

(Unaudited)

(In thousands, except share and per share data) | June 30, 2026 | December 31, 2025
Assets
Current assets:
Cash and cash equivalents | 73,846 | 90,853
Marketable securities | 188,158 | 170,676
Trade accounts receivable, net | 49,698 | 62,509
Inventories | 52,251 | 48,428
Prepaid expenses and other current assets | 13,978 | 19,530
Total current assets | 377,931 | 391,996
Property and equipment, net | 20,801 | 18,009
Operating lease right-of-use assets | 10,962 | 11,315
Goodwill | 16,690 | 16,697
Intangible assets, net | 14,865 | 16,821
Other noncurrent assets | 5,685 | 6,704
Total assets | 446,934 | 461,542
Liabilities and stockholders' equity
Current liabilities:
Trade accounts payable | 8,408 | 6,410
Legal settlement liability, current | 2,353 | 2,495
Accrued expenses | 23,855 | 23,417
Other current liabilities | 20,513 | 16,978
Deferred revenue, current | 29,206 | 28,504
Total current liabilities | 84,335 | 77,804
Legal settlement liability, noncurrent | 6,368 | 6,786
Deferred revenue, noncurrent | 18,058 | 18,339
Operating lease liability, noncurrent | 13,517 | 14,042
Long-term debt | 246 | 525
Other noncurrent liabilities | 2,456 | 2,307
Total liabilities | 124,980 | 119,803
Stockholders' equity:
Common stock, $0.001 par value; 1,000,000,000 authorized shares as of June 30, 2026 and December 31, 2025, respectively; 129,982,753 and 128,550,136 issued and outstanding shares as of June 30, 2026 and December 31, 2025, respectively | 130 | 129
Additional paid-in capital | 451,846 | 441,107
Accumulated deficit | (132,761 | (101,738
Accumulated other comprehensive income | 2,739 | 2,241
Total stockholders' equity | 321,954 | 341,739
Total liabilities and stockholders' equity | 446,934 | 461,542

Cytek Biosciences, Inc.

Consolidated Statements of Operations and Comprehensive Loss

(Unaudited)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-26_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We are a leading cell analysis solutions company advancing the next generation of research and clinical tools with our novel technical approach of leveraging the full spectrum of fluorescence signatures from multiple lasers to distinguish fluorescent tags on single cells ("Full Spectrum Profiling" or "FSP" technology). Our goal is to become the premier cell analysis company through continued innovation that facilitates scientific advances in biomedical research and clinical applications. Our FSP platform includes instruments, accessories, reagents, software and services to provide a comprehensive and integrated suite of solutions for our customers.

Our FSP cell analyzers, the Cytek Aurora, Northern Lights and Cytek Aurora Evo systems, deliver high-resolution, high-content and high-sensitivity cell analysis and addresses the inherent limitations of other technologies by providing a higher level of multiplexing with exquisite sensitivity, more flexibility and increased efficiency, all at a lower cost for performance. Additionally, our Cytek Aurora cell sorter ("Aurora CS system") leverages our FSP technology to further broaden our potential applications across cell analysis. Each system is supported by our highly intuitive, proprietary embedded SpectroFlo software, our reagents, and our service offerings to provide a comprehensive, end-to-end platform of solutions for our customers. Since our first U.S. commercial launch in mid-2017, we have sold and deployed our instruments to customers around the world, including pharmaceutical companies, biopharma companies, academic research centers, and contract research organizations ("CROs").

In addition to our FSP product portfolio, pursuant to an acquisition in February 2023, we offer conventional flow and image-based flow cytometry instrumentation and related products and services under the Amnis ® and Guava ® brands, which provide insights into all facets of cellular phenotypes and morphology. Amnis instruments and applications are important tools in the investigation of cell morphology, intracellular translocation and cell-cell interaction in a variety of research areas, including immunology, neurobiology, stem cell research and cell biology. Guava flow cytometers expand our core instrument offerings, adding cost-effective, entry-level and personal instrument options with microcapillary-based fluidics for cell analysis. The Guava microcapillary-based flow cytometers are mainly adopted by entry to mid-range flow cytometry users who are looking for easy-to-use and cost-effective solutions for applications, such as cell counting, cell biology and lower-plex immunophenotyping.

We manufacture our instruments in our facilities in Fremont, California; Wuxi, China; and Singapore. We have designed our operating model to be capital efficient and to scale efficiently as our product volumes grow.

Total revenue for the year ended December 31, 2025 was $201.5 million , representing a 1% increase compared to revenue for the year ended December 31, 2024 of $200.5 million.

To date, we have adopted a direct sales model in North America, Europe, China, and several other countries in the Asia-Pacific region, and sell our products through third-party distributors in certain countries in Europe, Latin America, the Middle East, Africa and the Asia-Pacific region. Revenue from direct sales represented 73% , 75% and 76% of total revenue for the years ended December 31, 2025, 2024 and 2023, respectively, and revenue from distributors represented 27% , 25% and 24% of total revenue for the years ended December 31, 2025, 2024 and 2023, respectively.

We focus a substantial portion of our resources on developing new products and solutions to meet our customers' needs. Our research and development efforts focus on developing new and complementary instruments, reagents and reagent kits, and continued operating software development. We incurred research and development expenses of $36.5 million, $39.4 million and $44.2 million for the years ended December 31, 2025, 2024 and 2023, respectively. We intend to continue to make significant investments in research and development in the future.

We expect to continue to invest in our commercial infrastructure through hiring additional employees with strong scientific and technical backgrounds to support growth in our instrument sales as well as our planned expansion of reagents offerings and panel design capabilities. We also plan to continue to invest in sales, marketing and business development across the globe to drive commercialization of our products. We incurred sales and marketing expenses of $49.4 million, $49.1 million and $49.1 million for the years ended December 31, 2025, 2024 and 2023, respectively.

Since our inception in 2014, we have financed our operations primarily through sales of our securities and revenue from the sale of our products and services.

Our net loss was $66.5 million , $6.0 million and $12.1 million f or the years ended December 31, 2025, 2024 and 2023, respectively. The change for the year ended December 31, 2025, compared to the year ended December 31, 2024, was primarily driven by the recording of a $33.1 million valuation allowance against deferred tax assets in 2025. In addition, lower gross profit, increased operating expenses, and an operating and interest expense reduction related to a change in estimate of a license and royalty settlement liability in 2024, contributed to the overall year-over-year change.

We expect our expenses will increase substantially in connection with our ongoing activities, as we:

• attract, hire and retain qualified personnel;

• invest in processes, commercial infrastructure and supporting functions to scale our business and introduce new products and services;

• support our research and development efforts;

• continue to expand geographically;

• protect and defend our intellectual property; and

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of operations

Comparison of the years ended December 31, 2025 and 2024

The results of operations presented below should be reviewed in conjunction with the consolidated financial statements and related notes included elsewhere in this Annual Report on Form 10-K.

The following table sets forth our consolidated results of operations and comprehensive (loss) income data for the periods presented:

Year ended December 31,
(In thousands) | 2025 | 2024
Revenue, net:
Product | 144,233 | 153,263
Service | 57,260 | 47,190
Total revenue, net | 201,493 | 200,453
Cost of sales:
Product | 69,813 | 69,088
Service | 27,220 | 20,259
Total cost of sales | 97,033 | 89,347
Gross profit | 104,460 | 111,106
Operating expenses:
Research and development | 36,468 | 39,402
Sales and marketing | 49,440 | 49,114
General and administrative | 58,936 | 43,113
Total operating expenses | 144,844 | 131,629
Loss from operations | (40,384) | (20,523)
Other income (expense):
Interest income (expense), net (Notes 11, 12) | (474) | 5,239
Interest income | 2,216 | 5,121
Other income, net | 8,801 | 4,463
Total other income, net | 10,543 | 14,823
Loss before income taxes | (29,841) | (5,700)
Provision for (benefit from) income taxes | 36,698 | 320
Net loss | (66,539) | (6,020)
Foreign currency translation adjustment, net of tax | 2,167 | 1,193
Unrealized gain (loss) on marketable securities | 58 | 97
Net comprehensive loss | (64,314) | (4,730)

Total revenue, net

Year ended December 31, | Change
(In thousands, except percentages) | 2025 | 2024 | Amount | %
Revenue, net
Product | 144,233 | 153,263 | (9,030) | (6) | %
Service | 57,260 | 47,190 | 10,070 | 21 | %
Total revenue, net | 201,493 | 200,453 | 1,040 | 1 | %

Total revenue, net increased by $1.0 million, or 1%, for the year ended December 31, 2025 as compared to the year ended December 31, 2024. Revenue growth was primarily driven by growth in service revenue partially offset by a decline in product revenue.

Product revenue decreased by $9.0 million, or 6%, to $144.2 million, for the year ended December 31, 2025 as compared to the year ended December 31, 2024. The decrease was primarily driven by a decline in instrument revenue offset by growth in reagent revenue. Unit volumes decreased 6.0% for spectral and imaging products, including the Cytek Aurora, Northern Lights, Aurora CS and ImageStream systems.

Service revenue increased by $10.1 million, or 21%, to $57.3 million, for the year ended December 31, 2025 as compared to the year ended December 31, 2024. The increase in service revenue was mainly driven by continued growth in

the installed base of our instruments with more instruments with expiring warranties contributing to greater contract and time and material service revenue.

Total cost of sales, gross profit and gross margin

Year ended December 31, | Change
(In thousands, except percentages) | 2025 | 2024 | Amount | %
Cost of sales:
Product | 69,813 | 69,088 | 725 | 1 | %
Service | 27,220 | 20,259 | 6,961 | 34 | %
Total cost of sales | 97,033 | 89,347 | 7,686 | 9 | %
Gross profit | 104,460 | 111,106 | (6,646) | (6) | %
Gross margin | 52 | % | 55 | %

Total cost of sales increased by $7.7 million, or 9%, for the year ended December 31, 2025 as compared to the year ended December 31, 2024. The increase in cost of sales was driven primarily by an increase in service revenue, and associated service material, headcount, and other overhead costs. Product cost of sales increased due to higher tariff costs and higher overhead costs resulting from transitioning a manufacturing facility overseas, offset by lower material costs as a result of lower instrument volume.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-26_item1_business.md)

PART I.

Item 1. Business

Overview

We are a leading cell analysis solutions company advancing the next generation of research and clinical tools with our novel technical approach of leveraging the full spectrum of fluorescence signatures from multiple lasers to distinguish fluorescent tags on single cells ("Full Spectrum Profiling" or "FSP" technology). Our goal is to become the premier cell analysis company through continued innovation that facilitates scientific advances in biomedical research and clinical applications.

Biological systems are highly complex, and scientists are challenged by the multitude of questions that remain unanswered. Analysis at the single-cell level is essential to understand these complex systems. Identifying the correct cell in the context of a given biological question can have profound implications for drug development and health care decisions. It is essential to correlate information derived from multiple cell analysis approaches and to translate what is known at the gene level to the actual cell function. As a result, there is growing demand for deep content through high dimensional cell analysis and for solutions that can provide a complete picture of cellular biological processes and interactions. To achieve this, scientists need to phenotype and isolate rare events or unique populations down to the single-cell level through highly resolvable multi-dimensional cell analysis. While flow cytometry is a widely used tool for single cell analysis, conventional flow cytometry, mass cytometry and early approaches to spectral flow cytometry technologies have historically been challenged due to limited dimensionality, sub-optimal resolution, low throughput, high cost for performance and/or significant technical expertise required to operate systems.

Full Spectrum Profiling™ (FSP ® ) Technology

Our patented FSP technology optimizes sensitivity and accuracy through its unique optical and electronic designs that utilize an innovative method of light detection and distribution to a specifically selected number and type of detectors. This patented optics design enables researchers to effectively collect the full range of light emissions in an extremely compact space, resulting in higher resolution and enabling the development of highly complex assays with 50 different colors (individual fluorochromes), supporting 50 biomarkers within just a single tube.

Our FSP cell analyzers, the Cytek Aurora™, Northern Lights™, and Cytek Aurora Evo systems, deliver high-resolution, high-content and high-sensitivity cell analysis and address the inherent limitations of other technologies by providing a higher level of multiplexing with exquisite sensitivity, more flexibility and increased efficiency, all at a lower cost for performance. Additionally, our Cytek Aurora cell sorter ("Aurora CS system") leverages our FSP technology to further broaden our potential applications across cell analysis by enabling the same number of parameters with the same sensitivity as the Cytek Aurora and Cytek Aurora Evo cell analyzer systems. Each system is supported by our highly intuitive, proprietary embedded SpectroFlo ® software, our reagents, and our service offerings to provide a comprehensive, end-to-end platform of solutions for our customers.

Since our first U.S. commercial launch in mid-2017, we have sold and deployed our instruments to customers around the world, including pharmaceutical companies, biopharma companies, academic research centers, and contract research organizations ("CROs"). Our solutions have enabled researchers to make significant scientific advances in key areas of medical discovery (such as oncology, immunology and infectious diseases) in addition to empowering improved downstream cell analysis with complementary cell analysis technologies (such as next-generation sequencing ("NGS")). We believe that our innovative FSP and targeted cell isolation technology has the potential to accelerate scientific discovery and have a profound impact on the understanding of cell biology, immunotherapy, and targeted therapeutic approaches (personalized medicine). Further, there has been a meaningful number of publications generated to showcase our technology, with more than 3,500 peer-reviewed articles published relating to our FSP products since our first commercial launch in 2017, including many prominent journals, across a wide range of applications including oncology, infectious diseases, immunology, immunotherapy and immuno-oncology.

Our FSP platform was purpose-built to advance the next generation of cell analysis by delivering deep insights, high-throughputs and ease-of-use. Our FSP platform is designed to offer the following key benefits:

• Ultra-sensitive: resolve the most challenging cell populations (such as cells with high autofluorescence or low levels of expression of key biomarkers) by providing high-resolution data at the single-cell level with an optimized signal-to-noise ratio.

• Deep, high integrity content: allow development of highly complex assays through access to 50 different colors and, thus, supporting 50 biomarkers in a single tube without sacrificing precision and throughput to gain a deeper understanding of biological systems and arrive at faster and more accurate diagnoses in clinica l settings.

• Flexible and compatible: enable a single configuration across a wide range of reagents and applications, full backwards compatibility across panels, and greater leverage for downstream analysis with complementary technologies, including NGS.

• Efficient and compact: improve costs and save time while maintaining industry-leading performance and efficient workflows that limit consumables usage and reduce labor costs—all within a highly compact footprint minimizing space requirements for laboratories.

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
