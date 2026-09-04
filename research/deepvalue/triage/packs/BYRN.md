# Triage pack — BYRN · Byrna Technologies Inc.

_Generated 2026-09-04 16:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** BYRN · **Name:** Byrna Technologies Inc.
- **CIK:** 0001354866
- **SIC:** 3690 — Miscellaneous Electrical Machinery, Equipment & Supplies
- **Fiscal year end (MM-DD):** 11-30
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/BYRN

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Byrna Technologies Inc.
- **CIK:** 1,354,866 · **SIC:** 3690 (Miscellaneous Electrical Machinery, Equipment & Supplies) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 3.41 |
| mktcap | $77.4M |
| ev | $67.9M |
| ev_ebit | 5.7x |
| fcf | -$9.2M |
| fcf_yield | -11.9% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 19.7% |
| net_debt | -$9.4M |
| net_debt_ebit | -0.8x |
| cash | $9.4M |
| ltd | $0.00 |
| equity | $57.0M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $118.1M |
| revenue_prior | $85.8M |
| rev_growth | 37.7% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $11.8M |
| net_income | $9.7M |
| cfo | -$1.6M |
| capex | $7.6M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -0.0% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 22,693,356 |
| shares_py | 22,703,814 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -77.0% |
| r6m | -72.7% |
| off_52w_high | -87.7% |
| adv20 | $1.5M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.07 |
| r_ev_ebit | 0.92 |
| r_roic | 0.87 |
| r_rev_growth | 0.92 |
| r_buyback | 0.68 |
| score | 0.59 |

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
| rank | 154 |

**Screen rationale:** cheap at 5.7x EV/EBIT; high ROIC 19.7%; revenue +37.7%; debt data missing (net cash unverified); WARNING 6m return below -40%


## 3. Share count trend

- Shares outstanding: **22,693,356** (CY2026Q2I) vs **22,703,814** prior year (CY2025Q2I)
- Change: **-0.0%** — roughly flat
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-09-03** — Item 5.02 (officer / director change or comp arrangement): On August 29, 2026, the Board of Directors (the "Board") of Byrna Technologies Inc. (the "Company") increased the size of the Board from seven to eight members and appointed Matthew McBrady, Ph.D. to fill the resulting vacancy, effective immediately.
- **2026-08-14** — Item 5.02 (officer / director change or comp arrangement): On August 10, 2026, Emily Rooney tendered her resignation as a member of the Board of Directors (the "Board") of Byrna Technologies Inc. (the "Company"), effective as of such date.
- **2026-07-08** — Item 1.01 (Entry into a Material Definitive Agreement): On July 7, 2026, Byrna Technologies Inc. (the "Company") entered into an Asset Purchase Agreement (the "Purchase Agreement") with HERO Defense Systems, LLC, a Nevada limited liability company ("Hero"), and, solely for the limited purposes specified therein...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 72,831 sh / $267,739 vs sells 0 sh / $0 -> net $267,739 (BUYING).
Distinct insiders buying (code P): 4. Largest buy: Kennedy TJ bought 29,000 sh @ $3.53 ($102,286) on 2026-07-22.

Form 4 filings parsed: 12; transaction rows: 21 (open-market buys 8, sales 0).

| code | rows |
|---|---|
| A | 1 |
| M | 12 |
| P | 8 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-09_2-02-results.md)

_Extraction: started at the first release heading, 'Byrna Technologies Reports Fiscal Second Quarter 2026 Results'; skipped 9 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EXHIBIT 99.1 (ex_985847.htm)

Byrna Technologies Reports Fiscal Second Quarter 2026 Results

ANDOVER, Mass., July 9, 2026 - Byrna Technologies Inc. ( " Byrna " or the " Company " ) (Nasdaq: BYRN) , a personal defense technology company specializing in the development, manufacture, and sale of innovative less-lethal personal security solutions, today reported select financial results for its fiscal second quarter ("Q2 2026") ended May 31, 2026.

Fiscal Second Quarter 2026 and Recent Operational Highlights

● | Entered into a binding agreement to purchase HERO Defense Systems, LLC, a complementary less-lethal self-defense company, expanding Byrna's product portfolio across additional price points and everyday-carry form factors.

