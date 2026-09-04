# Triage pack — MTRX · MATRIX SERVICE CO

_Generated 2026-09-04 20:11 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** MTRX · **Name:** MATRIX SERVICE CO
- **CIK:** 0000866273
- **SIC:** 1700 — Construction - Special Trade Contractors
- **Fiscal year end (MM-DD):** 06-30
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/MTRX

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** MATRIX SERVICE CO
- **CIK:** 866,273 · **SIC:** 1700 (Construction - Special Trade Contractors) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 10.55 |
| mktcap | $296.8M |
| ev | $73.8M |
| ev_ebit | n/a |
| fcf | $109.8M |
| fcf_yield | 37.0% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | -$223.0M |
| net_debt_ebit | n/a |
| cash | $223.0M |
| ltd | $0.00 |
| equity | n/a |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $769.3M |
| revenue_prior | $728.2M |
| rev_growth | 5.6% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$35.1M |
| net_income | -$29.5M |
| cfo | $117.5M |
| capex | $7.7M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 1.9% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 28,133,850 |
| shares_py | 27,610,499 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -18.9% |
| r6m | -6.1% |
| off_52w_high | -32.4% |
| adv20 | $2.9M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.96 |
| r_ev_ebit | 0.00 |
| r_roic | 0.50 |
| r_rev_growth | 0.54 |
| r_buyback | 0.33 |
| score | 0.47 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | n/a |
| shares_period | CY2026Q1I |
| shares_py_period | CY2025Q1I |
| capex_missing | False |
| ltd_missing | True |

**Other screen columns**

| metric | value |
|---|---|
| rank | 273 |

**Screen rationale:** top-quartile FCF yield 37.0%; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **28,133,850** (CY2026Q1I) vs **27,610,499** prior year (CY2025Q1I)
- Change: **1.9%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-02** — Item 5.02 (officer / director change or comp arrangement): In connection with our previously announced leadership transition and his appointment to the role of President and Chief Executive Officer of Matrix Service Company (the "Company"), the Board of Directors (the "Board") of the Company has elected Shawn P....
- **2026-04-30** — Item 5.02 (officer / director change or comp arrangement): As part of broader organizational changes across the Company following the previously announced appointment of Shawn P. Payne as Chief Executive Officer, who will assume his new role effective July 1, 2026, Kevin S. Cavanah, Vice President of Finance and...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 182,415 sh / $2,406,195 -> net $-2,406,195 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 62 (open-market buys 0, sales 9).

| code | rows |
|---|---|
| A | 4 |
| D | 12 |
| F | 13 |
| M | 24 |
| S | 9 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-09-02_2-02-results.md)

_Extraction: started at the first release heading, 'MATRIX SERVICE COMPANY REPORTS FISCAL YEAR 2026 FOURTH QUARTER AND FUL'; skipped 8 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99 - EX-99 (a063026ex99earningsrelease.htm)

MATRIX SERVICE COMPANY REPORTS FISCAL YEAR 2026 FOURTH QUARTER AND FULL-YEAR RESULTS

HOUSTON, TX – September 2, 2026 – Matrix Service Company (Nasdaq: MTRX, "Matrix" or "the Company"), a leading heavy industrial contractor that engineers, constructs, and maintains critical energy, power, and industrial infrastructure, today announced financial results for the fourth quarter of fiscal 2026 ended June 30, 2026.

FOURTH QUARTER FISCAL 2026 HIGHLIGHTS

(all comparisons versus the prior year period unless otherwise noted)

• Revenue of $244.5 million versus $216.4 million; highest quarterly revenue in six years

• Net income of $1.1 million, or $0.04 per share versus net loss of $(11.3) million or $(0.40) per share

• Adjusted net income (1) of $4.6 million, or $0.16 per share versus adjusted net loss of $(7.8) million, or $(0.28) loss per share; second consecutive quarter of profitability

• Adjusted EBITDA (1) of $6.3 million versus $(4.8) million

• Liquidity (2) at June 30, 2026 of $283.9 million with no outstanding debt

• Total backlog of $953.2 million, with awards of $169.0 million

FULL-YEAR FISCAL 2026 RESULTS

(all comparisons versus the prior year period unless otherwise noted)

