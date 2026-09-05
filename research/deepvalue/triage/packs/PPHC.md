# Triage pack — PPHC · Public Policy Holding Company, Inc.

_Generated 2026-09-05 00:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** PPHC · **Name:** Public Policy Holding Company, Inc.
- **CIK:** 0001903508
- **SIC:** 8742 — Services-Management Consulting Services
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/PPHC

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Public Policy Holding Company, Inc.
- **CIK:** 1,903,508 · **SIC:** 8742 (Services-Management Consulting Services) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 11.24 |
| mktcap | $339.6M |
| ev | $335.0M |
| ev_ebit | n/a |
| fcf | $24.8M |
| fcf_yield | 7.3% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -25.2% |
| net_debt | -$4.6M |
| net_debt_ebit | n/a |
| cash | $36.9M |
| ltd | $32.3M |
| equity | $110.9M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $186.5M |
| revenue_prior | $149.6M |
| rev_growth | 24.7% |
| rev_growth_note | share count +24.5% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | n/a |
| ebit | -$33.9M |
| net_income | -$39.0M |
| cfo | $24.8M |
| capex | $11k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 24.5% |
| share_chg_src | us-gaap:CommonStockSharesOutstanding |
| shares | 30,216,533 |
| shares_py | 24,017,599 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | n/a |
| r6m | -9.2% |
| off_52w_high | -23.1% |
| adv20 | $1.1M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.61 |
| r_ev_ebit | 0.00 |
| r_roic | 0.05 |
| r_rev_growth | 0.87 |
| r_buyback | 0.06 |
| score | 0.32 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q2I |
| shares_period | CY2026Q2I |
| shares_py_period | CY2024Q4I (CommonStockSharesOutstanding) |
| capex_missing | False |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 393 |

**Screen rationale:** revenue +24.7% BUT share count +24.5% yoy — growth may be acquisition/issuance-driven, not organic


## 3. Share count trend

- Shares outstanding: **30,216,533** (CY2026Q2I) vs **24,017,599** prior year (CY2024Q4I (CommonStockSharesOutstanding))
- Change: **24.5%** — dilution / growing count
- Source concept: `us-gaap:CommonStockSharesOutstanding`
- **Flag:** share count +24.5% yoy — growth may be acquisition/issuance-driven, not organic

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-03 among the 6 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 8,829 sh / $96,553 -> net $-96,553 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 12 (open-market buys 0, sales 5).

| code | rows |
|---|---|
| A | 7 |
| S | 5 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-10_2-02-results.md)

_Extraction: started at the first release heading, 'Q2 2026 Financial Highlights'; skipped 2 cover-page block(s) and 12 forward-looking-statement block(s); 9 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (pphc-earningsreleasex2026q.htm)

Q2 2026 Financial Highlights

• Revenue increased 7.3% over Q2 2025 to $52.1 million

• Organic revenue growth of 3.9% over Q2 2025

• GAAP net loss of $3.7 million, an improvement of 34.8% compared to $5.7 million in Q2 2025

• Adjusted EBITDA of $12.3 million, down 4.4% over Q2 2025, achieved at a 23.5% margin; — reflecting a particularly strong prior-year comparable period, incremental public company costs incurred following the January 2026 U.S. IPO, and, to a lesser extent, a shift in business mix

• Adjusted Net Income of $10.6 million, down 11.0% over Q2 2025

• GAAP basic and diluted loss per share of $0.19 an improvement as compared to $0.44 in Q2 2025

• Adjusted EPS, fully diluted of $0.34 compared to $0.45 in Q2 2025, reflecting the higher share count following January 2026 U.S. IPO

H1 2026 Financial Highlights

• Revenue increased 16.3% over H1 2025 to $102.3 million

• Organic Revenue growth of 4.4% over H1 2025

• GAAP Net Loss of $15.2 million compared to $16.3 million in H1 2025

• Adjusted EBITDA of $23.4 million, up 9.3% over H1 2025, achieved at a 22.9% margin

• Adjusted Net Income of $17.9 million, up 15.3% over H1 2025

• GAAP Basic and diluted loss per share of $0.68 an improvement as compared to $1.06 in H1 2025