● | Initiated and recently expanded its "try before you buy" pilot program, following early results achieving an approximately 30% conversion rate among participating customers who received a demo unit, with most conversions occurring in the second week of the two-week trial period.

● | Generated over 150,000 responses on the "Find the Right Launcher" guided shopping experience on Byrna.com since it was introduced in April. Customers who used the product education tool converted at approximately twice the conversion rate of the overall website.

● | Reduced launcher assembly operations from four lines at the end of fiscal Q1 to two lines by May and ceased in-house ammunition manufacturing to better align production with current demand, improve cost efficiency, and support the reduction of finished goods inventory over time.

● | Activated its Fox Sports media partnership through iHeartMedia in June, expanding Byrna's reach to a broad, highly engaged sports audience across radio and digital platforms.

● | Realigned sales and marketing functions and initiated a search for dedicated leaders to support retail growth and brand expansion.

● | Appointed HLK as agency of record to strengthen brand messaging, customer acquisition, and product education initiatives.

● | Appointed Acceleration Partners as its influencer and affiliate marketing agency to build a broader social creator program, relaunch Byrna's affiliate marketing program and improve the Company's ability to measure customer acquisition across its e-commerce channels.

● | Promoted industry veteran Matthew Campagni to Chief Strategy Officer to lead the Company's strategic planning initiatives and support cross-functional execution.

Fiscal Second Quarter 2026 Financial Results

Results compare Q2 2026 to the 2025 fiscal second quarter ended May 31, 2025, unless otherwise indicated.

Net revenue for Q2 2026 was $16.4 million, compared to $28.5 million in the fiscal second quarter of 2025 ("Q2 2025"). The approximately 43% year-over-year decrease was driven primarily by a decrease in e-commerce sales and slower reorder activity from dealers and chain stores following substantial restocking in fiscal Q1 and slower-than-expected sell-through.

Gross profit for Q2 2026 was $1.8 million (11% of net revenue), down from $17.6 million (62% of net revenue) in Q2 2025. Reported gross margin included a one-time $5.9 million inventory write-down and a $3.5 million impairment of equipment, this was partially offset by a $1.1 million tariff refund recorded in cost of goods sold. Excluding these items, adjusted gross profit was $10.1 million, representing adjusted gross margin of approximately 62%.

Operating expenses for Q2 2026 were $14.6 million, compared to $14.2 million for Q2 2025, an increase of 2.7%. The increase primarily reflected an impairment charge of $1 million as well as continued investment in marketing, partially offset by the change in variable selling expenses associated with a decrease in sales.

Net income (loss) for Q2 2026 was $(10.1) million, compared to $2.4 million for Q2 2025. Net loss included non-cash impairment and inventory write-down charges of $10.4 million related to the shutdown of our ammunition manufacturing facility in Fort Wayne and strategic product rationalization. A tax benefit of $2.7 million was also recorded for the quarter.

Adjusted EBITDA 1 , a non-GAAP metric reconciled below, for Q2 2026 totaled $(0.6) million, compared to $4.3 million in Q2 2025.

Cash, cash equivalents and marketable securities as of May 31, 2026 totaled $10.4 million, compared to $15.5 million at November 30, 2025. Inventory on May 31, 2026 totaled $30.4 million, compared with $32.7 million on November 30, 2025. The Company is focused on lowering inventory over time and improving working capital efficiency.

Management Commentary

"Our second quarter results did not reflect the level of performance we believe Byrna can deliver," said Byrna CEO Conn Davis. "We expected the quarter to begin a transition period, but continued softness in our direct-to-consumer channel as well as a slower pace of reorders across retail partners led to a steeper reset than we initially expected.

"In e-commerce, web traffic remained weak, and while conversion rates showed modest improvement as a result of our website changes, overall conversion levels and average order value were below where we expected. In retail, our partners entered the quarter with elevated inventory levels following meaningful post-holiday restocking in Q1. Sell-through during the quarter did not occur at a pace that supported consistent reorder activity, which impacted revenue across both dealer and big box channels.

"From an operational standpoint, we took actions during the quarter to better align production and operating costs with current demand. We reduced production capacity in our launcher facility and exited in-house ammo manufacturing where we were not cost competitive. These actions reduce costs, operating complexity, and establish a more balanced operating baseline that should allow us to work down physical inventory through the second half of the year.

