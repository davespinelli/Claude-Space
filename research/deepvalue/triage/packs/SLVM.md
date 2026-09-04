# Triage pack — SLVM · Sylvamo Corp

_Generated 2026-09-04 17:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** SLVM · **Name:** Sylvamo Corp
- **CIK:** 0001856485
- **SIC:** 2621 — Paper Mills
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/SLVM

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Sylvamo Corp
- **CIK:** 1,856,485 · **SIC:** 2621 (Paper Mills) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtAndCapitalLeaseObligations

**Valuation**

| metric | value |
|---|---|
| price | 35.53 |
| mktcap | $1.4B |
| ev | $2.1B |
| ev_ebit | 8.5x |
| fcf | $44.0M |
| fcf_yield | 3.1% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 11.8% |
| net_debt | $720.0M |
| net_debt_ebit | 2.9x |
| cash | $123.0M |
| ltd | $843.0M |
| equity | $955.0M |
| ltd_tag | LongTermDebtAndCapitalLeaseObligations |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $3.4B |
| revenue_prior | $3.8B |
| rev_growth | -11.2% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $251.0M |
| net_income | $132.0M |
| cfo | $268.0M |
| capex | $224.0M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -1.5% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 39,760,243 |
| shares_py | 40,372,555 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -8.4% |
| r6m | -19.5% |
| off_52w_high | -33.6% |
| adv20 | $9.6M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.38 |
| r_ev_ebit | 0.81 |
| r_roic | 0.75 |
| r_rev_growth | 0.09 |
| r_buyback | 0.77 |
| score | 0.56 |

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
| rank | 185 |

**Screen rationale:** cheap at 8.5x EV/EBIT; buying back stock -1.5%


## 3. Share count trend

- Shares outstanding: **39,760,243** (CY2026Q2I) vs **40,372,555** prior year (CY2025Q2I)
- Change: **-1.5%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-02 among the 3 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 14 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 13 |
| F | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-07_2-02-results.md)

_Extraction: started at the first release heading, 'Sylvamo Releases Second Quarter Earnings'; skipped 8 forward-looking-statement block(s); 5 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (sylvamoex9912026secondquar.htm)

Sylvamo Releases Second Quarter Earnings

MEMPHIS, Tenn. – Aug. 7, 2026 – Sylvamo (NYSE: SLVM), the world's paper company, is releasing second quarter earnings. The company will host an audio webcast at 10 a.m. EDT at investors.sylvamo.com .

Management Summary from Chief Executive Officer John Sims

Our second quarter highlights include implementing uncoated freesheet price increases with our customers across all regions. We're advancing our lean transformation journey to embed continuous improvement into how we run the business, so performance improvement becomes employee-driven, systematic and self-sustaining. Our teams also continue to make good progress on our high-return strategic investments at our Eastover, South Carolina, mill.

2026 is a transition year as we adjust our North America footprint while working through the termination of the Riverdale supply agreement with International Paper (NYSE: IP), changing tariffs and the extended outage to complete our strategic investments at our Eastover mill. Our commercial and supply chain teams have done an outstanding job to ensure our customers are well served.

Our strategic investments at Eastover continue to progress:

• The woodyard modernization project is going well, with the hardwood line yielding improved reliability and chip quality since its startup in May. The softwood operation remains on schedule for the first quarter of 2027.

• The paper machine optimization project remains on schedule, on budget and is expected to be completed during a planned maintenance outage in the fourth quarter, which will add an additional 60,000 short tons of uncoated freesheet capacity annually.

• The new cutsize sheeter passed equipment acceptance testing in June, arrived in the U.S. a few weeks ago and teams are preparing for installation.

• We are expanding warehouse capacity at our existing sheeting plant through a sale-leaseback transaction with a third party. The project will reduce supply chain costs, improve service to our customers and provide additional flexibility. We expect this project to be completed in the first quarter of 2027.