• Revenue of $873.6 million versus $769.3 million

• Net loss per share of $(0.09) versus $(1.06); adjusted net income (loss) per share of $0.26 versus $(0.93)

• Adjusted EBITDA of $16.0 million versus $(12.9) million

(1) Adjusted net income and adjusted net income per diluted share are non-GAAP financial measures which exclude restructuring expense, Adjusted EBITDA is a non-GAAP financial measure which excludes interest expense, interest income, income taxes, depreciation and amortization expense, restructuring expense, and stock-based compensation. See the Non-GAAP Financial Measures section included at the end of this release for a reconciliation to net income and net income per share.

(2) Liquidity includes unrestricted cash, cash equivalents and borrowing availability under a $90 million ABL facility maturing in September 2029

MANAGEMENT COMMENTARY

"Our fourth quarter results reflect the continued execution of our WIN, EXECUTE, DELIVER strategy. The combination of strong project execution, a more efficient cost structure, and a disciplined focus on the initiatives that matter most resulted in our second consecutive quarter of profitable growth," stated Shawn P. Payne, President and Chief Executive Officer. "Revenue grew 13% year over year as our teams converted backlog into higher volumes, led by specialty storage activity in our Storage and Terminal Solutions segment and continued strong execution in Utility and Power Infrastructure. At the same time, the leaner organizational structure we have built over the past 18 months has meaningfully reduced our fixed overhead costs, while enabling us to support a higher base of revenue with improved efficiency. We enter fiscal 2027 with a debt-free balance sheet and substantial liquidity to support our growth objectives in this next chapter.

"Matrix is focused on high-value opportunities, prioritizing backlog growth across our targeted end-markets," continued Payne. "We secured nearly $170 million of project awards in the fourth quarter, including a major mining construction project in the western United States. This project, which supported a book-to-bill ratio of 3.2x in our Process and Industrial Facilities during the fourth quarter, expands our position in the non-ferrous mining and critical minerals market, broadens the range of end markets served by our engineering and construction capabilities, and represents an important new client relationship that we expect to expand over time.

"Fiscal 2026 was a pivotal year for Matrix," concluded Payne. "Our opportunity pipeline has grown to over $7 billion, reflecting generational levels of investment underway across the markets we serve, including LNG and NGL infrastructure, power generation, electric grid modernization, data centers, and mining and minerals production. A number of larger, multi-year opportunities within that pipeline have advanced meaningfully, and we anticipate a higher level of award activity as those targets reach final investment decision. Looking ahead, we are focused on driving profitable growth, executing projects safely, on time and on budget, and deploying capital with discipline as we seek to drive long-term value creation for our clients and shareholders."

FISCAL 2026 FOURTH QUARTER CONSOLIDATED RESULTS

Fiscal 2026 fourth quarter revenue was $244.5 million, compared to $216.4 million in the fourth quarter of fiscal 2025. The increase in revenue for the quarter was attributable to higher revenue in the Storage and Terminal Solutions segment, partially offset by lower revenue in the Process and Industrial Facilities segment.

Gross profit was $19.5 million, or 8.0% of revenue, in the fourth quarter of fiscal 2026 compared to $8.1 million, or 3.8% of revenue, for the fourth quarter of fiscal 2025. The increase in gross margin was due to higher gross margins in the Storage and Terminal Solutions and Utility and Power Infrastructure segments, partially offset by lower gross margins in the Process and Industrial Facility segment.

SG&A expenses were $16.9 million in the fourth quarter of fiscal 2026, compared to $17.6 million for the fourth quarter of fiscal 2025. The decrease in SG&A expenses primarily reflects the reduction of costs associated with the Company's organizational realignment initiatives over the last 12 months partially offset by variable compensation tied to a return to profitable performance.

During the quarter, the Company incurred $3.4 million of restructuring costs and other expenses, which included costs associated with the previously announced leadership transitions, as well as costs associated with actions taken in the fourth quarter to reduce our cost structure by reducing our workforce.