"We also advanced a number of initiatives designed to improve demand over both the near and longer term. Our top operational priority is improving customer conversion and retail productivity across all channels.

"We are seeing encouraging early results from our "try before you buy" program, which is attracting new customers to the brand and generating conversion rates of approximately 30%. This represents a meaningful improvement versus traditional e-commerce and provides a scalable pathway to reaccelerate direct-to-consumer growth over time.

"On the retail side, we are focused on continuing our store expansion while also working closely with our partners to improve customer discovery and sell-through. Initiatives such as in-store training, enhanced merchandising, including end-cap displays, and expanded demo experiences are producing stronger results in the locations where they have been implemented. Our focus now is applying those learnings more consistently across the wider footprint.

See non-GAAP financial measures at the end of this press release for a reconciliation and a discussion of non-GAAP financial measures.

"In parallel, our messaging pivot is underway, as we work to broaden our reach and engage a wider set of customer segments. This includes partnerships such as Fox Sports, along with new social and influencer programs designed to introduce Byrna to previously underpenetrated audiences while continuing to build on the existing foundation with our core customers. We believe this approach will expand our addressable market while supporting more consistent and durable demand over time. We are also in the process of bringing on experienced leaders across marketing and retail to strengthen execution, improve accountability and support the next phase of growth.

"Based on current expectations, fiscal 2026 will not be a revenue-growth year. Q2 reset the revenue baseline, and we are planning the business around current demand trends rather than assuming a quick return to prior growth rates. We expect improvement from the first half of the fiscal year to the second half, as retailers prepare for the holidays and more of our marketing, conversion and customer-acquisition initiatives enter the market.

"We are building from a more realistic baseline, with the opportunity to improve as these initiatives begin to contribute. Our focus is on improving website traffic and conversion, strengthening retail sell-through and reorder cadence, reducing inventory and improving working capital efficiency. We believe the actions underway position Byrna to finish fiscal 2026 on stronger footing and enter fiscal 2027 with a business capable of delivering more consistent growth."

Conference Call

The Company's management will host a conference call today, July 9, 2026, at 9:00 a.m. Eastern time (6:00 a.m. Pacific time) to discuss these results, followed by a question-and-answer period.

Toll-Free Dial-In: 877-709-8150

International Dial-In: +1 201-689-8354

Confirmation: 13761119

Please call the conference telephone number 5-10 minutes prior to the start time of the conference call. An operator will register your name and organization. If you have any difficulty connecting with the conference call, please contact Gateway Group at 949-574-3860.

The conference call will be broadcast live and available for replay here and via the Investor Relations section of Byrna's website .

About Byrna Technologies Inc.

Byrna is a personal defense technology company specializing in the development, manufacture, and sale of innovative less-lethal personal security solutions. For more information on the Company, please visit the corporate website here or the Company's investor relations site here . The Company is the manufacturer of the Byrna® CL, Byrna® LE and Byrna® SD personal security devices, state-of-the-art handheld CO2 powered launchers designed to provide a less-lethal alternative to a firearm for the consumer, private security, and law enforcement markets. To purchase Byrna products, visit the Company's e-commerce store.

BYRNA TECHNOLOGIES INC.

Condensed Consolidated Statements of Operations and Comprehensive Income (Loss)

(Amounts in thousands except share and per share data)

(Unaudited)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-05_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

OVERVIEW

Byrna Technologies Inc. designs, manufactures, retails, and distributes less‑lethal personal security solutions intended for situations that do not require the use of lethal force. Our mission is to empower individuals to protect themselves and others, and our product strategy emphasizes ease of use, effectiveness, and reliability in both consumer and professional safety environments. We also develop tools intended to serve as alternatives to traditional firearms for law enforcement and private security customers, with the goal of reducing firearm‑related incidents and supporting de‑escalation practices. Our strategy includes positioning Byrna® as a consumer lifestyle brand associated with personal confidence and safety, while expanding our product portfolio to broaden market reach and drive sales growth from both new and existing customers.

Our business strategy is twofold: (1) to fulfill the growing demand for less-lethal products in the law enforcement, correctional services, and private security markets and (2) to provide civilians – including those whose work or daily activities may put them at risk of being a victim – with easy access to an effective, less-lethal way to protect themselves and their loved ones from threats to their person or property.