• Adjusted EPS, fully diluted of $0.59 compared to $0.60 in H1 2025, reflecting the higher share count following the January 2026 U.S. IPO

Adjusted EBITDA, Adjusted EBITDA margin, Adjusted EBITDA Incl. M&A expense, Adjusted net income, Adjusted EPS, fully diluted, Organic Revenue Growth and Adjusted Free Cash Flow, are non-GAAP financial measures, as defined and reconciled to the nearest related GAAP measure below.

Stewart Hall, CEO of PPHC, commented:

"Our performance in the first half of 2026 demonstrates the strength of the platform we have built. Our clients operate in an increasingly complex political, regulatory and reputational environment; one in which swift access to senior, integrated counsel across multiple spheres of influence matters more than ever. Our strategy of building a diversified yet

complementary group of firms, offering premier counsel across key US and European markets, differentiates PPHC and continues to win us high-value mandates.

"The first half reflected that positioning, with H1 revenue and profit growth year-over-year and continued momentum across the business. Our revenue base remains highly diversified, and we ended the period serving approximately 1,500 clients, including representations of approximately half of the Fortune 100. We now cover every area in strategic communications across our key global markets, providing a strong foundation for further organic growth. At the same time, our pipeline of acquisition opportunities and of senior talent remains strong. With a growing and resilient platform and an active M&A program, we enter the second half with confidence."

Roel Smits, CFO of PPHC, Commentary and Financial Guidance:

"PPHC enters the second half of 2026 from a position of financial strength. Our first-half performance reflects continued revenue growth, Adjusted EBITDA growth with margins improving sequentially from Q1 to Q2, while the proceeds from our U.S. IPO have enhanced our ability to execute on our acquisition strategy. We continue to manage the business back towards our 25% Adjusted EBITDA margin target as recently acquired businesses scale and as we absorb the first full year of U.S. public company costs. We remain focused on balancing investment in future growth with profitability, and we are pleased to raise our full-year guidance to reflect the contribution from acquisitions completed and announced during the year. With a strong balance sheet, recurring client relationships and a robust acquisition pipeline in North America, UK, and mainland Europe. We believe PPHC is well positioned to continue creating value for shareholders."

Financial Outlook

For full year 2026, PPHC is raising its guidance to reflect the expected in-year contribution of the acquisitions completed and announced in YTD 2026:

• Revenue in the range of $213 million to $216 million (previously $205 million to $209 million)

• Adjusted EBITDA in the range of $48.5 million to $50.5 million (previously $46 million to $48 million), reflecting an adjusted margin between 22.5% and 23.5% (previously 22% to 23%)

• Organic Revenue Growth of approximately 5%, unchanged

The increase in guidance is attributable to completed and announced acquisitions; the Company's outlook for the underlying business is unchanged. Guidance continues to exclude the impact of any future acquisitions. The Company does not provide a reconciliation of forward-looking non-GAAP measures to the most directly comparable GAAP measures because the reconciling items, including acquisition-related charges, share-based accounting charges and changes in the fair value of contingent consideration, cannot be reasonably predicted without unreasonable effort.

Operational Highlights

• Significant progress in line with the Group's stated growth strategy, with earnings-accretive acquisitions and senior hires adding complementary services and expertise for the Group's international client base:

• Completed the acquisition of Westminster Policy Partners Limited ("WPI") on April 1, 2026, expanding Group-wide capabilities in economic and policy research and providing cross-referral revenue opportunities.

• Post-period end, completed the acquisition of Tancredi Intelligent Communication Ltd ("Tancredi") on July 1, 2026, adding financial, corporate and litigation communications expertise as the first member of TrailRunner Group, the Group's corporate and financial communications platform, and expanding international operations in London and Milan.

• Post-period end, completed the acquisition of The Advocacy Partners on August 1, 2026, one of Florida's pre-eminent government relations firms, completing a coast-to-coast state government relations affairs footprint.

• Strengthened senior talent with significant new hires in Government Relations, Corporate Communications, and Public Affairs.

