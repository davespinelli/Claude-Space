# Triage pack — YEXT · Yext, Inc.

_Generated 2026-09-04 13:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** YEXT · **Name:** Yext, Inc.
- **CIK:** 0001614178
- **SIC:** 7374 — Services-Computer Processing & Data Preparation
- **Fiscal year end (MM-DD):** 01-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/YEXT

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Yext, Inc.
- **CIK:** 1,614,178 · **SIC:** 7374 (Services-Computer Processing & Data Preparation) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 6.44 |
| mktcap | $645.6M |
| ev | $706.5M |
| ev_ebit | 15.9x |
| fcf | $53.3M |
| fcf_yield | 8.3% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 36.5% |
| net_debt | $60.9M |
| net_debt_ebit | 1.4x |
| cash | $86.8M |
| ltd | $147.7M |
| equity | $35.7M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $446.6M |
| revenue_prior | $421.0M |
| rev_growth | 6.1% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $44.5M |
| net_income | $38.0M |
| cfo | $55.8M |
| capex | $2.6M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -18.1% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 100,248,116 |
| shares_py | 122,397,716 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -37.4% |
| r6m | 16.9% |
| off_52w_high | -28.9% |
| adv20 | $6.2M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.66 |
| r_ev_ebit | 0.56 |
| r_roic | 0.96 |
| r_rev_growth | 0.55 |
| r_buyback | 0.98 |
| score | 0.74 |

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
| rank | 38 |

**Screen rationale:** high ROIC 36.5%; buying back stock -18.1%


## 3. Share count trend

- Shares outstanding: **100,248,116** (CY2026Q2I) vs **122,397,716** prior year (CY2025Q2I)
- Change: **-18.1%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-07** — Item 5.02 (officer / director change or comp arrangement): On July 7, 2026 , the board of directors (the "Board") of Yext, Inc. (the "Company") approved an increase in the number of authorized directors from seven to eight and elected Cynthia Paul as a Class I member of the Board to fill the vacancy.
- **2026-06-11** — Item 5.02 (officer / director change or comp arrangement): Approval of Yext, Inc. 2016 Equity Incentive Plan, as amended, restated and extended

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 76,190 sh / $397,910 vs sells 0 sh / $0 -> net $397,910 (BUYING).
Distinct insiders buying (code P): 1. Largest buy: Englander Daniel J bought 76,190 sh @ $5.22 ($397,910) on 2026-07-13.

Form 4 filings parsed: 12; transaction rows: 31 (open-market buys 1, sales 0).

| code | rows |
|---|---|
| A | 6 |
| F | 4 |
| M | 20 |
| P | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-09-01_2-02-results.md)

_Extraction: started at the first release heading, 'Second Quarter Fiscal 2027 Results'; skipped 18 forward-looking-statement block(s); 95 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (ex991q2fy27earningsrelease.htm)

## EX-99.2 - EX-99.2 (ex992q2fy27shareholderlett.htm)

Second Quarter Fiscal 2027 Results

Revenue for the second quarter of fiscal 2027 was $111.1 million, compared to $113.1 million in the second quarter of fiscal 2026, a 2% decrease, driven by the same customer size cohort dynamics described above and consistent with our go-to-market strategy. Gross margin improved to 75.5% on a GAAP basis from 75.2% in the prior year. GAAP net income and earnings per share were $13.1 million and $0.13, respectively, and Non-GAAP net income and earnings per share were $21.2 million and $0.21, respectively. We reduced our weighted average basic share count by 19% year over year to 100.1 million. This is the first quarter to show the full effect of the tender offer we completed in the spring. Adjusted EBITDA was $34.0 million, compared to $26.4 million in the second quarter fiscal 2026, representing an Adjusted EBITDA margin of 31%.

Total ARR ended the quarter at $440.8 million. The composition of ARR continues to evolve in-line with our expectations and strategy, as customers with annual contract value of ≥$50K accounted for $405.9 million, or 92% of our ARR at the end of FY27 Q2, up 2% year over year. ARR growth from this cohort is accelerating on both a sequential and a year-over-year basis. The recovery has been gradual but consistent, and we expect our FY27 Q3 results to reflect continued positive momentum. ARR from sub-$50K customers was $34.9 million, down 22% year over year, consistent with our expectations and the plan we have previously laid out. We have refocused our go-to-

