# Triage pack — CNXC · Concentrix Corp

_Generated 2026-09-05 08:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** CNXC · **Name:** Concentrix Corp
- **CIK:** 0001803599
- **SIC:** 7389 — Services-Business Services, NEC
- **Fiscal year end (MM-DD):** 11-30
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/CNXC

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Concentrix Corp
- **CIK:** 1,803,599 · **SIC:** 7389 (Services-Business Services, NEC) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 32.16 |
| mktcap | $2.0B |
| ev | $5.6B |
| ev_ebit | n/a |
| fcf | $572.5M |
| fcf_yield | 29.2% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -11.4% |
| net_debt | $3.7B |
| net_debt_ebit | n/a |
| cash | $255.6M |
| ltd | $3.9B |
| equity | $2.7B |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $9.8B |
| revenue_prior | $9.6B |
| rev_growth | 2.2% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$918.2M |
| net_income | -$1.3B |
| cfo | $807.0M |
| capex | $234.5M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -3.2% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 61,018,350 |
| shares_py | 63,025,120 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -47.4% |
| r6m | -5.7% |
| off_52w_high | -41.0% |
| adv20 | $32.7M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.95 |
| r_ev_ebit | 0.00 |
| r_roic | 0.11 |
| r_rev_growth | 0.42 |
| r_buyback | 0.82 |
| score | 0.46 |

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
| rank | 281 |

**Screen rationale:** top-quartile FCF yield 29.2%; buying back stock -3.2%


## 3. Share count trend

- Shares outstanding: **61,018,350** (CY2026Q2I) vs **63,025,120** prior year (CY2025Q2I)
- Change: **-3.2%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-24** — Item 5.02 (officer / director change or comp arrangement): On July 23, 2026, the Board of Directors (the "Board") of Concentrix Corporation (the "Company") adopted an Amended and Restated Executive Severance Plan (the "Amended Plan") to amend and replace the Company's Change of Control Severance Plan.
- **2026-05-01** — Item 5.02 (officer / director change or comp arrangement): Under the terms of the Investor Rights Agreement, dated as of March 29, 2023 (the "Investor Rights Agreement"), by and among Concentrix Corporation (the "Company") and certain former stockholders of Marnix Lux SA, a public limited liability company ( société...
- **2026-03-27** — Item 5.02 (officer / director change or comp arrangement): As described below in Item 5.07 of this Current Report on Form 8-K, on March 25, 2026, the stockholders of Concentrix Corporation (the "Company") approved an amendment (the "Amendment") to the Concentrix Corporation Amended and Restated 2020 Stock Incentive...
- **2026-03-23** — Item 1.01 (Entry into a Material Definitive Agreement): On March 20, 2026, Concentrix Corporation (the "Company"), as servicer, entered into an amendment (the "Amendment") to its accounts receivable securitization facility (as amended, the "Securitization Facility") by and among Concentrix Receivables, Inc., a...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 4,500 sh / $118,089 vs sells 6,000,000 sh / $133,500,000 -> net $-133,381,911 (SELLING).
Distinct insiders buying (code P): 2. Largest buy: Valentine Andre S bought 2,500 sh @ $27.95 ($69,869) on 2026-04-09.

Form 4 filings parsed: 12; transaction rows: 12 (open-market buys 3, sales 1).

| code | rows |
|---|---|
| A | 8 |
| P | 3 |
| S | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-06-29_2-02-results.md)

_Extraction: started at the first release heading, 'Concentrix Reports Second Quarter 2026 Results'; skipped 9 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (exhibit991q22026.htm)

Concentrix Reports Second Quarter 2026 Results

• Revenue and profit within guidance as reported

• A record-high second quarter $258M in cash flow from operations, $242M in adjusted free cash flow

• iX Suite deals up 400% year over year

Newark, Calif., June 29, 2026 – Concentrix Corporation (NASDAQ: CNXC), a global technology and services leader, today announced financial results for the fiscal second quarter ended May 31, 2026.