• Revenue diversification further enhanced with the top 10 Group clients representing 7.5% of revenue in H1 2026 (H1 2025: 9.4%). Revenue mix by segment also diversified further, with the Corporate Communications & Public Affairs segment, the Group's second largest reporting segment, growing to represent 35.7% of total revenue in H1 2026 (H1 2025: 32.0%).

• Grew the client base to approximately 1,500, including representations of approximately half of the Fortune 100 and many more via trade associations, reflecting continued high retention and new-business generation.

• The Group ended H1 2026 with 476 employees (H1 2025: 447).

2026 Segment Results

• Government Relations Consulting grew at 9.8% for H1 2026, as compared to H1 2025 as a consequence of continued organic growth of 6.3% in tandem with the acquisitions of Pine Cove Strategies, LLC ("Pine Cove") (completed July 11, 2025) and WPI (completed April 1, 2026). The margin of Segment Adjusted pre-bonus EBITDA marginally increased to 46.7%, reflecting the consistent pricing of retainer contracts both at U.S. Federal and State level.

• Corporate Communications & Public Affairs Consulting increased by 29.5% for H1 2026, as compared to H1 2025, driven by the impact of the acquisitions of TrailRunner International, LLC ("TrailRunner") (completed April 1, 2025) and WPI (completed April 1, 2026), offset by slow organic growth, which was down 0.9%. The margin of Segment Adjusted pre-bonus EBITDA decreased by 0.9pts to 24.8% in H1 2026, reflecting the inclusion of acquired revenues, representing operating margins that are lower than the Group's average.

• Compliance and Insights Services continued its strong growth at 12.8% for H1 2026, as compared to H1 2025 (reported and organic) as a result of high renewal rates, price increases, and new client wins, reflective of a unique and high value-added offering. The margin of Segment Adjusted pre-bonus EBITDA was 50.2%, reflecting the strong pricing of subscription-based contracts in this area, in combination with the increased use of technology in servicing our clients.

Conference Call Webcast Information

PPHC management will host a conference call to discuss the Company's financial results today at 4:30 p.m. Eastern Time. The call will be led by Stewart Hall, Chief Executive Officer, Roel Smits, Chief Financial Officer, and Thomas Gensemer, Chief Strategy Officer.

Date: Monday, August 10, 2026

Time: 4:30 p.m. Eastern Time

Webcast: Participants may access the conference call via live webcast at https://edge.media-server.com/mmc/p/mxsggmoi

Dial-in: To participate via telephone, please register in advance and receive a unique PIN at https://register-conf.media-server.com/register/BI39227e4481c34165806143b77781608f

A replay of the webcast of the conference call will be available on the Investor Relations section of the Company's website at investors.pphcompany.com.

This announcement contains inside information under the UK Market Abuse Regulation. The person responsible for arranging for the release of this announcement on behalf of the Company is Roel Smits, CFO.

About PPHC

Incorporated in 2014, PPHC is a global strategic communications platform that supports clients in enhancing and defending their reputations, advancing policy objectives, managing regulatory risk, and engaging with federal and state-level policymakers, stakeholders, media, and the public.

Engaged by approximately 1,500 clients, including companies, trade associations and non-governmental organizations, PPHC is active in all major sectors of the economy, including healthcare and pharmaceuticals, financial services, energy, technology, telecoms and transportation.

With operations across the United States and internationally, PPHC's services include government relations, public affairs and corporate communications, research and analytics, digital advocacy campaigning, and compliance support. The Company's shares are admitted to trading on the Nasdaq Global Market and on AIM, a market operated by the London Stock Exchange, under the ticker symbol "PPHC".

For more information, visit www.pphcompany.com.

Financial Review

Certain monetary amounts, percentages and other figures included elsewhere in this earnings release have been subject to rounding adjustments. Accordingly, figures shown as totals in certain tables or charts may not be the arithmetic aggregation of the figures that precede them, and figures expressed as percentages in the text may not total 100% or, as applicable, when aggregated may not be the arithmetic aggregation of the percentages that precede them.

Adjusted Profit & Loss Statement

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-31_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

Overview