EXHIBIT 99.2

market strategy on enterprise customers, and as a result, we are not dedicating material resources to mitigate churn within our current SMB customer base. These numbers reflect the exit of customers who were a poor fit for our enterprise product. We have continued to experiment with better ways to serve SMB customers, and we will discuss our latest offerings in the platform section below.

Gross retention rate within the ≥$50K cohort improved to 90% from 89% a year ago, and net retention rate for this cohort was 98%, up from 96% in FY26 Q2. The improvement in net retention came from both components of the metric: we kept more of the revenue we started the year with, and expansion within the base widened. Combined with new customer additions, net ARR grew $6.6 million in the ≥$50K cohort over the past twelve months. The sub-$50K cohort saw net churn of $10.1 million, consistent with our deliberate shift to focus on our enterprise customers.

GoShine, Action Center, and Earned Visibility

In June, we acquired GoShine, a brand visibility platform built for the AI search era. GoShine finds what blocks a brand from appearing in AI-generated answers, then produces optimized content designed to win the questions that matter to that brand, and measures visibility over time so customers can see that it is working. Scout gives brands competitive intelligence at the level of individual locations, and the integration of GoShine - now Brand Scout - adds the brand-level view. The combination completes the visibility portfolio we have been assembling for AI search. GoShine is integrated into our platform, and we plan to pilot it with a small number of enterprise customers before making it broadly available later this year. We do not expect the financial contribution from GoShine acquired revenue to be material to our consolidated results this fiscal year.

We also launched Action Center. Intelligence that identifies a visibility gap is worth little until a marketing action closes the gap. Action Center takes the recommendations produced by Scout (now across Brand AND Hyper-local competitive intelligence) and executes them across Listings, Reviews, Pages, and Social, increasingly through agents. As described in our last letter, Scout gives customers programmatic access to our localized competitive intelligence dataset, structured for agentic consumption. Customers can run all of this workflow through our interfaces, or they can plug the same capabilities into agents they build themselves through MCP.

Our platform is rapidly evolving into a harness for Agentic Marketing. Yext Scout is the intelligence layer, gathering local and brand level granular competitive intelligence. Taking this intelligence, Scout also acts as the orchestration agent across Listings, Reviews, Social, Content generation and distribution and customer communication. The agents scale with demand, and the Action Center organizes the output. The platform continues to learn and do more of the work on its own. That is the direction of the product roadmap, and it is also the direction of the market. As discovery fragments across answer engines and conversational interfaces, the brands that win will be the ones whose data is accurate everywhere and whose response to a competitive gap is the most timely and data-driven. The bottom line is brands need best-in-class competitive intelligence that is connected to the AI action layer, and our platform is rapidly evolving into that solution.

We have written before about zero-click search, where the consumer gets what they need from the answer without visiting a website. A growing share of searches now end this way, breaking a playbook brands have run for twenty years, in which organic visibility came from optimizing pages to rank on a list of links. The engines now compose a single answer in place of that list, and they build it from whatever data and content they trust, which is why a brand's pages can rank well while the answer recommends a competitor.

The AI recommendation has to be earned. It takes accurate structured data everywhere the engines look and content worth quoting, and because answers change constantly, a brand has to know what they say about it before a competitor takes its place. This complex challenge is what we built our platform for, from the Knowledge Graph that gives the engines data they can trust to the agents in Action Center that close the gaps Scout finds. Every brand that built its visibility on the ranked list now needs to embrace this new norm, this new way customers behave, and the need grows each time a search ends without a click.

EXHIBIT 99.2

From Architecture to Shipping Product

In June, we described the enterprise market splitting into two camps: companies that want to build their own agents on clean, programmatic data and companies that want finished agents ready to deploy, and we said we would serve both. What changed this quarter is how much of that architecture became product. GoShine fills the brand-level position we committed to building, and Action Center supplies the execution layer we had described as the destination. The MCP interfaces that connect Scout, Knowledge Graph, and Yext's Action agents to customer agents are in customers' hands today.