For the fourth quarter of fiscal 2026, the Company had net income of $1.1 million, or $0.04 per share, compared to a net loss of $11.3 million, or $(0.40) per share, in the fourth quarter of fiscal 2025. Adjusted net income for the fourth quarter of fiscal 2026 was $4.6 million, or $0.16 per share, compared to adjusted net loss of $7.8 million, or $(0.28) per share in the fourth quarter of fiscal 2025. Adjusted EBITDA for the fourth quarter of fiscal 2026 was $6.3 million compared to a loss of $4.8 million for the fourth quarter of fiscal 2025.

FISCAL 2026 FOURTH QUARTER SEGMENT RESULTS

Storage and Terminal Solutions segment revenue increased 43% to $137.4 million in the fourth quarter of fiscal 2026 compared to $96.1 million in the fourth quarter of fiscal 2025, due to higher specialty storage activity. Gross margin was 6.4% in the fourth quarter of fiscal 2026, compared to (1.1)% in the fourth quarter of fiscal 2025. In the fourth quarter of fiscal 2025, the Company lowered its recovery expectations on a legacy project completed in fiscal 2021 that was in arbitration which resulted in a $6.4 million decrease to both revenue and gross margin. The matter was fully resolved in fiscal 2026.

Utility and Power Infrastructure segment revenue was $73.5 million in the fourth quarter of fiscal 2026, which was consistent with the prior year period. Gross margin was 12.8% in the fourth quarter of fiscal 2026, compared to 9.1% for the fourth quarter of fiscal 2025, an increase of 3.7% due to strong project execution.

Process and Industrial Facilities segment revenue decreased to $33.6 million in the fourth quarter of fiscal 2026 compared to $47.3 million in the fourth quarter of fiscal 2025, primarily due to lower revenue volumes for refinery work, partially offset by an increase in revenue for a mining project. Gross margin was 2.9% in the fourth quarter of fiscal 2026, compared to 5.9% for

the fourth quarter of fiscal 2025, a decrease of 3.0%, primarily due to a mix of work, as well as an increase in under-recovery of overhead costs as a result of lower revenue.

BACKLOG

Total backlog was $953.2 million as of June 30, 2026. Project awards totaled $169.0 million in the fourth quarter of fiscal 2026, resulting in a book-to-bill ratio of 0.7x for the quarter. Project awards during the fourth quarter for fiscal 2026 were driven primarily by activity in the Process and Industrial Facilities segment, including a major mining construction project in the western United States.

The table below summarizes awards, book-to-bill ratios and backlog by segment for the fourth quarter ended June 30, 2026 (amounts are in thousands, except for book-to-bill ratios):

Three Months Ended | Backlog as of
June 30, 2026
Segment: | Awards | Book-to-Bill (1) | June 30, 2026
Storage and Terminal Solutions | 31,201 | 0.2x | 641,159
Utility and Power Infrastructure | 29,805 | 0.4x | 145,732
Process and Industrial Facilities | 108,036 | 3.2x | 166,287
Total | 169,042 | 0.7x | 953,178

(1) Calculated by dividing project awards by revenue recognized during the period.

BALANCE SHEET & LIQUIDITY

As of June 30, 2026, Matrix had total liquidity of $283.9 million. Liquidity is comprised of $223.0 million of unrestricted cash and cash equivalents and $60.9 million of borrowing availability under the credit facility. The Company also has $25.0 million of restricted cash to support the credit facility. As of June 30, 2026, the Company had no outstanding debt.

CONFERENCE CALL DETAILS

In conjunction with the earnings release, Matrix Service Company will host a conference call with Shawn P. Payne, President and CEO, Kevin S. Cavanah, Vice President and CFO, and Patrick Roberts, Director, Corporate Development and Investor Relations. The call will take place at 10:30 a.m. (Eastern) / 9:30 a.m. (Central) on Thursday, September 3, 2026.

Investors and other interested parties can access a live audio-visual webcast using this webcast link: https://edge.media-server.com/mmc/p/iaonjazk , or through the Company's website at www.matrixservicecompany.com on the Investors Relations page under Events & Presentations.

If you would like to dial in to the conference call, please register at https://register-conf.media-server.com/register/BIa70ac1007e5d4738bedd41c695baab7f at least 10 minutes prior to the start time. Upon registration, participants will receive a dial-in number and unique PIN to join the call as well as an e-mail confirmation with the details.

For those unable to participate in the conference call, a replay of the webcast will be available on the Investor Relations page of the Company's website.