Public Policy Holding Company, Inc. ("we," "us," "our," "PPHC," or the "Company") through our wholly-owned subsidiaries, operates a portfolio of firms that offer global strategic communications services, including government relations, corporate communications and public affairs. Engaged by over 1,400 clients, including companies, trade

associations and non-governmental organizations, we are active in all major sectors of the economy, including healthcare and pharmaceuticals, financial services, energy, technology, telecoms and transportation. Our services help clients to enhance and defend their reputations, advance policy goals, manage regulatory risk and engage with federal and state-level policy makers, stakeholders, media and the public in multiple jurisdictions and with diverse and complementary capabilities.

Since our inception in 2014, we have acquired and integrated numerous businesses specializing in key facets of strategic communications, including government relations, public affairs, research, crisis management, investor relations and creative communications delivery. Under the PPHC holding company, we now operate as 12 member companies in the United States ("US" or "U.S.") and the United Kingdom ("UK"), with expanding reach into Europe and parts of Asia and the Middle East. These 12 member companies include Crossroads, Forbes Tate, Seven Letter, O'Neill, Alpine, KP, MultiState, Concordant, Lucas, Pagefield, TrailRunner, and Pine Cove.

We operate in large growing markets that we believe provide us significant opportunity for continued growth. We estimate our total addressable market ("TAM") in 2024 was in excess of $20.0 billion, comprising $4.4 billion of disclosed federal lobbying expenditure, an estimated $2.2 billion of partially disclosed total US state-based lobbying expenditure, an estimated $5.6 billion global public affairs spend, and an estimated $8.4 billion global corporate communications spend. The latter, which covers corporate, crisis, and financial communications, became part of our offering with the 2025 acquisition of TrailRunner. We believe this segment may be larger than $8.4 billion, though it is difficult to quantify given that industry metrics often combine it with broader public relations categories—such as marketing communications—that PPHC does not provide.

We have built a scalable platform which also creates cross-selling and referral opportunities. We provide our companies with a scalable platform for growth, providing uniform and efficient financial infrastructure, legal services, human resources, compliance and administration at the parent company level. We also incentivize cross-company selling, talent referrals and effective conflict management remedies across our client portfolio.

We have grown our geographical reach and practice capabilities to provide clients a full range of services through multiple member companies. Our evolution to date is the result of a careful and methodical strategy to build a unique service platform to simplify and more effectively address global client challenges and opportunities in an increasingly fragmented and accelerated policy and communications landscape. This growth strategy is predicated on adding both geographic reach for clients and a complete set of asset capabilities to bring the client the ability to synthesize and simplify the best in class practices to address policy and reputational issues. Leveraging deep policy and issue expertise derived from our original core government relations member companies, first established in 2014, we now work with clients to provide the full-spectrum of strategic communications, including government affairs, public affairs, issues and crisis communications, financial communications and corporate and institutional reputation management needs.

Building on the globalization of public policy and reputation challenges, our founders and many of our senior managers operate in Washington, DC, and have past careers and/or close professional ties to the US executive branch, Congress and regulatory authorities over a period of more than 30 years. Other leaders operate principally at the state or regional level, drawing on decades of experience, deep community ties and relationships with key stakeholders in key markets, including California, Texas and New York. With the acquisition of Pagefield in June 2024 and TrailRunner in April 2025, we have expanded our operations to London, Shanghai, Abu Dhabi and Dubai, giving us truly global reach. We continue to look for opportunities to broaden the geographic scope of our services both domestically and abroad.

Adding complementary practice capabilities to augment geographic coverage, our business comprises three reporting segments—Government Relations Consulting, Corporate Communications & Public Affairs Consulting and Compliance and Insights Services—corresponding to the different types of strategic communications services our member companies provide to our clients:

• Government Relations Consulting services include advocacy, strategic guidance, political intelligence and issue monitoring at the United States federal and state levels and internationally through our offices in London;

• Corporate Communications & Public Affairs Consulting services include crisis communications, community relations, social and digital media, public opinion research, branding and messaging, relationship marketing and litigation support; and

• Compliance and Insights Services include lobbying compliance services and legislative tracking.