In the second quarter, Sylvamo generated a net loss of $11 million and adjusted EBITDA * of $60 million. Cash from continuing operations was $38 million, and free cash flow * was negative $23 million. In the last few years, we generated most of our free cash flow in the second half, and we expect to do so again this year.

Overall, we expect a much better earnings performance for the last six months of the year as price and mix, volume and operations should be better compared to the first half.

Our board of directors declared a $0.45 dividend for the third quarter, which we paid July 28.

-Regional Business Conditions

• In Europe, pulp prices improved throughout the first half of the year and seem stable. We continue to realize previously communicated price increases and announced another price increase effective in mid-June, which we expect to realize through the third quarter.

*See "Non-GAAP Financial Measures" for definitions of non-GAAP financial measures. Reconciliations are included in the financial schedules below.

Exhibit 99.1

• In Latin America, we expect seasonally higher demand through the second half of the year, positively impacting volume and geographic mix. We continue to realize previously communicated price increases to export customers across other Latin American countries as well as customers in the Middle East and Africa. Realization of these increases should continue through the third quarter.

• In North America, industry supply and demand dynamics improved as roughly 7% of the annual uncoated freesheet industry supply was removed with the Riverdale paper machine conversion. In the second quarter, we saw imports into North America increase compared to the previous quarter, a reaction to the 10% global tariff window. We also continue to realize previously communicated paper price increases and expect to see additional realization through the third quarter.

We expect the Middle East conflict to continue pressuring energy, chemical and transportation costs across our regions as we go through the year.

-Looking Ahead

We continue to execute in the six areas I outlined in my letter to shareowners earlier this year that define how Sylvamo will be legendary for the way we relentlessly pursue and achieve world-class excellence. These areas are safety and well-being, employee engagement, customer centricity, operational excellence, cost leadership and sustainability, all of which support our long-term value creation strategy for shareowners.

We will make disciplined, data-driven decisions that position us for sustainable success and strengthen Sylvamo for decades to come. As industry conditions turn, our capital spending normalizes and the benefits from our investments begin to materialize, we have the potential to generate annually:

• > $300 million in free cash flow

• > 15% return on invested capital

Earnings Webcast

The company will host an audio webcast at 10 a.m. EDT at investors.sylvamo.com .

To participate in Q&A, use the analyst registration to receive a unique passcode.

Replays will be available at investors.sylvamo.com for one year.

Investor Contact: Hans Bjorkman, 901-519-8030, Hans.Bjorkman@sylvamo.com

Media Contact: Adam Ghassemi, 901-519-8115, Adam.Ghassemi@sylvamo.com

About Sylvamo

Sylvamo Corporation (NYSE: SLVM) is the world's paper company with mills in Europe, Latin America and North America. Our vision is to be the employer, supplier and investment of choice. We transform renewable resources into papers that people depend on for education, communication and entertainment. Headquartered in Memphis, Tennessee, we employ more than 6,500 colleagues. Net sales for 2025 were $3.4 billion. For more information, please visit Sylvamo.com .

Exhibit 99.1

Select Financial Measures

(In millions) | Second Quarter 2026 | First Quarter 2026 | Second Quarter 2025
Net Sales | 806 | 755 | 794
Net Income (Loss) | (11) | (3) | 15
Business Segment Operating Profit (Loss) | 14 | (15) | 30
Adjusted Operating Earnings (Loss) | 1 | (21) | 15
Adjusted EBITDA | 60 | 29 | 82
Cash Provided By (Used For) Operating Activities | 38 | (10) | 64
Free Cash Flow | (23) | (59) | (2)

Segment Information

Sylvamo uses business segment operating profit (loss) to measure the earnings performance of its businesses, see definition within "Non-GAAP Financial Measures". Second quarter 2026 sales by business segment and operating profit (loss) by business segment compared with the first quarter of 2026 and the second quarter of 2025 are as follows:

Business Segment Results