New entrants keep arriving in AI visibility, and most of them stop at the diagnosis. Acting on a visibility gap takes an execution layer, and acting on it across thousands of locations or a global Brand takes infrastructure that can't be built overnight. What we have built over the course of fifteen years is not easy to replicate.

Much has been said about the threat to enterprise software from AI native startups. It is true, that building an interface is easier than it has ever been. However, what we are seeing is that the core business context engine (Knowledge Graph) and the decades of enterprise class infrastructure, execution agents, compliance, proprietary data, and expertise cannot be easily replicated. The advantage is shifting to companies like Yext. We have all the same AI tools at our disposal, along with the scaled and tested infrastructure, client trust and scaled distribution to make agentic marketing successful.

One thing is clear, AI has lowered the bar for building UI that works for specific clients needs. This is a shift, and a very important one. With a complete set of APIs and MCPs, we can now produce different versions of UI for the core utilities and agents we have built. As we have been discussing for the last year, our SMB cohort reflects what happens when we distribute an enterprise UI to SMB customers. We made the decision last year to focus the majority of our energy on our enterprise customers. This has accelerated churn in SMB customers using a mis-matched enterprise product UI. Now that our core platform is fully headless, we are prepared to unveil one of the focused experiments we have been working on to better serve our SMB customers - particularly the single operator, very small business cohort. We recently publicly released a working prototype of Corvo AI. This is a complete re-imagination of the UI for our core Competitive intelligence, AI Visibility, Listings, Reviews and ultimately the entire portfolio of our marketing agents - in a conversational platform that the busy business owner will be able to access through a mobile first experience and increasingly via SMS - allowing action through natural language. This experiment is now publicly available at www.askcorvo.com. We look forward to updating our view on this opportunity in future communications.

Customer Success

We saw good traction with enterprise customers in our healthcare and financial services verticals last quarter. One of the large financial institutions we serve expanded its relationship with us again. The firm has been a customer since 2012 and is one of our largest. This quarter it renewed for another two years, added our Pages product to the Listings and Reviews products it already runs, and separately renewed the Hearsay products its advisors use to engage clients. We are seeing our land and expand motion resonate with more customers as the investments we have made to extend the functionality of our platform and better integrate its components make it easier for customers to build more of their operations on it.

While land-and-expand remains a core growth driver, our expanded platform capability is increasingly enabling us to win full-scale commitments right from the start. For example, during the quarter, a middle-market customer purchased our complete platform, including services, on Day 1. This precedent-setting agreement was the first mid-market deal to combine all of our products into a single AI platform, and it shows how our product enhancements are creating a compelling platform, driving larger initial entry points across our pipeline.

We saw the same dynamics elsewhere in the quarter. One of the nation's leading academic medical centers, an existing customer, put its digital presence business through a formal RFP and awarded it to us, expanding its relationship across Listings and Reviews throughout its health system. A national insurance distributor returned to us this quarter as a boomerang customer, signing on for our Listings and Reviews products after our Scout scans made it clear how much control over the brand's presence had been lost, from location data that could not be kept

EXHIBIT 99.2

accurate across major platforms to duplicate listings that no one could fix. And the national advertising fund of one of the world's largest restaurant brands expanded with us again, purchasing additional licenses and adding a managed review response program for its stores.

Consolidation remains an effective sales motion for us. Customers tell us they want fewer vendors, a single, accountable platform. We believe we are uniquely capable of meeting this requirement. These types of deals create an outsized financial benefit due to the significantly improved retention we experience when a customer adds a new product. We expect continued success in vendor consolidation deals to be a key driver of our growth over the next several years because of our expanded and compelling platform capabilities.

Our Efficiency Journey

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-10_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

