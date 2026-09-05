# Triage pack — AOUT · American Outdoor Brands, Inc.

_Generated 2026-09-05 08:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** AOUT · **Name:** American Outdoor Brands, Inc.
- **CIK:** 0001808997
- **SIC:** 3949 — Sporting & Athletic Goods, NEC
- **Fiscal year end (MM-DD):** 04-30
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/AOUT

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** American Outdoor Brands, Inc.
- **CIK:** 1,808,997 · **SIC:** 3949 (Sporting & Athletic Goods, NEC) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 14.48 |
| mktcap | $181.1M |
| ev | $147.8M |
| ev_ebit | n/a |
| fcf | $4.3M |
| fcf_yield | 2.4% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -5.4% |
| net_debt | -$33.3M |
| net_debt_ebit | n/a |
| cash | $33.3M |
| ltd | $0.00 |
| equity | $164.4M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $190.5M |
| revenue_prior | $222.3M |
| rev_growth | -14.3% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$9.0M |
| net_income | -$9.2M |
| cfo | $6.3M |
| capex | $2.0M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -2.0% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 12,507,120 |
| shares_py | 12,757,954 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 20.6% |
| r6m | 63.6% |
| off_52w_high | -0.1% |
| adv20 | $3.8M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.33 |
| r_ev_ebit | 0.00 |
| r_roic | 0.18 |
| r_rev_growth | 0.07 |
| r_buyback | 0.78 |
| score | 0.32 |

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
| rank | 388 |

**Screen rationale:** buying back stock -2.0%; debt data missing (net cash unverified); 12-1 momentum 20.6%


## 3. Share count trend

- Shares outstanding: **12,507,120** (CY2026Q2I) vs **12,757,954** prior year (CY2025Q2I)
- Change: **-2.0%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-06** — Item 5.02 (officer / director change or comp arrangement): On August 4, 2026, Kevin D. Leary was appointed to our Board of Directors to serve for a term expiring at our 2026 annual meeting of stockholders and until his successor is duly elected and qualified.
- **2026-03-12** — Item 1.01 (Entry into a Material Definitive Agreement): On March 10, 2026, we and certain of our direct and indirect Subsidiaries amended our secured loan and security agreement pursuant to Amendment No. 3 to Loan and Security Agreement, or the Amended Loan and Security Agreement, with certain lenders and TD Bank...

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m across 16 transaction row(s) — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 16 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 9 |
| F | 7 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-09-03_2-02-results.md)

_Extraction: started at the first release heading, 'First Quarter Fiscal 2027 Financial Results'; skipped 10 forward-looking-statement block(s); 9 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (aout-20260903xexx991.htm)

First Quarter Fiscal 2027 Financial Results

COLUMBIA, Mo., September 3, 2026 – American Outdoor Brands, Inc. (NASDAQ Global Select: AOUT) , an innovation company that provides product solutions for outdoor enthusiasts, today announced financial results for the first quarter fiscal 2027 ended July 31, 2026.

First Quarter Fiscal 2027 Financial Highlights

• Quarterly net sales were $37.3 million, an increase of $7.6 million, or 25.4%, compared with quarterly net sales of $29.7 million for the comparable quarter last year. Adjusted for approximately $6.0 million of orders that were accelerated by retailers from the first quarter of fiscal 2026 into the fourth quarter of fiscal 2025, net sales in the first quarter of fiscal 2027 increased by 4.3%.

• Quarterly gross margin was 53.0%, compared with quarterly gross margin of 46.7% for the comparable quarter last year.

• Quarterly GAAP net loss was $1.5 million, or $(0.12) per diluted share, compared with a GAAP net loss of $6.8 million, or $(0.54) per diluted share for the comparable quarter last year.

• Quarterly non-GAAP net income was $415,000, or $0.03 per diluted share, compared with non-GAAP net loss of $3.3 million, or $(0.26) per diluted share, for the comparable quarter last year. GAAP to non-GAAP adjustments for net income (loss) exclude acquired intangible amortization, stock compensation, and other costs. For a detailed reconciliation, see the schedules that follow in this release.

• Quarterly non-GAAP Adjusted EBITDA was $1.2 million, or 3.1% of net sales, compared with $(3.1) million, or (10.5)% of net sales for the comparable quarter last year. For a detailed reconciliation, see the schedules that follow in this release.