Three Months Ended
May 31, 2026 | May 31, 2025 | Change
Revenue ($M) | 2,462.5 | 2,417.4 | 1.9 | %
Operating income ($M) | 95.4 | 148.3 | (35.7) | %
Non-GAAP operating income ($M) (1) | 292.0 | 303.7 | (3.9) | %
Operating margin | 3.9 | % | 6.1 | % | -220 bps
Non-GAAP operating margin (1) | 11.9 | % | 12.6 | % | -70 bps
Net income ($M) | 55.3 | 42.1 | 31.4 | %
Non-GAAP net income ($M) (1) | 168.6 | 179.6 | (6.1) | %
Adjusted EBITDA ($M) (1) | 347.4 | 357.3 | (2.8) | %
Adjusted EBITDA margin (1) | 14.1 | % | 14.8 | % | -70 bps
Diluted earnings per common share | 0.86 | 0.63 | 36.5 | %
Non-GAAP diluted earnings per common share (1) | 2.63 | 2.70 | (2.6) | %

(1) See non-GAAP reconciliations included in the accompanying financial tables for the reconciliation of each non-GAAP measure to its most directly comparable GAAP measure.

Second Quarter Fiscal 2026 Highlights:

• Revenue of $2,462.5 million, an increase of 1.9% year-on-year on an as reported basis compared to revenue of $2,417.4 million in the prior year second quarter. The Company grew revenue 0.6% year-on-year on a constant currency basis.

• Operating income of $95.4 million, or 3.9% of revenue, compared to $148.3 million, or 6.1% of revenue, in the prior year second quarter.

• Non-GAAP operating income of $292.0 million, or 11.9% of revenue, compared with $303.7 million, or 12.6% of revenue in the prior year second quarter.

• Adjusted EBITDA of $347.4 million, or 14.1% of revenue, compared with $357.3 million, or 14.8% of revenue in the prior year second quarter.

• Cash flow provided by operations was $257.9 million in the quarter. Adjusted free cash flow (1) was $242.3 million in the quarter.

• Diluted earnings per common share ("EPS") was $0.86 compared to $0.63 in the prior year second quarter.

• Non-GAAP diluted EPS was $2.63 compared to $2.70 in the prior year second quarter.

"Our second quarter marked an acceleration in many areas in the evolution of our business," said Chris Caldwell, President and CEO of Concentrix. "Our blended AI and services approach is delivering value to clients by lowering their costs and increasing their revenue, helping us differentiate ourselves in the marketplace."

Quarterly Dividend and Share Repurchase Program:

• The Company paid a $0.36 per share quarterly dividend on May 5, 2026. The Company's Board of Directors has declared a quarterly dividend of $0.36 per share payable on August 4, 2026, to shareholders of record at the close of business on July 24, 2026.

• The Company did not repurchase any shares under its share repurchase program during the second quarter of fiscal year 2026. At May 31, 2026, the Company's remaining share repurchase authorization was $396.6 million.

Business Outlook:

The following statements are based on the Company's current expectations for the third quarter and the full year fiscal 2026. Non-GAAP financial measures exclude the impact of acquisition-related, integration and restructuring expenses, amortization of intangible assets, depreciation, loss on held for sale, share-based compensation and the related tax effects thereon. The non-GAAP EPS guidance assumes no impact from changes in acquisition contingent consideration and foreign currency losses (gains), net included in other expense (income), net. These statements are forward-looking and actual results may differ materially.

Third Quarter Fiscal 2026 Expectations:

• Third quarter reported revenue of $2.465 billion to $2.490 billion. Based on current exchange rates, these expectations assume an approximate 75-basis point negative impact of foreign exchange rates compared with the prior year period. The guidance implies constant currency revenue growth for the quarter ranging from 0.0% to 1.0%.

• Operating income of $121 million to $131 million and non-GAAP operating income of $295 million to $305 million.

• Non-GAAP diluted EPS of $2.65 to $2.77, assuming approximately 60.9 million diluted common shares outstanding and approximately 4.8% of net income attributable to participating securities.

• The effective tax rate is expected to be approximately 25%.

Full Year 2026 Expectations:

• Full year reported revenue of $9.925 billion to $10.025 billion. Based on current exchange rates, these expectations assume an approximate 75-basis point positive impact of foreign exchange rates compared with the prior year. The guidance implies constant currency revenue growth for the full year of 0.25% to 1.25%.

• Operating income of $509 million to $539 million and non-GAAP operating income of $1,200 million to $1,230 million.

• Non-GAAP diluted EPS of $10.83 to $11.18, assuming approximately 61.1 million diluted common shares outstanding and approximately 4.8% of net income attributable to participating securities.