Yext empowers businesses to manage their knowledge so they can deliver relevant, actionable answers to consumer questions as well as consistent, accurate and engaging experiences to customers throughout the digital ecosystem. Our digital presence platform (also known as the Answers Platform) lets businesses structure and organize information about their brands in our Knowledge Graph (previously known as Yext Content), which is then delivered across first-and third-party websites and applications through our network of over 200 service and application providers, which we refer to as our Publisher Network. These publishers include, among others, Amazon Alexa, Apple, Bing, Facebook, Gemini, Google, OpenAI, and Yelp. Our platform powers all of our key products, including Listings, Reviews, Pages, Search, Social, Relate, and Scout, each with robust analytics capabilities for businesses to easily track performance across customer experiences. It is our mission to empower businesses to easily manage every aspect of their digital presence to make meaningful connections with their customers across every digital touchpoint.

We sell our platform throughout the world to customers of all sizes, including our enterprise, mid-size, and third-party reseller customers. In transactions with resellers, we are only party to the transaction with the reseller and are not a party to the reseller's transaction with its customer.

Revenue is a function of the number of customers, the number of licenses or capacity purchased by each customer, the package to which each customer subscribes, the price of the package and renewal rates. We offer subscriptions in a discrete range of packages, with pricing based on specified feature sets and the number of licenses managed by the customer as well as on a capacity-basis.

In August 2024, we acquired Hearsay Social, Inc., a digital client engagement platform for financial services ("Hearsay"). See Note 4 "Business Combinations" to our consolidated financial statements for additional information.

Fiscal Year

Our fiscal year ends on January 31 st . References to fiscal 2026, for example, are to the fiscal year ended January 31, 2026.

Macroeconomic Conditions

Our results of operations have been and may continue to be influenced by general macroeconomic conditions, including, but not limited to, the impact of foreign currency fluctuations, interest rates, inflation, recession risks, tariffs and other trade restrictions, geopolitical events and shifts, and changes in government administration policy positions. Fluctuations in foreign exchange rates and rising inflation have had, and may continue to have an adverse impact on our financial condition and operating results in future periods. The extent to which such disruptions will continue in future periods remains uncertain, which has had and may continue to have an adverse impact on our financial condition and operating results in future periods. We continue to be committed to our business, the strength of our platform, our ability to continue to execute on our strategy, and our efforts to support our customers.

Near-term revenues are relatively predictable as a result of our subscription-based business model. However, if the macroeconomic uncertainty continues or further increases, we may continue to experience a negative impact on existing and potential customers that may reduce, suspend or delay technology spending, request to renegotiate contracts to obtain concessions such as, extended billing and payment terms; shorten the duration of contracts; or elect not to renew their subscriptions which could materially adversely impact our business, financial condition and results of operations in future periods. Therefore, changes in our contracting activity in the near term may not be fully reflected in our results of operations and overall financial performance until future periods.

Recent Developments

On February 10, 2026, we commenced an issuer self-tender offer (the "Tender Offer") to purchase for cash up to $180.0 million in value of shares of our common stock at a price of not less than $5.75 nor greater than $6.50 per share, upon the terms and subject to the conditions described in the offer to purchase and the related letter of transmittal filed with the SEC on February 10, 2026, as each may be amended time to time. The Tender Offer was originally scheduled to expire on March 12, 2026, unless the offer was extended or terminated. On March 4, 2026, we decreased the maximum aggregate purchase price of shares to be repurchased in the Tender Offer to $140.0 million and extended the expiration date to March 18, 2026, unless further extended or earlier terminated.

On August 18, 2025, we announced that Michael Walrath, Yext's Chief Executive Officer and Chairman on the Board of Directors, submitted a non-binding proposal to acquire all outstanding shares of Yext not already owned by him at a price of $9.00 per share in cash. Our Board of Directors formed a Special Committee of independent directors to evaluate the proposal, advised by independent legal and financial advisers. On February 2, 2026, we announced that Michael Walrath, our Chief Executive Officer and Chairman of the Board of Directors, had withdrawn his previously announced non-binding proposal.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

In this section, we discuss the results of our operations for the fiscal year ended January 31, 2026 compared to the fiscal year ended January 31, 2025. For a discussion of our results of operations for the fiscal year ended January 31, 2025 compared to the fiscal year ended January 31, 2024, see Part II, Item 7, "Management's Discussion and Analysis of Financial Condition and Results of Operations" in our Annual Report on Form 10-K for the fiscal year ended January 31, 2025.