We believe demand for less‑lethal products in the United States and globally continues to rise and that this category will remain a growing segment of the broader security market. We plan to meet this demand by manufacturing and distributing our Byrna SD, Byrna LE, and most recently our Byrna CL launchers, along with continued expansion of our accessory and ammunition offerings.

On January 10, 2023, we acquired a 51% ownership interest in Byrna LATAM S.A. ("Byrna LATAM"), a corporate joint venture formed to expand our operations and presence in South American markets, for $0.5 million. We accounted for this investment using the equity method because we did not have voting control or substantive participating rights that would give us control over Byrna LATAM. On August 19, 2024, we sold our 51% ownership interest to Fusady S.A. for $1 pursuant to the LATAM Share Purchase Agreement and entered into an exclusive distribution, manufacturing, and licensing agreement with Byrna LATAM (the "LATAM Licensing Agreement"). Under this agreement, Byrna LATAM is authorized to exclusively manufacture the Byrna SD launcher and ammunition in certain South American countries and is required to pay us royalties on Byrna products manufactured. The LATAM Share Purchase Agreement also includes put and call rights based on defined triggers that expire on August 19, 2029.

Beginning in fiscal 2024 and continuing through fiscal 2025, we expanded our go‑to‑market strategy beyond our historical e‑commerce focus by adopting a broader omnichannel distribution model. These initiatives included the commercial launch of the Byrna CL, expansion of the Byrna LE and LE PRO platforms, the opening of Byrna‑branded retail locations, and onboarding national retail partners such as Sportsman's Warehouse. In addition, we implemented an AI‑driven advertising engine and expanded our influencer‑based marketing program, both of which contributed to improved customer‑acquisition efficiency and increased brand reach. Beginning in fiscal 2025, we also reorganized our operations into two reportable sales channels, Direct‑to‑Consumer ("DTC") and Wholesale (dealer/distributor), to align with our expanded omnichannel strategy, the opening of Company‑operated retail stores, and increased penetration into national retail chains and international distributors.

RESULTS OF OPERATIONS

Revenue of $118.1 million for the fiscal year ended November 30, 2025 increased $32.3 million, or 37.7%, compared to $85.8 million in the prior fiscal year. The increase was primarily driven by higher wholesale dealer and distributor sales, which increased by $21.6 million, as well as continued growth in direct‑to‑consumer e‑commerce sales. E‑commerce transactions through Amazon and our website remained the largest revenue contributor, accounting for 64.8% of total net revenue for fiscal year 2025 compared to 76.8% in fiscal year 2024. We also achieved growth in our dealer channel and experienced increased sales in Canada.

Gross margin declined by 1.0% compared to the prior year. Operating expenses increased due to higher marketing expenditures, personnel‑related costs, and professional fees. Although revenue growth resulted in higher gross profit, the increase in operating expenses partially offset these gains, resulting in profit from operations of $11.8 million for fiscal year 2025, compared to an operating profit of $6.7 million for fiscal year 2024. Gross margin declined primarily due to a higher proportion of Wholesale and Retail revenue, which are lower‑margin channels, partially offset by improved cost absorption in manufacturing and lower per‑unit freight costs.

Year ended November 30, 2025, as compared to year ended November 30, 2024:

Net Revenue

We present revenue net of returns, allowances, and discounts. Net revenue for the year ended November 30, 2025 was $118.1 million, an increase of $32.3 million, or 37.7%, compared to $85.8 million in the prior year. Direct‑to‑consumer revenue, including sales through Amazon and our website, increased by $10.7 million, or 16.3%, from $65.9 million in fiscal year 2024 to $76.6 million in fiscal year 2025. Domestic dealer and retail sales increased by $14.0 million, or 108.4%, from $12.9 million in fiscal year 2024 to $26.9 million in fiscal year 2025. International revenue, including Canada, increased from $6.8 million to $12.1 million year‑over‑year. We recognized $1.6 million in royalty revenue related to the LATAM Licensing Agreement during fiscal year 2025.

Segment Results

Direct‑to‑Consumer (DTC)