• The effective tax rate is expected to be approximately 24.5%.

In addition, the Company expects to generate approximately $630.0 million to $650.0 million of adjusted free cash flow in fiscal year 2026.

The Company believes that a quantitative reconciliation of the non-GAAP EPS outlook to the most directly comparable GAAP measure cannot be provided without unreasonable efforts due to (a) the inability to forecast future changes in acquisition contingent consideration, which is based, in part, on the future trading price of the Company's common stock, and (b) the inability to forecast future foreign currency losses (gains), net included in other expense (income), net. For the same reason, the Company is unable

to address the probable significance of the unavailable information, which may have a material impact on the Company's GAAP results.

The Company believes that a quantitative reconciliation of the adjusted free cash flow outlook to the most directly comparable GAAP measure cannot be provided without unreasonable efforts due to uncertainty related to the future changes in the Company's factoring program and related timing of those changes. For the same reason, the Company is unable to address the probable significance of the unavailable information, which may have a material impact on the Company's GAAP results.

Conference Call and Webcast

The Company will host a conference call for investors to review its second quarter fiscal 2026 results today at 5:00 p.m. (ET)/2:00 p.m. (PT).

The live conference call webcast will be available in listen-only mode in the Investor Relations section of the Company's website under "Events and Presentations" at https://ir.concentrix.com/events-and-presentations. A replay will also be available on the website following the conference call.

About Concentrix: Powering a World That Works

Concentrix Corporation (NASDAQ: CNXC), is the Fortune 500® technology and services company, helping the world's best brands create intelligent operations that perform in the real world. We design, build, and run integrated human and AI solutions, harnessing the insight from billions of real-world interactions to help 2,000+ of the world's most complex organizations solve their toughest business challenges. Backed by 20+ years of operational experience and battle tested AI, we're the intelligent transformation partner that helps clients across every major industry move from ambition to measurable, scalable performance. Virtually everywhere. To learn more, visit concentrix.com.

Use of Non-GAAP Information

In addition to disclosing financial results that are determined in accordance with GAAP, we also disclose certain non-GAAP financial information, including:

• Constant currency revenue growth, which is revenue growth adjusted for the translation effect of foreign currencies so that certain financial results can be viewed without the impact of fluctuations in foreign currency exchange rates, thereby facilitating period-to-period comparisons of our business performance. Constant currency revenue growth is calculated by translating the revenue of each fiscal year in the billing currency to U.S. dollars using the comparable prior year's currency conversion rate in comparison to prior year's revenue. Generally, when the U.S. dollar either strengthens or weakens against other currencies, revenue growth at constant currency rates or adjusting for currency will be higher or lower than revenue growth reported at actual exchange rates.

• Non-GAAP operating income, which is operating income, adjusted to exclude acquisition-related, integration and restructuring expenses, step-up depreciation, amortization of intangible assets, loss on held for sale and share-based compensation.

• Non-GAAP operating margin, which is non-GAAP operating income, as defined above, divided by revenue.

• Adjusted earnings before interest, taxes, depreciation, and amortization, or adjusted EBITDA, which is non-GAAP operating income, as defined above, plus depreciation (exclusive of step-up depreciation).

• Adjusted EBITDA margin, which is adjusted EBITDA, as defined above, divided by revenue.

• Non-GAAP net income, which is net income excluding the tax-effected impact of acquisition-related, integration and restructuring expenses, step-up depreciation, amortization of intangible assets, loss on held for sale, share-based compensation, certain debt costs, imputed interest related to the Sellers' Note, certain legal settlement costs, change in acquisition contingent consideration and foreign currency losses (gains), net. Non-GAAP net income also excludes the income tax effect of certain tax law changes.

• Free cash flow, which is cash flows from operating activities less capital expenditures, and adjusted free cash flow, which is free cash flow excluding the effect of changes in the outstanding factoring balance. We believe that free cash flow is a meaningful measure of cash flows since capital expenditures are a necessary component of ongoing operations. We believe that adjusted free cash flow is a meaningful measure of cash flows because it removes the effect of factoring which changes the timing of the receipt of cash for certain receivables. However, free cash flow and adjusted free cash flow have limitations because they do not represent the residual cash flow available for discretionary expenditures. For example, free cash flow and adjusted free cash flow do not incorporate payments for business acquisitions.