The conference call will be recorded and will be available for replay within one hour of completion of the live call and can be accessed following the same link as the live call.

ABOUT MATRIX SERVICE COMPANY

Matrix Service Company (Nasdaq: MTRX) is a leading heavy industrial contractor that engineers, constructs, and maintains critical energy, power, and industrial infrastructure. Our commitment to safety, quality, and integrity has earned the Company a leadership position in providing infrastructure solutions across multiple end markets. Our work is foundational to helping our energy, power, and industrial clients achieve their objectives, positively impact quality of life through the products they provide

and improve the efficiency and resilience of their critical infrastructure. We pride ourselves on our commitment to our culture and core values, offering an inclusive and respectful work environment, and being certified as a Great Place To Work®.

The Company maintains its principle executive offices in Houston, Texas with offices located throughout the United States and Canada, as well as Sydney, Australia, and Seoul, South Korea. The Company reports its financial results in three key operating segments: Storage and Terminal Solutions, Utility and Power Infrastructure, and Process and Industrial Facilities.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-09-03_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

Overview

Significant period to period changes in revenue, gross profits and operating results between fiscal 2026 and fiscal 2025 are discussed below on a consolidated basis and for each segment. A discussion of results of operations changes between fiscal 2025 and fiscal 2024 is included in Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations of our Annual Report on Form 10-K for the year ended June 30, 2025, which was filed with the SEC on September 10, 2025.

Matrix Service Company

Results of Operations

(In thousands)

Operational Update

Effective July 1, 2026, Shawn P. Payne assumed the role of President and Chief Executive Officer. His appointment reflects the Board's commitment to improving performance and delivering sustainable growth and profitability.

While we believe Matrix is well positioned to benefit from significant investment across its core and emerging markets, the Company's historical results have not consistently reflected the strength of its capabilities, customer relationships, and market opportunities. To address this, Mr. Payne led the development and implementation of Matrix's WIN, EXECUTE, DELIVER strategic framework, which is designed to accelerate growth, strengthen project execution, enhance organizational efficiency, and deliver sustainable profitability.

Under his leadership, Matrix is focused on converting its competitive advantages into stronger financial performance, improved operational outcomes, and long-term shareholder value.

Under our Win strategy, we continue to focus on securing projects that align with our capabilities, experience, and demonstrated track record of execution. We are focused on growing and diversifying our revenue base through expansion into attractive end markets, broadening relationships with existing customers, and accelerating new customer acquisition efforts across North America. We are pursuing opportunities across our traditional energy and industrial infrastructure markets, including LNG and NGL storage and terminal infrastructure, while selectively expanding into attractive growth markets such as power generation, utility infrastructure, data center-related power infrastructure, and mining and minerals. We believe demand in these markets is supported by increasing domestic electricity demand, growth in data center development, investment in power generation and related infrastructure, and continued demand for critical minerals essential to energy, technology, defense, and AI-related infrastructure. We are also expanding our geographic reach across strategically important regions and pursuing additional construction-only opportunities that complement our full-service capabilities and broaden the range of project delivery models we offer customers. We believe these efforts, combined with our focus on strengthening existing customer relationships and expanding our customer base, contributed to fiscal 2026 revenue growth of 14% to $873.6 million compared to $769.3 million in fiscal 2025.

Under our Execute strategy, our focus remains on delivering projects safely, efficiently, and with a high degree of quality while strengthening profitability and operational performance. During fiscal 2026, we advanced a variety of initiatives designed to improve project execution and drive greater consistency across the enterprise, including enhancing project proposal and contracting discipline, strengthening project controls and change management processes, improving engineering and construction execution, reinforcing quality management systems, and further developing our safety culture and performance. We also continued efforts to streamline internal processes, refine organizational workflows, support continuous improvement initiatives across the enterprise, and reinforce accountability throughout the organization with a continued focus on execution, performance, and measurable outcomes. We believe these initiatives contributed to improved project outcomes and operating performance, as evidenced by an increase in gross margin to 7.3% in fiscal 2026 from 5.2% in fiscal 2025.