Brian Murphy, President and Chief Executive Officer, said, "We are very pleased with our strong start to fiscal 2027. First quarter net sales increased approximately 25%. As a reminder, the prior-year quarter was impacted by approximately $6 million of orders that retailers accelerated into fiscal 2025. Even after adjusting for that acceleration, first quarter net sales increased approximately 4% – a great result that exceeded our expectations and reflects the continued strength of our brands.

"Importantly, that performance was broad-based, reflecting growth in both our Outdoor Lifestyle and Shooting Sports categories, and supported by increased sales with our largest retail partners. Point-of-sale (POS) results also remained positive in both categories during the quarter, which we believe demonstrates healthy consumer demand across multiple brands in our portfolio. POS increased 6% in Outdoor Lifestyle and 3% in Shooting Sports.

"Innovation remained a key driver of our first quarter performance, with new products representing more than 36% of our net sales. Our Caldwell ClayCopter® platform continued to outperform during the quarter, generating strong retailer and consumer adoption, positive POS results, and significant engagement across social media. That success was further validated by the ClayCopter Surface-to-Air TM being named the 2026 Frank Desomma Innovation of the Year by the Industry Choice Awards in August. This recognition means a

1800 N Route Z
Columbia, MO 65202
(800) 338-9585
NASDAQ: AOUT

great deal to our team because the award is an unbiased evaluation of all products in the shooting sports industry – and Caldwell® came out on top.

"We continued to expand our BUBBA® brand with new product introductions, including the launch of our Pro Series Gen 2 Electric Fillet Knife, which was recognized as Best of Show for the category of Cutlery, Hand Pliers, or Tools at ICAST 2026. A major milestone in the quarter was the consumer launch of SCORETRACKER® LIVE, our digital platform developed with Major League Fishing, that brings real-time scoring technology and the excitement of professional-grade competition to anglers, tournament organizers and fans everywhere. The launch expands BUBBA's opportunity within the large angling market while adding another important component to its growing ecosystem of connected hardware, software and subscription-based services.

"More broadly, BUBBA® and Caldwell® demonstrate our strategy to build connected ecosystems around key growth brands that deepen consumer engagement and loyalty, extend the value of our innovation beyond individual products, and create multiple avenues for long-term growth. We believe this approach has the potential to extend to other brands in our portfolio over time."

Andrew Fulmer, Chief Financial Officer, said, "Sales growth in the quarter translated to solid financial performance. Strength in new products helped accelerate margin expansion with gross margins increasing 630 basis points to 53.0% and Adjusted EBITDA improving more than $4.0 million. We also generated meaningful cash flow and ended the quarter with $33.3 million in cash and no debt, further strengthening our financial position."

Fiscal 2027 Outlook

"Our first quarter performance reinforces our confidence in our expectations for the year. We are maintaining our full-year guidance for net sales of $200 million to $210 million, and we are increasing our Adjusted EBITDA guidance to $14.5 million to $17.5 million. As we enter our seasonally stronger second and third quarters, we remain focused on delivering profitable growth while maintaining the financial flexibility to invest in our business and pursue opportunities that create long-term shareholder value."

The Company does not provide a quantitative reconciliation of non-GAAP Adjusted EBITDA guidance in reliance on the "unreasonable efforts" exception for forward-looking non-GAAP measures set forth in SEC rules because certain financial information, the probable significance of which cannot be determined, is not available and cannot be reasonably estimated without unreasonable effort and expense.

Conference Call and Webcast

In this press release, certain non-GAAP financial measures, including "non-GAAP net income (loss)," "Adjusted EBITDA," and net sales adjusted for $6.0 million of orders that were accelerated by retailers from fiscal 2026 into the final weeks of fiscal 2025 are presented. A reconciliation of "non-GAAP net income (loss)," "Adjusted EBITDA," and other non-GAAP financial measures is contained at the end of this press release. From time to time, the Company considers and uses these non-GAAP financial measures as supplemental measures of

1800 N Route Z
Columbia, MO 65202
(800) 338-9585
NASDAQ: AOUT