The following table sets forth selected consolidated statement of operations data for each of the periods indicated:
(in thousands) | Fiscal year ended January 31,
2026 | 2025
Revenue | 446,579 | 420,957
Cost of revenue (1) | 114,068 | 96,364
Gross profit | 332,511 | 324,593
Operating expenses:
Sales and marketing (1) | 134,765 | 174,779
Research and development (1) | 89,874 | 77,201
General and administrative (1) | 63,323 | 105,061
Total operating expenses | 287,962 | 357,041
Income (loss) from operations | 44,549 | (32,448)
Interest income | 3,856 | 6,102
Interest expense | (7,575) | (967)
Other expense, net | (704) | (745)
Income (loss) from operations before income taxes | 40,126 | (28,058)
(Provision for) benefit from income taxes | (2,255) | 110
Net income (loss) | 37,871 | (27,948)

(1) See Note 10 "Stock-Based Compensation" to our consolidated financial statements for amounts included.

The following table sets forth selected consolidated statements of operations data for each of the periods indicated as a percentage of total revenue:

Fiscal year ended January 31,
2026 | 2025
Revenue | 100 | % | 100 | %
Cost of revenue | 26 | 23
Gross profit | 74.5 | 77.1
Operating expenses:
Sales and marketing | 30 | 42
Research and development | 20 | 18
General and administrative | 14 | 25
Total operating expenses | 64 | 85
Income (loss) from operations | 10 | (8)
Interest income | 1 | 1
Interest expense | (2) | —
Other expense, net | — | —
Income (loss) from operations before income taxes | 9 | (7)
(Provision for) benefit from income taxes | (1) | —
Net income (loss) | 8 | % | (7 | %)

Note: Numbers rounded for presentation purposes and may not sum.

Fiscal Year Ended January 31, 2026 Compared to Fiscal Year Ended January 31, 2025

Revenue
Fiscal year ended January 31, | Variance
(in thousands) | 2026 | 2025 | Dollars | Percent
Revenue | 446,579 | 420,957 | 25,622 | 6 | %
Cost of revenue | 114,068 | 96,364 | 17,704 | 18 | %
Gross profit | 332,511 | 324,593 | 7,918 | 2 | %
Gross margin | 74.5 | % | 77.1 | %

Total revenue was $446.6 million for the fiscal year ended January 31, 2026, compared to $421.0 million for the fiscal year ended January 31, 2025, an increase of $25.6 million or 6%. The increase was entirely driven by the inclusion of Hearsay's revenue as a result of the acquisition which was completed on August 1, 2024. Revenue recognized from subscriptions and associated support to our platform was 94% and 93%, while revenue recognized from professional services was 6% and 7%, for the fiscal years ended January 31, 2026 and 2025, respectively.

Revenue for the fiscal year ended January 31, 2026 included a positive impact from foreign currency exchange rates of approximately $3.3 million, using a constant currency basis. We calculate constant currency by translating our current period results for entities reporting in currencies other than U.S. Dollars ("USD") into USD at the average monthly exchange rates in effect during the comparative period, as opposed to the average monthly exchange rates in effect during the current period.

The following table summarizes our revenue by sales channel for the periods presented:

Fiscal year ended January 31, | Variance
2026 | 2025 | Dollars | Percent
(in thousands)
Direct Customers | 372,485 | 346,951 | 25,534 | 7 | %
Third-Party Reseller Customers | 74,094 | 74,006 | 88 | — | %
Total Revenue | 446,579 | 420,957 | 25,622 | 6 | %

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-10_item1_business.md)

Item 1. Business

Overview