• Non-GAAP diluted EPS, which is diluted EPS excluding the per share, tax-effected impact of acquisition-related, integration and restructuring expenses, step-up depreciation, amortization of intangible assets, loss on held for sale, share-based compensation, certain debt costs, imputed interest related to the Sellers' Note, certain legal settlement costs, change in acquisition contingent consideration and foreign currency losses (gains), net. Non-GAAP EPS also excludes the per share income tax effect of certain tax law changes. Non-GAAP EPS also reflects a per share adjustment to exclude non-GAAP net income attributable to participating securities.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-01-28_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview and Basis of Presentation

Concentrix is a global technology and services leader that powers exceptional brand experiences and digital operations for more than 2,000 clients across the globe. We design, build, and run fully integrated, end-to-end solutions, including customer experience ("CX") process optimization, technology innovation and design engineering, front- and back-office automation, analytics, and business transformation services to clients in five primary industry verticals. Our differentiated portfolio of solutions supports Fortune Global 500 clients across the globe in their efforts to deliver an optimized, consistent brand experience across all channels of communication, including voice, chat, email, GenAI- and agentic AI-powered self-service, social media, asynchronous messaging, and custom applications. We strive to deliver exceptional services globally supported by our deep industry knowledge, technology and security practices, talented people, and digital and analytics expertise.

We generate revenue from performing services and providing technology that is generally tied to our clients' products and services. Any shift in business, demand, or the size of the market for our clients' products or services, or any failure of technology or failure of acceptance of our clients' products or services in the market may impact our business. The staff turnover rate in our business is high, as is the risk of losing experienced team members. High staff turnover rates may increase costs and decrease operating efficiencies and productivity. For more information on the risks associated with our business, please see "Risk Factors" in this Annual Report on Form 10-K.

Webhelp Combination

On September 25, 2023, we completed our acquisition (the "Webhelp Combination") of all of the issued and outstanding capital stock (the "Shares") of Marnix Lux SA ("Webhelp"), from the holders thereof (the "Sellers"). The purchase consideration for the acquisition of the Shares was valued at approximately $3,774.8 million, net of cash and restricted cash acquired.

Revenue and Cost of Revenue

We generate revenue through the provision of technology and services to our clients pursuant to client contracts. Our client contracts typically consist of a master services agreement, supported in most cases by multiple statements of work, which contain the terms and conditions of each contracted solution. Our client contracts can range from less than one year to over five years in term and are subject to early termination by our clients for any reason, typically with 30 to 90 days' notice.

Our technology and services are generally characterized by flat unit prices. Approximately 99% of our revenue is recognized as services are performed, based on staffing hours or the number of client customer transactions handled using contractual rates. Remaining revenue from the sale of these solutions are typically recognized as the services are provided over the duration of the contract using contractual rates.

Our cost of revenue consists primarily of personnel costs related to the delivery of our technology and services. The costs of our revenue can be impacted by the mix of client contracts, where we deliver the technology and services, additional lead time for programs to be fully scalable, and transition and initial set-up costs. Our cost of revenue as a percentage of revenue has also fluctuated in the past, based primarily on our ability to achieve economies of scale, the management of our operating expenses, and the timing and costs incurred related to our acquisitions and investments.

In fiscal years 2025 and 2024, approximately 89% and 88%, respectively, of our consolidated revenue was generated from our non-U.S. operations, and approximately 54% and 50%, respectively, of our consolidated revenue was priced in U.S. dollars. We expect that a significant amount of our revenue will continue to be generated from our non-U.S. operations while being priced in U.S. dollars. We have certain client contracts that are priced in non-U.S. dollar currencies for which a substantial portion of the costs to deliver the services are in other currencies. Accordingly, our revenue may be earned in currencies that are different from the currencies in which we incur corresponding expenses. Fluctuations in the value of currencies, such as the Philippine peso, the Indian rupee, the Egyptian pound, the Columbian peso, and the Canadian dollar, against the U.S. dollar or other currencies in which we bill our clients, and inflation in the local economies in which these delivery centers are located, can impact the operating and labor costs in these delivery centers, which can result in reduced profitability. As a result, our revenue growth, costs, and profitability have been impacted, and we expect will continue to be impacted, by fluctuations in foreign currency exchange rates and inflation.

Margins