(In millions) | Second Quarter 2026 | First Quarter 2026 | Second Quarter 2025
Sales by Business Segment
Europe | 197 | 190 | 181
Latin America | 219 | 187 | 207
North America | 411 | 390 | 419
Inter-segment Sales | (21) | (12) | (13)
Net Sales | 806 | 755 | 794
Operating Profit (Loss) by Business Segment
Europe | (20) | (44) | (38)
Latin America | (16) | 4 | 2
North America | 50 | 25 | 66
Business Segment Operating Profit (Loss) | 14 | (15) | 30

Operating profits in the second quarter of 2026:

Europe - $(20) million compared with $(44) million in the first quarter of 2026. Losses were lower due to higher sales price and mix and lower operating and input costs which were partially offset by higher planned maintenance outages.

Latin America - $(16) million compared with $4 million in the first quarter of 2026. Earnings were lower due to higher planned maintenance outages and higher input costs which were partially offset by higher sales price and mix and higher volumes.

North America - $50 million compared with $25 million in the first quarter of 2026. Earnings were higher due to higher sales price and mix and lower operating and input costs which were slightly offset higher planned maintenance outages.

Effective Tax Rate

The reported effective tax rate for the second quarter of 2026 was 1200%, compared to 50% for the first quarter of 2026. The higher rate for the second quarter was primarily driven by a $12 million valuation allowance on certain foreign deferred tax assets which will not expected to be realized due to a planned internal merger.

The effective operational tax rate for the second quarter of 2026 was 80%, compared with 13% for the first quarter of 2026.

Exhibit 99.1

The effective operational tax rate is a non-GAAP financial measure and is calculated by adjusting the income tax provision (benefit) and rate to exclude the tax effect at the applicable statutory rate of net special items and the impact of foreign exchange on an intercompany note receivable from our Brazilian subsidiary. Management believes that this presentation provides useful information to investors by providing a more meaningful comparison of the income tax rate between past and present periods.

Effects of Net Special Items

Net special items in the second quarter of 2026 amounted to a net after-tax charge of $13 million ($0.34 per diluted share), compared with a net after-tax charge of $1 million ($0.03 per diluted share) in the first quarter of 2026.

Non-GAAP Financial Measures

Adjusted Operating Earnings (Loss) (non-GAAP) are net income (loss) (GAAP) plus the impact of foreign exchange on an intercompany note receivable from our Brazilian subsidiary, and, when applicable for the periods reported, net special items. Management uses this measure to focus on ongoing operations and believes it is useful to investors because it enables them to perform meaningful comparisons of past and present operating results. The Company believes that using this information, along with net income (loss), provides for a more complete analysis of the results of operations. Net income (loss) is the most directly comparable GAAP measure. For more information regarding net special items, see the information under the heading Effects of Net Special Items and the Consolidated Statement of Operations and related notes included later in this release.

Adjusted EBITDA (non-GAAP) is net income (loss) (GAAP) plus the sum of income taxes, net interest expense, depreciation, amortization and cost of timber harvested, stock-based compensation, the impact of foreign exchange on an intercompany note receivable from our Brazilian subsidiary, and, when applicable for the periods reported, net special items. Management uses these measures in managing the operating performance of our business and believes that adjusted EBITDA along with adjusted EBITDA margin provide investors and analysts meaningful insights into our operating performance and is a relevant metric for the third-party debt. Adjusted EBITDA is reconciled to net income (loss), the most directly comparable GAAP measure. Adjusted EBITDA margin (adjusted EBITDA divided by net sales) is reconciled to net income (loss) margin (net income (loss) divided by net sales), the most directly comparable GAAP measure. For more information regarding net special items, see the information under the heading Effects of Net Special Items and the Consolidated Statement of Operations and related notes included later in this release.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-20_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

EXECUTIVE SUMMARY