operating performance in order to provide the reader with an improved understanding of underlying performance trends. The Company believes it is useful for itself and the reader to review, as applicable, both (1) GAAP measures that include (i) amortization of acquired intangible assets, (ii) stock compensation, (iii) contract exit costs, (iv) income tax adjustments, (v) interest income, (vi) income tax expense, and (vii) depreciation and amortization; and (2) the non-GAAP measures that exclude such information. The Company presents these non-GAAP measures because it considers them an important supplemental measure of its performance and believes the disclosure of such measures provides useful information to investors regarding the Company's financial condition and results of operations. The Company's definition of these adjusted financial measures may differ from similarly named measures used by others. The Company believes these measures facilitate operating performance comparisons from period to period by eliminating potential differences caused by the existence and timing of certain expense items that would not otherwise be apparent on a GAAP basis. These non-GAAP measures have limitations as an analytical tool and should not be considered in isolation or as a substitute for the Company's GAAP measures. The principal limitations of these measures are that they do not reflect the Company's actual expenses and may thus have the effect of inflating its financial measures on a GAAP basis.

About American Outdoor Brands, Inc.

American Outdoor Brands, Inc. (NASDAQ Global Select: AOUT) is an innovation company that provides product solutions for outdoor enthusiasts, including hunting, fishing, camping, shooting, meat processing, outdoor cooking, and personal security and personal defense products. The Company produces innovative, high-quality products under brands including BOG®; BUBBA®; Caldwell®; Crimson Trace®; Frankford Arsenal®; Grilla®; Hooyman®; Imperial®; LaserLyte®; Lockdown®; MEAT! Your Maker®; Old Timer®; Schrade®; Tipton®; Uncle Henry®; and Wheeler®. For more information about all the brands and products from American Outdoor Brands, Inc., visit www.aob.com .

As of:
July 31, 2026 (Unaudited) | April 30, 2026
ASSETS
Current assets:
Cash and cash equivalents | 33,275 | 21,436
Accounts receivable, net of allowance for credit losses of $396 on July 31, 2026 and $419 on April 30, 2026 | 25,498 | 29,233
Inventories | 100,313 | 91,889
Assets held for sale | 633 | 734
Prepaid expenses | 2,671 | 2,268
Other current assets | 4,389 | 16,978
Income tax receivable | 73 | 156
Total current assets | 166,852 | 162,694
Property, plant, and equipment, net | 8,815 | 9,327
Intangible assets, net | 22,340 | 23,527
Right-of-use assets | 30,270 | 30,710
Other assets | 341 | 362
Total assets | 228,618 | 226,620
LIABILITIES AND EQUITY
Current liabilities:
Accounts payable | 15,288 | 13,432
Accrued expenses | 15,444 | 13,212
Accrued payroll and incentives | 1,485 | 1,700
Lease liabilities, current | 1,602 | 1,569
Total current liabilities | 33,819 | 29,913
Lease liabilities, net of current portion | 30,403 | 30,814
Total liabilities | 64,222 | 60,727
Commitments and contingencies
Equity:
Preferred stock, $0.001 par value, 20,000,000 shares authorized, no shares issued or outstanding on July 31, 2026 and April 30, 2026 | — | —
Common stock, $0.001 par value, 100,000,000 shares authorized, 15,444,198 shares issued and 12,615,054 shares outstanding on July 31, 2026 and 15,288,148 shares issued and 12,459,004 shares outstanding on April 30, 2026 | 15 | 15
Additional paid in capital | 283,358 | 283,327
Retained deficit | (85,436) | (83,908)
Treasury stock, at cost (2,829,144 shares on July 31, 2026 and April 30, 2026) | (33,541) | (33,541)
Total equity | 164,396 | 165,893
Total liabilities and equity | 228,618 | 226,620

1800 N Route Z
Columbia, MO 65202
(800) 338-9585
NASDAQ: AOUT

AMERICAN OUTDOOR BRANDS, INC. AND SUBSIDIARIES

CONSOLIDATED STATEMENTS OF OPERATIONS

(In thousands, except per share data)

For the Three Months Ended July 31,
2026 | 2025
(Unaudited)
Net sales | 37,254 | 29,702
Cost of sales | 17,519 | 15,844
Gross profit | 19,735 | 13,858
Operating expenses:
Research and development | 1,552 | 1,955
Selling, marketing, and distribution | 12,278 | 10,520
General and administrative | 8,021 | 8,202
Total operating expenses | 21,851 | 20,677
Operating loss | (2,116) | (6,819)
Other income, net:
Other income, net | 13 | 35
Interest income, net | 576 | 7
Total other income, net | 589 | 42
Loss from operations before income taxes | (1,527) | (6,777)
Income tax expense | 1 | 52
Net loss | (1,528) | (6,829)
Net loss per share:
Basic and diluted | (0.12) | (0.54)
Weighted average number of common shares outstanding:
Basic and diluted | 12,550 | 12,719