Our gross margins fluctuate and can be impacted by the mix of client contracts, services provided, shifts in the geography from which our technology and services are delivered, client volume trends, the amount of lead time that is required for programs or services to become fully scaled, and transition and set-up costs. Our operating margin fluctuates based on changes in gross margins as well as overall volume levels, as we are generally able to gain scale efficiencies in our selling, general and administrative costs as our volumes increase.

Economic and Industry Trends

The industry in which we operate is competitive, including on the basis of pricing terms, delivery capabilities, and quality of services. Labor in various markets is also subject to competitive pressures that can result in increased labor costs. These factors subject us to pricing and labor cost pressures that can negatively affect our revenue, gross profit, and operating income.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations – Fiscal Years Ended November 30, 2025 and 2024

Fiscal Years Ended November 30,
2025 | 2024
(in thousands)
Revenue | 9,825,771 | 9,618,900
Cost of revenue | 6,390,760 | 6,170,013
Gross profit | 3,435,011 | 3,448,887
Selling, general and administrative expenses | 2,825,468 | 2,852,500
Impairment charges | 1,527,726 | —
Operating income (loss) | (918,183) | 596,387
Interest expense and finance charges, net | 290,349 | 321,828
Other income, net | (26,310) | (24,715)
Income (loss) before income taxes | (1,182,222) | 299,274
Provision for income taxes | 96,702 | 48,057
Net income (loss) | (1,278,924) | 251,217

Revenue

Fiscal Years Ended November 30, | Percent Change
2025 | 2024 | 2025 to 2024
(in thousands)
Industry vertical:
Technology and consumer electronics | 2,666,072 | 2,674,040 | (0.3) | %
Retail, travel and e-commerce | 2,433,885 | 2,361,866 | 3.0 | %
Communications and media | 1,592,373 | 1,527,922 | 4.2 | %
Banking, financial services and insurance | 1,536,223 | 1,455,641 | 5.5 | %
Healthcare | 725,283 | 727,389 | (0.3) | %
Other | 871,935 | 872,042 | 0.0 | %
Total | 9,825,771 | 9,618,900 | 2.2 | %

We generate revenue by delivering our technology and services to our clients categorized in the above industry verticals. Our solutions focus on customer engagement, process optimization, and back-office automation.

Our revenue increased 2.2% in fiscal year 2025. The increase in revenue resulted primarily from increases in revenue in our retail, travel and e-commerce, communications and media, and banking, financial services and insurance verticals. Changes in foreign currency exchange rates had a de minimis impact on revenue growth for fiscal year 2025.

Revenue increased in our retail, travel and e-commerce, communications and media, and banking, financial services and insurance verticals, while revenue decreased slightly in our technology and consumer electronics and healthcare verticals and remained flat in our other vertical. Revenue in our technology and consumer electronics vertical decreased 0.3%, which included a decrease as a result of foreign currency exchange rates and a decrease in underlying business with a client in this vertical, partially offset by increases in business with several clients in the vertical. Revenue in our retail, travel and e-commerce vertical increased 3.0%, which included increases in underlying business, primarily from several larger clients in this vertical. Revenue in our communication and media vertical increased 4.2%, which included increases in underlying business primarily from several larger clients in the vertical. Revenue in our banking, financial services and insurance vertical increased 5.5%, which included increases in underlying business from the majority of clients in the vertical. Revenue in our healthcare vertical decreased 0.3%, which included slight decreases in underlying business, primarily from a larger client in the vertical, partially

offset by increases in business with several other clients in the vertical. Revenue in our other vertical remained flat over prior year and included a decrease in underlying business, primarily related to an automotive client, partially offset by increases in business with several other clients in the vertical.

Cost of Revenue, Gross Profit and Gross Margin Percentage

Fiscal Years Ended November 30, | Percent Change
2025 | 2024 | 2025 to 2024
($ in thousands)
Cost of revenue | 6,390,760 | 6,170,013 | 3.6 | %
Gross profit | 3,435,011 | 3,448,887 | (0.4) | %
Gross margin % | 35.0 | % | 35.9 | %

Cost of revenue consists primarily of personnel costs. Gross margins can be impacted by resource location, client mix and pricing, additional lead time for programs to be fully scalable, and transition and initial set-up costs.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-01-28_item1_business.md)

ITEM 1. BUSINESS

Our Company