DTC revenue increased to $76.6 million in fiscal year 2025, driven by increased web sessions and expanded consumer reach, expanded digital‑marketing initiatives, enhanced influencer partnerships, and the launch of new Byrna‑operated retail locations. These efforts increased overall brand visibility and market reach.

Wholesale (Dealer/Distributor)

Wholesale revenue increased to $41.5 million in fiscal year 2025, reflecting (i) expanded relationships with national and regional retailers, (ii) enhanced engagement with distributors, (iii) increased law‑enforcement interest, and (iv) the first year of royalty revenue under the LATAM Licensing Agreement.

Cost of Goods Sold

Cost of goods sold was $46.7 million for fiscal year 2025, compared to $33.0 million in fiscal year 2024. The $13.7 million increase was driven primarily by higher sales volume. Cost of goods sold attributable to Direct‑to‑Consumer ("DTC") was $26.5 million in fiscal year 2025, compared to $22.9 million in fiscal year 2024. Cost of goods sold attributable to Wholesale was $20.2 million in fiscal year 2025, compared to $10.1 million in fiscal year 2024.

Gross Profit

Gross profit is calculated as total revenue less cost of goods sold, and gross margin is calculated as gross profit divided by total revenue. Included as cost of goods sold are costs associated with the production and procurement of products, such as inbound freight costs, manufacturing depreciation, purchasing and receiving costs, and inspection costs. Gross profit was $71.5 million, or 60.5% of net revenue, for fiscal year 2025, compared to $52.8 million, or 61.5%, in the prior year. The decline in gross margin resulted from an increased proportion of wholesale revenue relative to DTC revenue as well as manufacturing inefficiencies. The broader shift toward Wholesale and Retail channels reduced the proportion of higher‑margin DTC revenue, contributing to the decline in consolidated gross margin for the year. Because wholesale transactions generally carry lower average selling prices relative to DTC sales, the higher wholesale mix contributed to the decline in consolidated gross margin during the period.

Operating Expenses

Operating expenses were $59.6 million for the fiscal year ended November 30, 2025, compared to $46.1 million in the prior fiscal year. The $13.5 million increase was primarily driven by higher marketing expenditures, personnel‑related costs, and variable selling expenses. Marketing expenditures increased by $5.5 million, from $12.4 million in fiscal year 2024 to $17.9 million in fiscal year 2025. Total employee compensation costs decreased by $0.7 million, from $17.8 million in fiscal year 2024 to $17.1 million in fiscal year 2025. Variable selling expenses increased by $3.6 million, from $7.8 million in fiscal year 2024 to $11.4 million in fiscal year 2025. Professional fees increased by $0.1 million, from $2.0 million in fiscal year 2024 to $2.1 million in fiscal year 2025. Other operating costs, including administrative expenses, increased by $2.0 million, from $6.1 million in fiscal year 2024 to $8.1 million in fiscal year 2025. The increase was primarily driven by higher insurance costs—including D&O, umbrella, general liability, and cyber coverage—along with increases in facility expenses, repairs and maintenance, depreciation and amortization, and production‑related operating expenses. These increases were partially offset by lower research and development expenses. In addition, the overall increase in operating expenses reflects higher spending on influencer‑marketing programs, expanded creative‑content production to support AI‑assisted advertising initiatives, and initial occupancy and labor costs associated with new Company‑operated retail stores.

Profit from Operations

The increase in revenue, off-set by the increase in operating expenses resulted in an increase of $5.1 million in profit from operations of $11.8 million in fiscal year 2025, compared to a profit from operations of $6.7 million in fiscal year 2024.

Interest Income/Expense

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-05_item1_business.md)

ITEM 1. BUSINESS

Overview

We are a less‑lethal self‑defense technology company specializing in innovative, next‑generation solutions for security situations that do not require the use of lethal force. Our mantra is Live Safe®, and our core mission is to empower people to safely embrace life. We seek to fulfill our mission by developing easy‑to‑use self‑defense tools that are designed to allow people to live more safely. We are also focused on providing law enforcement and private security customers with less‑lethal alternatives to firearms that are intended to reduce the use of lethal force and facilitate trust within the communities they serve.