1800 N Route Z
Columbia, MO 65202
(800) 338-9585
NASDAQ: AOUT

AMERICAN OUTDOOR BRANDS, INC. AND SUBSIDIARIES

CONSOLIDATED STATEMENTS OF CASH FLOWS

(In thousands)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-06-25_item7_mdna.md)

_Extraction: started at 'Results of Operations'._

Results of Operations

Net Sales and Gross Profit

The following table sets forth certain information regarding consolidated net sales for the fiscal years ended April 30, 2026 and 2025 (dollars in thousands):

2026 | 2025 | $ Change | % Change
Net sales | 190,536 | 222,322 | (31,786) | (14.3) | %
Cost of sales | 105,342 | 123,058 | (17,716) | (14.4) | %
Gross profit | 85,194 | 99,264 | (14,070) | (14.2) | %
% of net sales (gross margin) | 44.7 | % | 44.6 | %

The following table sets forth certain information regarding trade channel net sales for the fiscal years ended April 30, 2026 and 2025 (dollars in thousands):

2026 | 2025 | $ Change | % Change
e-commerce channels | 71,216 | 84,391 | (13,175) | (15.6) | %
Traditional channels | 119,320 | 137,931 | (18,612) | (13.5) | %
Total net sales | 190,536 | 222,322 | (31,786) | (14.3) | %

Our e-commerce channels include net sales from customers that do not traditionally operate physical brick-and-mortar stores, but generate the majority of their revenue from consumer purchases from their retail websites. Our e-commerce channels also include our direct-to-consumer sales. Our traditional channels include customers that primarily operate out of physical brick-and-mortar stores and generate the large majority of revenue from consumer purchases in their brick-and-mortar locations.

We sell our products worldwide. The following table sets forth certain information regarding geographic makeup of net sales included in the above table for the fiscal years ended April 30, 2026 and 2025 (dollars in thousands):

2026 | 2025 | $ Change | % Change
Domestic | 179,911 | 207,834 | (27,923) | (13.4) | %
International | 10,625 | 14,488 | (3,863) | (26.7) | %
Total net sales | 190,536 | 222,322 | (31,786) | (14.3) | %

The following table sets forth certain information regarding net sales categories for the fiscal years ended April 30, 2026 and 2025 (dollars in thousands):

2026 | 2025 | $ Change | % Change
Shooting sports | 80,054 | 95,200 | (15,146) | (15.9) | %
Outdoor lifestyle | 110,482 | 127,122 | (16,640) | (13.1) | %
Total net sales | 190,536 | 222,322 | (31,786) | (14.3) | %

Fiscal 2026 Net Sales Compared with Fiscal 2025

Total net sales decreased $31.8 million, or 14.3%, from the prior fiscal year because of a decrease in all our channel and category sales primarily from reduced orders from the world's largest online retailer and our belief that a large portion of traditional channel sales were accelerated from our first fiscal quarter of 2026 into the fourth fiscal quarter of 2025, as mentioned below. The decrease in total net sales were partially offset by pricing actions taken on our products to mitigate additional tariff costs associated with tariffs imposed by the U.S. Administration starting in March and April of 2025.

E-commerce channel net sales decreased $13.2 million, or 15.6%, from the prior fiscal year primarily because of lower net sales to the world's largest online retailer in most of our product categories. We believe this decline reflects their inventory management actions, which reduced net sales across most of our products. In addition, we had lower direct-to-consumer net sales for products sold on our websites due to reduced consumer demand.

Net sales in our traditional channels decreased $18.6 million, or 13.5%, from the prior fiscal year. This decrease was driven by the majority of our product categories, partially offset by increased net sales of outdoor cooking equipment. We believe a large portion of the traditional channel decrease was a result of certain customers accelerating orders from our first fiscal quarter of 2026 into the fourth fiscal quarter of 2025. We believe this was due to the anticipated increased costs associated with tariffs imposed by the U.S. Administration in March 2025 and April 2025.

New products represented 29.1% of net sales for fiscal 2026 compared to 21.5% of net sales for fiscal 2025. We have a history of introducing over 200 new products each year.