Under our Deliver strategy, we remain committed to converting profitable growth and operational improvements into sustainable value creation for shareholders. During fiscal 2026, we continued to benefit from actions taken to simplify the organization, streamline operations, and create a flatter and more efficient operating structure. These efforts contributed to a more efficient operating structure and improved performance across the enterprise. As a result, selling, general and administrative expenses declined 11% to $63.6 million in fiscal 2026 compared to $71.2 million in fiscal 2025. Combined with revenue growth and improved profitability, we believe these results demonstrate meaningful progress in executing our strategy, strengthening financial performance, and positioning the Company to pursue both organic and acquisition-related growth opportunities. Supported by a strong balance sheet and liquidity, we believe Matrix remains well positioned to create sustainable value for all stakeholders.

Backlog

We define backlog as the total dollar amount of revenue that we expect to recognize as a result of performing work that has been awarded to us through a signed contract, limited notice to proceed ("LNTP") or other type of assurance that we consider firm. The following arrangements are considered firm:

• fixed-price awards;

• minimum customer commitments on cost plus arrangements; and

• certain time and material arrangements in which the estimated value is firm or can be estimated with a reasonable amount of certainty in both timing and amounts.

For long-term maintenance contracts with no minimum commitments and other established customer agreements, we include only the amounts that we expect to recognize as revenue over the next 12 months. For arrangements in which we have received a LNTP, we include the entire scope of work in our backlog if we conclude that the likelihood of the full project proceeding has a high probability. For all other arrangements, we calculate backlog as the estimated contract amount less revenue recognized as of the reporting date. Backlog differs from the amount of our remaining performance obligations, which are described in Note 2 - Revenue in the notes to the audited consolidated financial statements. Differences are due primarily to the inclusion within our backlog of estimates of future revenue under long-term maintenance contracts; future revenue for the full scope of work for certain arrangements where we have received an LNTP; and future revenue for arrangements where we have received assurance that we consider firm, but the associated contract has not been fully executed.

The following table provides a summary of changes in our backlog for fiscal 2026:

Storage and Terminal Solutions | Utility and Power Infrastructure | Process and Industrial Facilities | Total
(In thousands)
Backlog as of June 30, 2025 | 770,095 | 346,384 | 265,629 | 1,382,108
Project awards | 329,360 | 126,977 | 185,324 | 641,661
Other adjustment (2) | — | (44,239) | (152,720) | (196,959)
Revenue recognized | (458,296) | (283,390) | (131,946) | (873,632)
Backlog as of June 30, 2026 | 641,159 | 145,732 | 166,287 | 953,178
Book-to-bill ratio (1) | 0.7x | 0.4x | 1.4x | 0.7x

(1) Calculated by dividing project awards by revenue recognized.

(2) Previous project awards removed from backlog. During the first quarter of fiscal 2026, backlog was adjusted to reflect the removal of two projects. Backlog in the Utility and Power Infrastructure segment was impacted by the removal of an award originally added to backlog in the fourth quarter of fiscal 2025. Our unwillingness to accept an increased risk profile caused the client to change their award decision. Our backlog in the Process and Industrial Facilities segment was impacted by the removal of an award originally added to backlog in the third quarter of fiscal 2023. The project was removed from backlog as the ultimate customer is now planning to change the project execution and sourcing strategy for the project. While we ultimately may perform some of this work, we determined inclusion of the award in backlog was no longer appropriate.

In the Storage and Terminal Solutions segment, we booked $329.4 million of project awards during fiscal 2026. Project awards included a large award for the construction of the balance of plant supporting a dual service full containment storage tank, and an award for the construction of an LNG tank. This segment includes significant opportunities for storage infrastructure projects related to natural gas, LNG, ammonia, NGLs and other forms of low carbon energy. We believe LNG, NGLs and ammonia projects in particular will be key growth drivers for this segment. Bidding activity in these markets has been strong and we expect that to continue.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-09-03_item1_business.md)

Item 1. Business

BUSINESS

We began operations in 1984 as an Oklahoma corporation under the name of Matrix Service. In 1989, we incorporated in the State of Delaware under the name of Matrix Service Company, and in 1990 we began trading on the NASDAQ exchange. We provide engineering, fabrication, construction, and maintenance services to support critical energy infrastructure and industrial markets. We maintain regional offices throughout the United States, Canada and other international locations, and operate through separate union and non-union subsidiaries.