As of December 31, 2025, we had approximately 1,400 active client relationships, which were highly diversified with the top 10 PPHC clients representing 9.2% of revenue in 2025 versus 8.7% at the end of the year ended December 31, 2024. We have no single client representing more than 2.1% of overall revenues for the year ended December 31, 2025. Our client base includes corporate, trade association and non-profit client organizations across a range of industries. Our client portfolio includes clients in the healthcare and pharmaceuticals, defense and aerospace, agriculture, financial services, energy, technology, telecom and transportation sectors. We also have a track record of high client retention, with an average annual renewal rate of approximately 77.4% and an average revenue retention rate of 85.5% between 2020 to 2025.

From January 1, 2018 to December 31, 2025, we achieved revenue growth of 27.6% CAGR, with organic revenue growth of 15.0% CAGR over the same period.

Financial Results

• In the year ended December 31, 2025, Revenue increased by 24.7% to $186.5 million, with organic growth contributing 6.2% and the balance driven by four acquisitions made in 2024 and 2025.

• GAAP Net losses increased from $(24.0) million in 2024 to $(39.0) million in 2025, the losses primarily being the result of a $29.6 million share based accounting charge stemming from the UK IPO and the treatment of acquisitions in our accounts. The increase in loss in 2025 was driven by a $9.7 million increase in post-combination compensation charges primarily stemming from the Lucas, Pagefield, TrailRunner and Pine Cove acquisitions, a $9.1 million impairment charge related to Pagefield's intangibles and goodwill, and an increase of $3.2 million in the change in fair value of contingent consideration.

• Adjusted EBITDA was at record level of $45.4 million, up 17.7% as compared to prior year, achieved at a 24.3% margin.

• Adjusted Net Income of $36.6 million was up 32.1% as compared to prior year that includes an increase in finance costs offset by a more favorable effective tax rate.

• Adjusted EPS fully diluted of $1.39 was up $0.27 or 24.7%, with fully diluted share count increasing by 5.9%.

• PPHC's cash generation remains robust with net cash flows provided by operating activities increasing by $8.4 million to $24.8 million while Adjusted Free Cash Flow increased to $36.9 million as compared to $22.2 million in 2024, reflecting strong cash conversion helped by diligent working capital management.

Years ended December 31,
2025 | 2024 | $ Change | % Change
Revenue | 186.5 | 149.6 | 37.0 | 24.7 | %
Net loss | (39.0) | (24.0) | (15.0) | 62.5 | %
Adjusted EBITDA | 45.4 | 38.6 | 6.8 | 17.7 | %
Adjusted EBITDA margin | 24.3% | 25.8% | (1.5) | pts
Adjusted net income | 36.6 | 27.7 | 8.9 | 32.1 | %
Basic and diluted loss per share | (2.37) | (2.34) | (0.03) | (1.3) | %
Adjusted EPS fully diluted | 1.39 | 1.11 | 0.27 | 24.7 | %
Dividend paid, per share | 0.344 | 0.702 | (0.358) | (51.0) | %
Cash and cash equivalents at end of period | 20.4 | 14.5 | 5.9 | 40.6 | %
Net debt at period-end | (26.6) | (17.5) | (9.0) | 51.6 | %
(1) Refer to the Non-GAAP Financial Measures section below for our definition of the non-GAAP measures.

Recent Developments

Refer to Item 8. Financial Statements and Supplementary Data, Note 19 - Subsequent Events of this Form 10K.

Comparison of the years ended December 31, 2025 and December 31, 2024

Results of Operations

Amounts presented in the tables below are in millions, except percentages, share and per share data and unless otherwise noted.

The table below presents the detailed components of our income statement:

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-31_item1_business.md)

ITEM 1. BUSINESS

Overview

Our mission is to be the preeminent provider of global strategic communications by uniting a diverse group of leading government relations, corporate communications and public affairs specialists around the world for the collective success of our clients, employees, and shareholders.

Founded by veteran advisors with decades of experience in Washington, D.C.'s public policy and government relations landscape, we have grown and diversified our global communications advisory business through targeted acquisitions and organic growth. We designed our business to address the growing complexity and costs facing major corporate and non-profit entities in managing increasingly intricate and interdependent public policy and reputational challenges, and we now help more than 1,400 clients around the world navigate today's complex mosaic of stakeholders across the full spectrum of corporate affairs. Our clients include nearly half of the Fortune 100.