Our order backlog as of April 30, 2026 was $1.6 million, or $1.0 million lower than at the end of fiscal 2025. Although we generally fulfill the majority of our order backlog, we allow orders received that have not yet shipped to be cancelled, and therefore, our backlog may not be indicative of future sales.

Fiscal 2026 Cost of Sales and Gross Profit Compared with Fiscal 2025

Gross margin for fiscal 2026 increased 10 basis points over the prior fiscal year, primarily from our pricing actions mentioned above as well as a higher percentage of new product sales that typically have higher gross margins, offset by sales of slow-moving inventory at lower margins, increased depreciation expense, and higher inbound freight and tariff costs.

Operating Expenses

The following table sets forth certain information regarding operating expenses for the fiscal years ended April 30, 2026 and 2025 (dollars in thousands):

2026 | 2025 | $ Change | % Change
Research and development | 6,087 | 7,710 | (1,623) | (21.1) | %
Selling, marketing, and distribution | 51,748 | 55,563 | (3,815) | (6.9) | %
General and administrative | 32,926 | 36,145 | (3,219) | (8.9) | %
Impairment of assets held for sale | 3,433 | — | 3,433 | 100.0 | %
Total operating expenses | 94,194 | 99,418 | (5,224) | (5.3) | %
% of net sales | 49.4 | % | 44.7 | %

Fiscal 2026 Operating Expenses Compared with Fiscal 2025

Total operating expenses of $94.2 million included a $3.4 million non-cash impairment charge during fiscal 2026 related to the write-down of the Disposal Group assets to estimated fair value less costs to sell. Total operating expenses, excluding this non-cash impairment charge, were $90.8 million, or $8.7 million lower than the prior fiscal year. Research and development expenses decreased $1.6 million, primarily from decreased depreciation expense for new product tooling compared to the prior fiscal year. Selling, marketing, and distribution expenses decreased $3.8 million from the prior fiscal year, primarily because of lower sales volume-related expenses, including outbound freight costs and commissions. General and administrative expenses decreased $3.2 million from the prior fiscal year primarily because of lower variable compensation-related expenses, cost-saving initiatives, and acquired intangible amortization expense, partially offset by higher public company costs.

Operating Loss

The following table sets forth certain information regarding operating loss for the fiscal years ended April 30, 2026 and 2025 (dollars in thousands):

2026 | 2025 | $ Change | % Change
Operating loss | (9,000) | (154) | (8,846) | NM
% of net sales (operating margin) | (4.7) | % | — | %

Fiscal 2026 Operating Loss Compared with Fiscal 2025

We recorded an operating loss of $9.0 million for fiscal 2026 compared to an operating loss of $154,000 in fiscal 2025. This decrease was primarily driven by lower net sales volume, partially offset by $5.2 million decrease in operating expenses.

Interest (Expense)/Income, Net

The following table sets forth certain information regarding interest (expense)/income, net for the fiscal years ended April 30, 2026 and 2025 (dollars in thousands):

2026 | 2025 | $ Change | % Change
Interest (expense)/income, net | (276) | 60 | (336) | NM

Fiscal 2026 Interest (Expense)/Income Compared with Fiscal 2025

Interest expense was $276,000 compared to interest income of $60,000 in the prior fiscal year as a result of servicing our borrowings on our credit facility during fiscal 2026. We had no borrowings on our revolving line as of April 30, 2026.

Income Taxes

The following table sets forth certain information regarding income tax expense for the fiscal years ended April 30, 2026 and 2025 (dollars in thousands):

2026 | 2025 | $ Change | % Change
Income tax expense | 45 | 123 | (78) | (63.4) | %
% of income from operations (effective tax rate) | (0.5) | % | 267.4 | % | (267.9) | %

Fiscal 2026 Income Tax Expense Compared with Fiscal 2025

We recorded an income tax expense of $45,000 for fiscal 2026 as compared to income tax expense of $123,000 for fiscal 2025. The income tax expense recorded for fiscal year 2026 and 2025 was primarily due to a full valuation allowance recorded against our deferred tax assets.

Net Loss

The following table sets forth certain information regarding net loss and the related per share data for the fiscal years ended April 30, 2026 and 2025 (dollars in thousands, except per share data):

2026 | 2025 | $ Change | % Change
Net loss | (9,208) | (77) | (9,131) | NM
Net loss per share
Basic and diluted | (0.73) | (0.01) | (0.72) | NM