Full-year 2025 net income was $132 million ($3.24 per diluted share) compared with $302 million ($7.18 per diluted share) for 2024. Net sales decreased to $3.4 billion in the current year compared with $3.8 billion in 2024. Cash from continuing operations was $268 million in the current year compared to $469 million in the prior year. Adjusted EBITDA was $448 million in 2025 compared with $632 million in 2024. Additionally, our 2025 adjusted EBITDA margin was 13% compared to 17% in the prior year and free cash flow was $44 million compared to $248 million last year.

Comparing our performance in 2025 to 2024, challenging industry conditions contributed to lower volumes of uncoated freesheet across all three of our regions. Price and mix were unfavorable in Europe and Latin America but improved in North America. Planned maintenance outages were significantly higher due to two outages in Europe compared with one in the previous year. Europe and North America benefited from lower unabsorbed fixed costs due to reduced economic manufacturing downtime in 2025. Input costs and operations were unfavorable in all of our regions compared to 2024. We generated $44 million in free cash flow this year and returned $155 million in cash to shareowners. We also reinvested $224 million across our manufacturing network and Brazil forestlands to strengthen our low-cost position.

Looking ahead, 2026 will be a transition year for North America as we work through short-term capacity constraints with the Riverdale supply agreement exit and the execution of investments at our Eastover mill. We are prioritizing strategic projects with the fastest payback so that 2027 and beyond reflects lower costs, higher efficiency, and stronger cash conversion potential. We strive to create long-term shareowner value by executing our strategy and delivering on our investment thesis. Keeping a strong financial position is the cornerstone of our capital allocation framework. This allows us to reinvest in our business to strengthen our competitive advantages through the cycle and to increase future earnings and cash flow.

RESULTS OF OPERATIONS

When reading our financial statements and the information included in this Annual Report on Form 10-K, it should be considered that we have experienced, and continue to experience, several material trends and uncertainties that have affected our financial condition and results of operations and that could affect future performance. We believe that the following material trends and uncertainties are important to understanding our business.

Macroeconomic Conditions

The Company's operating results are typically closely tied to changes in the general economic conditions in Europe, Latin America and North America, as well as general global economic conditions. The Company's profitability and operating results are dependent on the price of our products and the market price of raw materials (primarily wood fiber and chemicals), energy sources and third-party transport of our goods. Historically, economic and market shifts, inflationary pressures, fluctuations in

capacity and changes in foreign currency exchange rates have created changes in prices, sales volume and margins for our products.

Consumer Behavior

Factors that impact the demand for our products include general macroeconomic conditions, consumer preferences, movements in currency exchange rates, consumer spending, commercial printing and advertising activity, adoption of electronic mediums, and white-collar employment and the shift to hybrid work models.

DESCRIPTION OF BUSINESS SEGMENTS

The Company's reportable business segments, Europe, Latin America and North America, are organized by geography and are consistent with the internal structure used to manage these businesses. Each of our segments derive their revenue from the manufacture and sale of paper and pulp products. The following summary describes the products and services offered in each of the segments as of December 31, 2025:

Europe

Our Europe segment produces a broad portfolio of uncoated freesheet papers for numerous uses and applications, and market pulp. We operate two integrated mills in the region, one in Saillat, France and one in Nymölla, Sweden. Located in the Limousin region of France, the Company's Saillat mill produces both paper and market pulp. It is the only mill in France to cover the entire production process from wood harvesting to paper, and is one of the leading cutsize producers in France and Western Europe. The Saillat mill produces UFS papers, such as copy paper, and value-added products such as tinted paper and colored laser printing paper under leading brands such as REY. In 2025, we made investments in our finished roll production capabilities to improve our product mix and also allow us to enhance our business in graphic and high-speed inkjet printing papers under the brand Berga. The Saillat mill has some of the highest environmental credentials for our products. In January 2023, the Company acquired a paper mill in Nymölla, Sweden. The integrated mill has two pulp lines and the capacity to produce approximately 500,000 short tons of uncoated freesheet on two paper machines. The mill produces several brands, including Multicopy, and paper used for office printing, business forms, digital printing, offset for printing books and much more. The Nymölla mill has an excellent environmental footprint, which complements Sylvamo's purpose to produce paper in the most responsible and sustainable ways.