Our principal executive offices are located at 15333 JFK Blvd., Ste. 400, Houston, TX, 77032. Unless the context otherwise requires, all references herein to "Matrix Service Company", "Matrix", the "Company" or to "we", "our", and "us" are to Matrix Service Company and its subsidiaries.

Our purpose is to create long-term value for our employees, business partners, shareholders and communities. We are committed to fulfilling our purpose by striving to be a profitable, innovative, and growth-oriented company of choice for engineering, constructing, and maintaining essential energy and industrial infrastructure that delivers its services safely, with high quality, and on time, resulting in strong customer relationships.

Through our zero-incident safety culture, commitment to execution excellence and highly skilled workforce, we share one goal: to deliver the best to our customers, shareholders, employees and people across the globe who rely on the infrastructure we help design, build and maintain.

REPORTABLE SEGMENTS

We operate our business through three reportable segments:

• Storage and Terminal Solutions : delivers integrated engineering, procurement and construction ("EPC") services, along with repair, maintenance and fabrication services for bulk liquid, cryogenic, and refrigerated storage and terminal facilities supporting both traditional and emerging energy markets, including LNG, NGLs, petroleum products, chemicals, hydrogen, and ammonia. We also manufacture and sell specialty, precision-engineered tank products, including geodesic domes, aluminum internal floating roofs, floating suction and skimmer systems, roof drain systems and floating roof seals.

• Utility and Power Infrastructure : delivers comprehensive construction, maintenance, upgrades and fabrication services for power generation facilities and power infrastructure systems for a variety of customers, including public and private utilities, energy producers and data center customers. We also deliver integrated EPC, fabrication, and upgrade services for LNG peak shaving facilities.

• Process and Industrial Facilities : delivers engineering, construction, maintenance, and repair services across diverse heavy industrial and energy transition markets, including midstream and downstream energy, chemicals, mining and minerals, renewable fuels, and hydrogen. We also engineer and construct highly specialized infrastructure, notably thermal vacuum test chambers for the aerospace and defense sectors.

STRATEGIC PRIORITIES

Our strategy is centered on creating long-term shareholder value through three strategic priorities: Win, Execute, and Deliver.

Win | Our WIN strategy focuses on growing and diversifying our revenue base by securing projects across legacy, new, and re-emerging North American markets. We are capitalizing on strong demand in our traditional LNG and NGL infrastructure markets while actively expanding into high-growth sectors, particularly power generation for data centers and the mining of critical minerals essential to technology and defense. To provide our clients greater flexibility across diverse project delivery models, we are also accelerating growth in our construction-only services business.
Beyond our specific market focus, we are broadening our geographic reach and elevating our strategic account management to deepen existing relationships and drive new customer acquisition. Collectively, these targeted initiatives, paired with our improved speed-to-market and lower cost structure, will strengthen our backlog, expand our market share, and drive sustainable, profitable organic growth.
Execute | Execution is where our reputation is earned, relying on our absolute commitment to delivering high-quality projects safely, on time, and on budget. Through recent organizational streamlining, our operations teams are now entirely dedicated to the bidding and execution of work, backed by an enterprise-wide culture of accountability where every leader and division is focused on measurable performance.
To drive consistent operational excellence, we are implementing targeted, full-lifecycle improvement initiatives across the organization. By refining our project proposal and contracting discipline, improving engineering and construction processes, and reinforcing our safety, change, and quality management systems, we are structurally improving project outcomes and delivering greater value to our clients and shareholders.
Deliver | We are committed to translating profitable growth and operational performance into sustainable value creation for our shareholders and other stakeholders. Through disciplined capital allocation, operational efficiency, strategic investment in our people and systems, and a balanced approach to both organic and acquisition-related growth opportunities, we seek to generate consistent financial performance and long-term shareholder value.
Our strategic framework aligns the organization around common objectives, supports disciplined execution, and promotes accountability across the enterprise. Supported by a strong balance sheet, liquidity, and a focus on operational excellence, we believe we are well positioned to execute our strategy and pursue long-term growth opportunities.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-09-03_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-09-03_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-09-03_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-09-02_2-02-results.md, 10-K_2026-09-03_item7_mdna.md, 10-K_2026-09-03_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