We are a global technology and services leader that powers exceptional brand experiences and digital operations for more than 2,000 clients across the globe. We design, build, and run fully integrated, end-to-end solutions — including customer experience ("CX") process optimization, technology innovation and design engineering, front- and back-office automation, analytics, and business transformation services — for clients in five primary industry verticals. Our solutions help our clients drive deep understanding, full lifecycle engagement, and differentiated customer experiences for their brands.

We strive to deliver exceptional services globally , supported by our deep industry knowledge, technology and security practices, talented people, and digital and analytics expertise. Our differentiated portfolio of solutions supports Fortune Global 500 and new economy companies across the globe in their efforts to deliver an optimized, consistent brand experience across all channels of communication, including voice, chat, email, generative AI ("GenAI") and agentic AI-powered self-service, social media, asynchronous messaging, and other custom applications.

We offer our clients integrated solutions to support the entirety of their customer lifecycles, transform their businesses, and solve business challenges:

• CX and user experience ("UX") strategy and design;

• digital operations, including business-to-business ("B2B") sales, performance marketing, customer loyalty, trust and safety, collections, and financial compliance;

• data analytics, enterprise intelligence, artificial intelligence ("AI") readiness, and actionable insights; and

• innovative new approaches to enhancing the customer experience through the latest technological advancements in our industry, including GenAI and agentic AI technologies.

Through our end-to-end capabilities, we believe we deliver better economic outcomes for our clients with solutions designed to meet their unique needs as they navigate a landscape characterized by discerning consumers and new market entrants.

We have strong relationships with global brands and are a partner of choice for industry leaders, including more than 160 Fortune Global 500 clients as of November 30, 2025. We believe in deepening and broadening our support of clients over the long term to build enduring relationships, and we prioritize the pursuit of clients in verticals characterized by high growth, high transaction volume, high levels of compliance and security, and steep barriers to entry. Our average client tenure for our top 30 clients is 16 years. Our strategic verticals include:

• technology and consumer electronics;

• retail, travel and e-commerce;

• communications and media;

• banking, financial services and insurance; and

• healthcare.

Our clients include:

• 8 of the top 10 global tech and consumer electronics companies

• 8 of the top 10 global fintech companies

• 2 of the top 5 global retail and e-commerce companies

• 8 of the top 10 European banks

• 7 of the top 10 U.S. banks

• 5 of the top 5 U.S. health insurance companies

• 3 of the top 5 global healthcare companies

• 10 of the top 10 global automotive companies

Through our technology-infused solutions, our clients benefit from having a single partner that can deliver integrated solutions globally at scale, enabling them to address the entirety of the customer journey, from acquisition to support to renewal. Our end-to-end capabilities and broad service offerings help our clients acquire, retain, and improve the lifetime value of their customer relationships while optimizing their back-office processes.

We combine global consistency with local expertise, enhancing the end user experience for our clients' customers through services rendered by a team of approximately 455,000 employees and staff, which we refer to as game-changers, across approximately 483 locations in 74 countries and six continents in the languages and dialects that are relevant to our clients and their customers.

Strategic Growth

We have a long history of growth through strategic acquisitions, including:

• Our September 2025 acquisition of SAI Digital, an end-to-end digital commerce and CX technology solutions company with a strong presence in Asia;

• Our September 2023 acquisition of the Webhelp business ("Webhelp"), a leading provider of CX solutions, including sales, marketing, and payment services, with significant operations and client relationships in Europe, Latin America, and Africa;

• Our July 2022 acquisition of ServiceSource International, Inc. ("ServiceSource"), a global outsourced go-to-market services provider that delivered business-to-business ("B2B") digital sales and customer success solutions;

• Our December 2021 acquisition of PK, a leading CX design engineering company that created pioneering experiences to accelerate digital outcomes for their clients' customers, partners and staff; and

• Our October 2018 acquisition of Convergys Corporation, a customer experience outsourcing company that added scale, diversified our revenue base, and expanded our service delivery capabilities.

Our strategic acquisitions have strengthened our position as a global technology and services leader by expanding our scale in the digital IT services market and creating one of the most robust, well-balanced global footprints in the industry. Our disciplined approach to growth has strengthened our value proposition for our clients by broadening our offering of AI solutions, digital capabilities, and high-value services.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-01-28_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-01-28_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-01-28_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-06-29_2-02-results.md, 10-K_2026-01-28_item7_mdna.md, 10-K_2026-01-28_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