Since 2023, the Company has modernized its product line, diversified its distribution channels, and implemented technology‑driven marketing tools that significantly expand reach and brand engagement. In 2024 and 2025, Byrna launched the Byrna CL™ (Compact Launcher), expanded its law‑enforcement‑grade Byrna LE™ and LE PRO™ product lines, deployed a proprietary AI‑assisted advertising platform, expanded retail distribution through Sportsman's Warehouse and other partners, and opened additional Byrna‑branded retail locations. The Company also established Byrna Technologies Canada, a wholly owned subsidiary supporting regulatory compliance, warehousing, marketing, and sales for the Canadian market.

Our product portfolio includes:

● | handheld personal security devices and shoulder-fired launchers designed for use by consumers and professional security customers without the need for a background check or firearms license in most U.S. jurisdictions;

● | a line of projectiles that are fired by Byrna devices, including chemical irritant, kinetic and inert rounds;

● | a line of self-defense aerosol products, including Byrna Bad Guy Repellent™; and

● | accessories and related safety products, including the Byrna Banshee™, Byrna Shield™, compressed carbon dioxide (CO2) canisters, sighting systems, holsters and Byrna-branded apparel.

Our Byrna personal security devices are powerful and effective less-lethal self-defense devices that are powered by CO2 and fire .68 caliber spherical kinetic and chemical irritant projectiles that are designed to disable a threat from a standoff distance of up to approximately 60 feet, depending on the launcher and the projectile used. We have designed our Byrna devices to function as a platform that can be enhanced, upgraded and customized in a modular fashion with our accessory products. Only Byrna projectiles are approved for use with Byrna launchers, which creates the potential for recurring sales of consumable products.

Our products are sold in both the consumer and security professional markets. In the consumer market, our solutions are designed to provide ordinary civilians with an effective, less-lethal tool to disable, disarm and deter would-be assailants and to escape harm's way. In the professional market, our products are designed to provide domestic and international law enforcement agencies, corrections and custodial officers, private security professionals, private investigators and other professional security users with a practical, less-lethal option to address threats and resolve conflicts without the need to resort to lethal force. Our products can be purchased in most U.S. locations quickly, simply and discreetly, generally without the requirement for a license, background check or waiting period, subject to applicable state and local laws.

Strategic Focus and Products

Our strategy is to establish Byrna as a consumer lifestyle brand associated with the confidence people can achieve by knowing they can protect themselves, their loved ones and those around them. We believe we have a significant opportunity to leverage the Byrna brand to expand our product line, broaden our user base and generate increasing sales from new and existing customers.

Our product offerings include handheld CO₂‑powered launchers, chemical irritant projectiles, kinetic projectiles, and a variety of accessories. Our flagship product, the Byrna SD, is a compact, ergonomically designed handheld personal security device with the size and form factor of a compact handgun. It is easy to use, has virtually no recoil, and is designed to fire accurately from a standoff distance of up to approximately 60 feet, depending on the projectile used. The Byrna SD utilizes our patented technology and more than 60 custom‑designed parts, and features reloadable magazines that hold five or seven .68‑caliber projectiles. In 2025, we introduced the Byrna CL™ (Compact Launcher), a compact, lightweight launcher designed specifically for the everyday carry ("EDC") consumer segment. The CL platform incorporates improved ergonomics, simplified operation, enhanced concealability, and utilizes newly developed .61‑caliber projectiles. We also expanded our law‑enforcement‑grade offerings with the Byrna LE™ and Byrna LE PRO™, which feature improved accuracy, higher muzzle velocity, and enhanced duty‑grade performance for both law enforcement and advanced civilian consumers. Our projectile portfolio was updated in 2024–2025 to include Eco‑Kinetic rounds, updated Max and Pepper chemical irritant formulations, and state‑compliant chemical‑free variants aligned with evolving legal requirements. Accessories now include premium holsters, optics‑integrated attachments, magazines, CO₂ cartridges, and EDC‑focused gear bundles tailored to both new and experienced users. The Byrna family of launchers is designed to provide less‑lethal alternatives to firearms, effective at significantly greater standoff distances than pepper spray or conductive energy devices, which have recommended maximum ranges of 10 feet and 20 feet, respectively.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-05_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-05_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-05_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-07-09_2-02-results.md, 10-K_2026-02-05_item7_mdna.md, 10-K_2026-02-05_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