Across our growing portfolio, our specialized firms offer global strategic communications services, including government relations, corporate communications, public affairs, research, crisis management, financial communications and investor relations, and creative communications delivery. We are active in all major sectors of the economy, including healthcare and pharmaceuticals, asset management and financial services, energy, technology, telecoms and transportation. Our diverse and complementary services help clients enhance, fortify and defend their reputations, advance corporate strategy, manage regulatory risk and opportunities, and maintain productive, ongoing engagement with their most important stakeholders including federal- and state-level policy makers, investors, employees, customers, the media, and the general public. We do this in multiple jurisdictions and with our diverse and complementary capabilities.

Our business comprises of three reporting segments—Government Relations Consulting, Corporate Communications & Public Affairs Consulting and Compliance and Insights Services—corresponding to the different types of strategic communications services our member companies provide to our clients:

Government Relations Consulting services (which are also commonly referred to as "lobbying") include advocacy, strategic guidance, political intelligence and issue monitoring at the US federal and state levels and in the United Kingdom through our offices in London;

Corporate Communications & Public Affairs Consulting services include crisis communications, financial communications and investor relations, litigation support, community relations, social and digital media, public opinion research, branding and messaging, and relationship marketing, across the United States and internationally through our offices in London, Shanghai, Abu Dhabi, and Dubai; and

Compliance and Insights Services include lobbying compliance services and legislative tracking.

Importantly, as distinct from legacy branded competitors in our industry who have sought to be all-in-one providers of strategic communications services to their clients, we deliver complementary strategic communications services through stand-alone firms. Each of our firms is recognized for excellence in its respective area of expertise, and is incentivized to collaborate and to partner with each of our other firms while maintaining a strong focus on its specialized services. Our business model allows us to deliver both the scale and reach of those all-in-one providers and also the higher standards of quality, service, creativity, and nimbleness that traditionally have been the domain of smaller boutiques. We seek to eliminate for clients the traditional trade-off between scale and quality, and our growth demonstrates that our business model is well-suited to the needs and preferences of modern clients.

Since our inception in 2014, we have acquired and integrated numerous businesses specializing in key facets of the global strategic communications market. Under our holding company, we now operate as 12 member companies in the United States and the United Kingdom, with expanding reach into Europe and parts of Asia and the Middle East. Our 12 member companies (together with PPHC, the "Company") include Crossroads Strategies, LLC ("Crossroads"), Forbes Tate Partners LLC ("Forbes Tate"), Blue Engine Message & Media, LLC (doing business as Seven Letter) ("Seven Letter"), O'Neill & Partners, LLC (doing business as O'Neill & Associates) ("O'Neill"), Alpine Group Partners, LLC ("Alpine"), KP Public Affairs LLC ("KP"), MultiState Associates, LLC ("MultiState"), Concordant LLC ("Concordant"), Lucas Public Affairs, LLC ("Lucas"), Pagefield Communications Limited ("Pagefield"),TrailRunner International, LLC ("TrailRunner"), and Pine Cove Strategies, LLC ("Pine Cove").

We announced the earnings-accretive acquisition of Texas-based TrailRunner for initial consideration of $33.0 million plus potential earnout payments in January 2025. Closing occurred on April 1, 2025. TrailRunner is a Texas headquartered global strategic communications advisory firm that operates with a global team across offices in Texas, New York,

Nashville, and Northern California, London, Shanghai, Abu Dhabi, and Dubai. We announced the earnings-accretive acquisition of Pine Cove for initial consideration of $3.0 million in July 2025 plus potential earnout payments. Pine Cove is a strategic consulting firm that serves as a long-term partner to clients ranging from start-ups to established businesses and Fortune 100 companies. It advises and supports clients in navigating regulatory and complex business challenges.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-31_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-31_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-31_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-10_2-02-results.md, 10-K_2026-03-31_item7_mdna.md, 10-K_2026-03-31_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