Fiscal 2026 Net Loss Compared with Fiscal 2025

We had a net loss of $9.2 million, or $(0.73) per diluted share in fiscal 2026 compared to a net loss of $77,000, or $(0.01) per diluted share in fiscal 2025.

Non-GAAP Financial Measure

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-06-25_item1_business.md)

Item 1. Business

General

We are a leading provider of outdoor lifestyle products and shooting sports accessories encompassing hunting, fishing, meat processing, outdoor cooking, shooting, and personal security and defense products for rugged outdoor enthusiasts.

We conceive, design, produce or source, and sell our outdoor lifestyle products, including:

• premium sportsman knives and tools for fishing and hunting;

• land management tools for hunting preparedness and for use in the backyard;

• products used while hunting;

• meat processing equipment; and

• outdoor cooking products.

We conceive, design, produce or source, and sell our shooting sports accessories, including:

• rests, vaults, and other related accessories;

• electro-optical devices, including hunting optics, firearm aiming devices, flashlights, and laser grips;

• and reloading, gunsmithing, and firearm cleaning supplies.

We focus on our brands and the establishment of product categories in which we believe our brands will resonate strongly with the activities and passions of consumers and enable us to capture an increasing share of our overall addressable markets. Our owned brands include BOG, BUBBA, Caldwell, Crimson Trace, Frankford Arsenal, Grilla, Hooyman, Imperial, LaserLyte, Lockdown, MEAT! Your Maker, Old Timer, Schrade, Tipton, Uncle Henry, and Wheeler, and we license additional brands for use in association with certain products we sell, including M&P, Smith & Wesson, and Performance Center by Smith & Wesson. In focusing on the growth of our brands, we organize our product development, customer service, and marketing teams into four brand lanes, each of which focuses on one of four distinct consumer verticals – Adventurer, Harvester, Marksman, and Defender – with each of our brands included in one of the brand lanes. Our brand lane structure allows us to efficiently leverage talent, expertise, and resources across multiple brands while maintaining a strong focus on the unique needs of each consumer vertical. This approach provides the benefits of dedicated brand support in a more scalable and cost-effective manner than maintaining separate teams for every individual brand.

Our sales activities are focused on how we go to market within the e-commerce and traditional distribution channels. These two channels involve distinct strategies intended to increase revenue and enhance market share by placing our products where the consumer expects to find them. Our sales team is built around the two distribution channels and is organized into product categories and regions within the e-commerce and traditional channels and sells our products across all of our brands. We measure our success through sales performance in these distribution channels against prior results and our own expectations.

Our objective is to enhance our position as a leading provider of high-quality and innovative outdoor lifestyle products and shooting sports accessories for the hunting, fishing, outdoor cooking, shooting, personal security and defense, and other rugged outdoor markets and to expand our addressable market into carefully selected new product arenas.

Key elements of our strategy to achieve this objective and deliver long-term stockholder value are as follows:

• introduce a continuing stream of innovative new and differentiated rugged outdoor products and product extensions that appeal to consumers;

• leverage our innovation advantage to gain market share, enter new product categories, enter new consumer markets, and expand distribution;

• cultivate and enhance consumer relationships through our digital platforms;

• expand and diversify our supply chain;

• maintain an asset-light operating model that is designed to be agile; and

• pursue acquisitions that financially and strategically complement our current business.

We believe that throughout our history, we have been able to utilize our understanding of consumer needs to develop and introduce innovative new disruptive products with strong intellectual property protection that have continually increased our market share in their product categories, such as our Caldwell ClayCopter, which we believe represents our entry into the consumable targets market within the shotgun sports category. We have enhanced our product development capabilities, developed a multi-faceted marketing approach, improved our multi-channel distribution platform, and expanded and diversified our business through organic growth and strategic acquisitions.

Our net sales for the fiscal years ended April 30, 2026, 2025 and 2024 totaled $190.5 million, $222.3 million, and $201.1 million, respectively. Our gross profit for the fiscal years ended April 30, 2026, 2025, and 2024 totaled $85.2 million, $99.3 million, and $88.4 million, respectively. Total assets were $226.6 million as of April 30, 2026 and $246.4 million as of April 30, 2025.

Corporate Information

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-06-25_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-06-25_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-06-25_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-09-03_2-02-results.md, 10-K_2026-06-25_item7_mdna.md, 10-K_2026-06-25_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