Yext, Inc. ("Yext," the "Company," "we," "us" or "our") empowers businesses to manage their knowledge so they can deliver relevant, actionable answers to consumer questions as well as consistent, accurate and engaging experiences to customers throughout the digital ecosystem. Our digital presence platform (also known as the Answers Platform) lets businesses structure and organize information about their brands in our Knowledge Graph (previously known as Yext Content), which is then delivered across first- and third-party websites and applications through our network of over 200 service and application providers, which we refer to as our Publisher Network. These publishers include among others, Amazon Alexa, Apple, Bing, Facebook, Gemini, Google, OpenAI, and Yelp. Our platform powers all of our key products, including Listings, Reviews, Pages, Search, Social, Relate, and Scout, each with robust analytics capabilities for businesses to easily track performance across customer experiences. It is our mission to empower businesses to easily manage every aspect of their digital presence to make meaningful connections with their customers across every digital touchpoint.

The digital consumer journey continues to change with the expansion of artificial intelligence ("AI") and large language models. Consumers increasingly depend on more tools to find information and interact with brands across search, websites, apps, voice assistants and AI chat. Consumers are no longer solely depending on individual keyword searches like "mortgage" or "menswear." Instead, they are increasingly using natural language phrases like "wealth advisor near me who specializes in healthcare" or asking specific questions like "what's the best menswear store in London that sells dress shirts and is open now?" Additionally, consumers are leveraging multiple channels, such as online reviews and social media, to find information that influences decisions both in-person and online. Publishers are increasingly answering these questions directly across digital touchpoints using complex algorithms that evaluate a brand's presence across many sources. In order to win customer impressions and conversions, businesses must maintain an accurate and consistent digital presence with proactive knowledge management to engage with customers across as many channels as possible.

With the evolution of consumer behavior and expectations, successful businesses have changed how they market their brands to be discovered and considered. The rapidly evolving AI landscape is changing search engine optimization, and it is becoming more challenging for businesses to keep up and manage all of their information and channels at scale, across various locations and regions. Poor user experience on a business's own website may result in lost sales opportunities or may cause consumers to visit a competitor's website. The challenge for businesses is to understand and provide accurate answers to consumer's questions while delivering a rich, consistent experience across all digital touchpoints without relying on "best guess" data that can be incomplete, misleading or incorrect.

Yext first pioneered a better way for businesses to control and publish the critical information about themselves to answer consumer questions and now leads the industry in digital presence management. We do so by enabling brands to collect, organize, and deliver their critical knowledge to consumers and manage their digital presence at scale to connect, engage, and convert customers. With one central platform, businesses can efficiently manage their digital presence at scale while maintaining a consistent and compelling brand story that resonates with their customers. Businesses can select as many products as needed to meet their goals. By leveraging Scout, Listings, Reviews, Social, Pages and one-on-one engagement, Yext drives a complete online digital presence for multi-location brands.

Businesses of nearly all sizes and in a diverse set of industries can benefit from our platform and capabilities. Yext enables businesses to:

• manage a consistent brand experience across all digital channels;

• increase local engagement by ensuring all publishers have accurate information about their business;

• access one platform for all digital marketing channels, with the ability to integrate with their existing marketing solutions and consolidate marketing data;

• make data-driven marketing decisions with access to real-time data and trend analysis across digital channels;

• leverage AI to deliver accurate information in a timely fashion and engage with consumers more efficiently and effectively while automating and optimizing workflows; and

• modify, enhance and control the information about each of their locations, professionals, menus, events or other entities in one place.

Industry Background

Managing Information Online Is Challenging. Many businesses struggle to effectively control, structure and manage information across the digital ecosystem where consumers discover their businesses. This is due to several factors:

• Lack of Control of Information Online. Many answers and results provided by searches currently come from third-party sources such as data aggregators, governmental agencies and consumers. The net result of this third-party sourcing has been to produce "best guess" data that can often miss or misstate the true facts about businesses worldwide.

• Attributes that Describe the Information About a Business Are Expanding. To respond to consumer questions, businesses need to be able to define the information about their business using detailed, category-specific attributes ranging from name, address and phone number to more detailed items such as whether a hotel accepts pets, a restaurant has a gluten-free menu, or a doctor accepts certain insurance plans.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-10_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-10_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-10_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-09-01_2-02-results.md, 10-K_2026-03-10_item7_mdna.md, 10-K_2026-03-10_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