Latin America

Our Latin American segment focuses on uncoated freesheet paper and market pulp, supported by the management of approximately 250,000 acres of certified eucalyptus forestlands in Brazil. With a total uncoated freesheet paper capacity exceeding 1.1 million short tons, our three mills in Brazil serve both regional and international markets, being a key supplier in Latin America and a solid global exporter, reaching customers worldwide. Our portfolio includes market-leading brands such as Chamex and Chamequinho copy papers, widely recognized by consumers and distribution channels for their superior quality. Additionally, Chambril offset papers are trusted by printers and converters for their versatility and reliability across various applications. Chambril is available in a wide range of basis weights and specifications to meet the demands of books, notebooks, inserts, leaflets, and industrial end-use requirements. All the products are primarily made from sustainably sourced eucalyptus, which is cultivated and harvested in less than seven years. Latin America operations combine sustainable forestry practices, operational excellence, strong brands and global distribution network.

North America

Our North American segment manufactures uncoated freesheet papers at its mills in Eastover, South Carolina and Ticonderoga, New York and has an offtake agreement to purchase the uncoated papers produced by International Paper's Riverdale mill in Selma, Alabama. This offtake agreement is expected to terminate in May 2026. The North American papers business comprises three product lines, Imaging Papers, Commercial Printing Papers and Converting Papers. The imaging papers business, which comprises roughly half of the North American segment's volume, produces copy paper for use in copiers, desktop and laser printers and digital imaging. These products are important for office use, home office use and in businesses such as education, healthcare and financial services. The commercial printing business comprises about 17% of the North American segment's volume, and end-use applications in the commercial printing business include advertising and promotional materials such as brochures, pamphlets, greeting cards, books, annual reports and direct mail. The converting business manufactures a variety of grades that are converted by our customers into envelopes, tablets, business forms, file folders and several specialty grades.

Uncoated papers are sold under private label and brand names that include Hammermill®, Springhill®, Williamsburg, Accent®, DRM® and Postmark®.

BUSINESS SEGMENT RESULTS

Management provides business segment operating profit, a non-GAAP financial measure, to supplement our GAAP financial information, and it should be considered in addition to, but not instead of, the financial statements prepared in accordance with GAAP. Management believes that business segment operating profit provides investors and analysts useful insights into our operating performance. Business segment operating profit is reconciled to Income from continuing operations before income taxes, the most directly comparable GAAP measure. Business segment operating profit may be determined or calculated differently by other companies and therefore may not be comparable among companies.

The following table presents a comparison of income from continuing operations before income taxes to business segment operating profit:

In millions for the years ended December 31 | 2025 | 2024
Income From Continuing Operations Before Income Taxes | 199 | 405
Interest expense (income), net | 39 | 39
Foreign exchange on intercompany note | (1) | —
Corporate special items, net (b) | 1 | —
Other special items, net (b) | 13 | 9
Business Segment Operating Profit (a) | 251 | 453
Europe | (112) | 10
Latin America | 100 | 150
North America | 263 | 293
Business Segment Operating Profit (Loss) (a) | 251 | 453

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-20_item1_business.md)

PART I.

ITEM 1. BUSINESS

OUR COMPANY

Sylvamo Corporation (the "Company" or "Sylvamo", which may also be referred to as "we" or "us") is a global uncoated papers company with a broad portfolio of top-tier brands and low-cost, large-scale paper mills located in and serving the most attractive geographies, including Europe, Latin America and North America, which are our business segments. We produce uncoated freesheet ("UFS") for paper products such as cutsize and offset paper, as well as market pulp. With roots going back to 1898, we have a long history of offering premium quality papers to meet the needs of our customers and end-users. Our mills in North America and Latin America predominantly rank in the lowest quartile on global and regional UFS cost curves, and we believe our low-cost operations enable us to serve our customers with the highest quality products at attractive margins. Our industry-leading brands, known for their long-standing reputation in their respective markets for product quality and performance, allow us to maintain our long-term relationships with top-tier customers throughout economic cycles. Our international reach and strong positioning across retail, merchant and e-commerce channels optimally positions us to meet the paper needs of our end-users around the world. This also provides geographical diversification of our revenue and profits. From 2023 to 2025, on average, we generated 48% of our revenues and 28% of our Business Segment Operating Profit in Europe and Latin America. Each region in which we operate exhibits different supply and demand characteristics. Both Latin America and North America have strong profitability for the uncoated paper industry relative to other geographies. See Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations - Business Segment Results - Results of Operations for a definition of Business Segment Operating Profit.

COMPETITION

The markets in which we operate are highly competitive with well-established domestic and foreign manufacturers. For instance, in North America, the four largest manufacturers of UFS, including Sylvamo, represent approximately 80% of the total annual production capacity. As the use of electronic mediums and alternative products increases, and because paper production does not generally rely on proprietary processes, except for highly specialized papers or products, the areas into which Sylvamo sells its principal products are increasingly competitive. Furthermore, the level of competitive pressure Sylvamo may face is dependent, in part, upon exchange rates, particularly the rate between the U.S. dollar and the Euro and the U.S. dollar and the Brazilian real. Some of our competitors have shut down or converted mills or paper machines at their mills to linerboard, pulp and boxboard capacity, which reduced the supply of UFS and other printing papers.

MARKETING AND DISTRIBUTION

Sylvamo sells products directly to end users and converters, as well as through agents, resellers and paper distributors.

DESCRIPTION OF PRINCIPAL PRODUCTS

The Company's principal products are described in Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations .

RAW MATERIALS

Raw materials essential to our businesses include wood fiber, chemicals, water and energy. Information about our sources and the availability to us of raw materials, particularly wood, the principal raw material from which our products are made, is included in Item 1A. Risk Factors - " Increased costs or decreased availability of raw materials and energy could adversely affect our business. " and Item 7. Managements's Discussion and Analysis of Financial Condition and Results of Operations.

HUMAN CAPITAL

In this Human Capital section and elsewhere in this Annual Report on Form 10-K, we refer in various contexts to our website and to sustainability performance reviews, other reports, policies, and other information published by us or on our website. The information on our website and in the referenced sustainability performance reviews, other reports, policies and other

information, and that is otherwise connected to our website, is not incorporated by reference into this Annual Report on Form 10-K, and should not be considered part of this or any other report that we file with or furnish to the SEC.

Employees

Sylvamo' s capabilities and potential are delivered through our dedicated, talented and diverse workforce, which we believe is among the best in the industry. As of December 31, 2025, our global workforce of over 6,500 people was located approximately 25% in Europe, 49% in Latin America and 26% in North America. A portion of our workforce is represented by unions in Brazil, France, Sweden and, in the United States, at our mill in Ticonderoga, New York. We believe that our relationships with our unions a re constructive.

We strive to be the employer of choice. We aim to attract, retain and develop talented employees that reflect our diverse communities and global end-users of our paper. To that end, we work to foster a safe and inclusive workplace where all employees feel safe, welcomed, valued, engaged, fairly compensated and have opportunities for professional development.

Health and Safety

Our priority is people before paper -- the health and safety of our employees, contractors and visitors to our facilities are paramount. We strive to design and operate injury-free workplaces for our employees and everyone who enters our facilities. As responsible stewards of people and their communities, we have emphasized safety at our Company and strictly complied with national regulations such as, in the United States, the Occupational Safety and Health Administration's regulatio ns. Based on our safety record and our comparison of it against publicly available industry safety information, we are an industry-leading company in employee safety.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-20_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-20_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-20_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-07_2-02-results.md, 10-K_2026-02-20_item7_mdna.md, 10-K_2026-02-20_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
