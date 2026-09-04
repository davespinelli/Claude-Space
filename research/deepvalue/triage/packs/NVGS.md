# Triage pack — NVGS · Navigator Holdings Ltd.

_Generated 2026-09-04 12:44 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** NVGS · **Name:** Navigator Holdings Ltd.
- **CIK:** 0001581804
- **SIC:** 4412 — Deep Sea Foreign Transportation of  Freight
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Annual report form:** 20-F — FOREIGN PRIVATE ISSUER. It files a 20-F (Item 4 = business, Item 5 = MD&A, Item 3.D = risk factors) and 6-Ks instead of a 10-K, 10-Q, 8-K and proxy. There is no quarterly 10-Q and no DEF 14A.
- **Filings fetched:** /Users/davidspinelli/Documents/Claude Space/research/deepvalue/filings/NVGS

## 2. Screen row (all metrics)

_Source: candidates.csv_

- **Name:** Navigator Holdings Ltd.
- **CIK:** 1,581,804 · **SIC:** 4412 (Deep Sea Foreign Transportation of  Freight) · **Exchange:** NYSE

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 22.62 |
| mktcap | $1.5B |
| ev | $1.3B |
| ev_ebit | 7.6x |
| fcf | $116.6M |
| fcf_yield | 7.9% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 12.9% |
| net_debt | -$225.9M |
| net_debt_ebit | -1.4x |
| cash | $225.9M |
| ltd | $0.00 |
| equity | $1.2B |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $587.0M |
| revenue_prior | $566.7M |
| rev_growth | 3.6% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $165.4M |
| net_income | $100.1M |
| cfo | $201.7M |
| capex | $85.0M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -6.0% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 65,250,444 |
| shares_py | 69,397,648 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 29.6% |
| r6m | 9.8% |
| off_52w_high | -6.3% |
| adv20 | $8.4M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.67 |
| r_ev_ebit | 0.89 |
| r_roic | 0.74 |
| r_rev_growth | 0.44 |
| r_buyback | 0.89 |
| score | 0.78 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q2I |
| shares_period | CY2025Q4I |
| shares_py_period | CY2024Q4I |
| capex_missing | False |
| ltd_missing | True |

**Screen rationale:** cheap at 7.6x EV/EBIT; buying back stock -6.0%; debt data missing (net cash unverified); 12-1 momentum 29.6%


## 3. Share count trend

- Shares outstanding: **65,250,444** (CY2025Q4I) vs **69,397,648** prior year (CY2024Q4I)
- Change: **-6.0%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

- Last 22.62 (as of 2026-09-03) · 52w range 14.40 - 24.29 · -6.9% vs 52w high · 57.1% above 52w low

_Source: yfinance, live._

## 5. Material 6-K events, last 6 months

_This is a foreign private issuer: it files 6-Ks, which carry no 8-K item codes, so these are the filings by headline rather than by item._

- **2026-08-04** — part ii second quarter 2026 conference call
- **2026-08-03** — navigator gas announces signing of 121 8
- **2026-07-14** — navigator gas announces signing of definitive
- **2026-06-18** — navigator gas announces signing of 205 8
- **2026-06-15** — navigator gas announces results of 2026 annual
- **2026-05-11** — 2 to ratify the appointment of
- **2026-05-06** — part ii first quarter 2026 conference call
- **2026-04-15** — navigator gas announces signing of non binding
- **2026-03-23** — subject to the sale of the securities by the
- **2026-03-20** — navigator gas announces pricing of upsized
- **2026-03-19** — navigator gas announces commencement of
- **2026-03-11** — part ii fourth quarter 2025 conference call

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 43,759 sh / $990,590 -> net $-990,590 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 5; transaction rows: 7 (open-market buys 0, sales 4).

| code | rows |
|---|---|
| F | 1 |
| M | 2 |
| S | 4 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (6-K exhibit from 6-K_2026-08-04_part-ii-second-quarter-2026-conference-call.md)

_This issuer reports on Form 6-K rather than 8-K._

_Extraction: started at the first release heading, 'Second Quarter Financial Highlights'; skipped 14 cover-page block(s) and 37 forward-looking-statement block(s); 11 block(s) of pre-heading matter dropped._

## Main document (nvgs-20260630.htm)

Second Quarter Financial Highlights

• For the quarter ended June 30, 2026, pursuant to the Company's capital return policy (the "Capital Return Policy") the Board of Directors of the Company declared, on August 4, 2026, a cash dividend of $0.07 per share of the Company's common stock, payable on September 1, 2026, to all shareholders of record as of the close of business U.S. Eastern Time on August 19, 2026, (the "Dividend"). The aggregate amount of the Dividend is expected to be approximately $4.3 million, which the Company anticipates will be funded from cash on hand.

• Also for the quarter ended June 30, 2026, pursuant to the Company's Capital Return Policy, the Company expects to repurchase approximately $14.2 million of its common stock between August 6, 2026, and September 30, 2026, subject to operating needs, market conditions, legal requirements, stock price and other circumstances (the "Share Repurchases"), such that the Dividend and the Share Repurchases together equal 35% of net income attributable to stockholders of the Company for the quarter ended June 30, 2026.

• For the quarter ending September 30, 2026, the Board of Directors of the Company approved, on August 4, 2026, an increase in the Fixed Element of the Company's Capital Return Policy to $0.08 per share of the Company's common stock, while maintaining that the Fixed Element and the Variable Element together should equal 35% of net income attributable to stockholders of the Company. The declaration of any dividends, and the amount of any such dividends or share repurchases, including with respect to the quarter ending September 30, 2026, remain subject to approval by the Company's Board of Directors following the conclusion of each quarter.

• For the quarter ended March 31, 2026, on June 10, 2026, the Company paid a dividend of $0.07 per share of the Company's common stock to all shareholders of record as of the close of business U.S. Eastern Time on May 20, 2026, totaling $4.3 million. The Company also repurchased 272,280 shares of common stock in the open market between March 16, 2026, and June 30, 2026, at an average price of $23.19 per share, totaling $6.3 million, such that the cash dividend and share repurchases together equaled 30% of net income attributable to stockholders of the Company in respect of the quarter ended March 31, 2026.

• The Company reported total operating revenues of $167.9 million for the three months ended June 30, 2026, compared to $129.6 million for the three months ended June 30, 2025. Disruption to transits through the Strait of Hormuz continued throughout the second quarter of 2026, constraining the availability of hydrocarbon products from the Middle East. End users sought alternative sources of supply, with Asian consumers in particular turning to North America for substitute volumes of LPG, ethane and ethylene. As a consequence, the price arbitrage between North America and Asia widened, supporting elevated freight rates for transportation between the two regions, while vessel utilization remained robust. Higher oil prices also increased demand for ethylene produced from competitively priced U.S. ethane. At the same time, a number of European crackers entered planned turnarounds, temporarily removing European ethylene production that had to be replaced by imports. These factors also resulted in record volumes of ethylene being exported through the Ethylene Export Terminal at Morgan's Point in the second quarter of 2026.

• Net income attributable to stockholders of the Company was $53.0 million for the three months ended June 30, 2026, compared to $21.5 million for the three months ended June 30, 2025.

• Adjusted net income attributable to stockholders of the Company 1 was $53.1 million for the three months ended June 30, 2026, compared to $22.2 million for the three months ended June 30, 2025. During the three months ended March 31, 2026, the Company revised its definition of Adjusted net income attributable to stockholders of the Company to no longer exclude profit/loss on sale of vessels. The Company believes this change provides improved comparability and better reflects overall earnings generated during the period, which earnings include contributions to net income arising from the Company's ongoing process of fleet renewal. Prior‑period Adjusted net income attributable to stockholders of the Company presented has been recast to conform to the current‑period presentation.

• EBITDA 2 was $101.6 million for the three months ended June 30, 2026, compared to $71.9 million for the three months ended June 30, 2025.

• Adjusted EBITDA 2 was $86.4 million for the three months ended June 30, 2026, compared to $60.1 million for the three months ended June 30, 2025.

1 Adjusted net income attributable to stockholders of Navigator Holdings Ltd. is not a measurement prepared in accordance with U.S. GAAP. Adjusted net income attributable to stockholders of Navigator Holdings Ltd. represents net income attributable to stockholders of Navigator Holdings Ltd. adjusted to exclude realized and unrealized gain/loss on non-designated derivative instruments and unrealized foreign currency exchange, write off of deferred financing costs, and other income. Management believes that EBITDA, Adjusted EBITDA, Adjusted Net Income Attributable to Stockholders of Navigator Holdings Ltd., Adjusted Basic Earnings per Share and Adjusted Diluted Earnings per Share are useful to investors in evaluating the operating performance of the Company but they do not represent and should not be considered alternatives to consolidated net income, earnings per share, cash generated from operations, or any other GAAP measure.

2 EBITDA and Adjusted EBITDA are not measurements prepared in accordance with U.S. GAAP. EBITDA represents net income before net interest expense, income taxes, depreciation and amortization. We define Adjusted EBITDA as EBITDA before profit/loss on sale of vessel, realized and unrealized gain/loss on non-designated derivative instruments and unrealized foreign currency exchange, write off of deferred financing costs, and other income. Management believes that EBITDA, Adjusted EBITDA, Adjusted Net Income Attributable to Stockholders of Navigator Holdings Ltd., Adjusted Basic Earnings per Share and Adjusted Diluted Earnings per Share are useful to investors in evaluating the operating performance of the Company but they do not represent and should not be considered alternatives to consolidated net income, earnings per share, cash generated from operations, or any other GAAP measure.

• Basic earnings per share attributable to stockholders of the Company was $0.86 for the three months ended June 30, 2026, compared to $0.31 per share for the three months ended June 30, 2025, with the increase primarily due to an increase in net income attributable to stockholders of Navigator Holdings Ltd., and by a lower number of shares of common stock in issue in the three months ended June 30, 2026, compared to the three months ended June 30, 2025.

• Adjusted basic earnings per share attributable to stockholders 3 of the Company was $0.86 per share for the three months ended June 30, 2026, compared to $0.32 per share for the three months ended June 30, 2025, driven primarily by an increase in Adjusted net income attributable to stockholders of the Company 4 , and by a lower number of shares of common stock in issue in the three months ended June 30, 2026, compared to the three months ended June 30, 2025.

• The Company increased its gross debt by $23.3 million to $920.4 million (net of deferred financing costs) during the three months ended June 30, 2026, as the Company made net repayments on loan facilities and revolving credit facilities of $71.1 million and the Company drew $28.5 million of the revolving credit portion of its $111.8 million December 2022 Term Loan and Revolving Credit Facility and $62.9 million of the revolving credit portion of its $147.6 million August 2024 Term Loan and Revolving Credit Facility, totaling $91.4 million. The Company reduced its gross debt by $3.1 million to $897.1 million (net of deferred financing costs) during the three months ended March 31, 2026, as the Company made net repayments on loan facilities and revolving credit facilities of $29.9 million, offset by the drawdown of $26.8 million from the March 2026 Senior Secured Term Loan (as defined below).

• At June 30, 2026, the Company's cash, cash equivalents, and restricted cash including available but undrawn credit facilities of $nil, was $273.8 million, compared to $291.0 million as of March 31, 2026, and $316.0 million as of June 30, 2025.

• On July 13, 2026, further to the non-binding letter of intent entered into on April 14, 2026, the Company entered into definitive agreements with Bernhard Schulte (Singapore) Holdings Pte. Ltd. ("Bernhard Schulte") and Sloman Neptun Schiffahrts-Aktiengesellschaft ("Sloman Neptun") for the sale of eight gas carriers (the "Unigas Vessels"), together with the Company's shareholding in Unigas International B.V. ("Unigas B.V."), the entity that commercially manages the Unigas Vessels through the Unigas Pool, for aggregate consideration of approximately $183.0 million (the "Unigas Transaction").

The combined book value in respect of the Unigas Vessels and the Company's holding in Unigas B.V. in the Company's accounts at June 30, 2026, was approximately $114.0 million. At June 30, 2026, the outstanding balance under the Company's May 2025 Secured Term Loan and RCF in respect of the Unigas Vessels was $18.3 million and was prepaid on July 27, 2026, and as a result all the security granted by the Company over Happy Albatross was released.

The Unigas Transaction, which is subject to customary closing conditions, as well as delivery of the Unigas Vessels pursuant to it, is expected to be completed by the fourth quarter of 2026 after which the Company's fleet, all other things being equal, will consist of 46 vessels, 18 of which will be ethylene and ethane-capable. The Company currently expects to recognize a profit on sale of the Unigas Vessels and the Company's holding in Unigas B.V. of between $66.0 million and $69.0 million, pursuant to the exact time at which each individual vessel is delivered based on operational practicalities.

3 Adjusted Basic Earnings per Share and Adjusted Diluted Earnings per Share are not measurements prepared in accordance with U.S. GAAP. Adjusted Basic Earnings per Share represents basic earnings per share adjusted to exclude realized and unrealized gain/loss on non-designated derivative instruments and unrealized foreign currency exchange, write off of deferred financing costs, and other income. Adjusted Diluted Earnings per Share represents Adjusted Basic Earnings per Share adjusting the weighted average number of common shares used for calculating Adjusted Basic Earnings per Share for the effects of all potentially dilutive shares. Management believes that EBITDA, Adjusted Net Income Attributable to Stockholders of Navigator Holdings Ltd., Adjusted Basic Earnings per Share and Adjusted Diluted Earnings per Share are useful to investors in evaluating the operating performance of the Company but they do not represent and should not be considered alternatives to consolidated net income, earnings per share, cash generated from operations, or any other GAAP measure.

_[...truncated at ~12,000 chars of this document]_

## 8. 20-F Item 5 - Operating and Financial Review and Prospects (MD&A) — Overview / Results of Operations (20-F_2026-03-12_item5_operating_review.md)

_Extraction: started at the Overview heading._

Overview

On December 31, 2025 we were the owner and operator of 57 liquefied gas carriers, which includes the world's largest fleet of handysize liquefied gas carriers. We also own a 50% share in an Ethylene Export Terminal at Morgan's Point, Texas on the Houston Ship Channel through our Export Terminal Joint Venture. We provide international and regional seaborne transportation services of petrochemical gases, LPG and ammonia for energy companies, industrial users and commodity traders. These gases are transported in liquefied form, by applying cooling and/or pressure, to reduce volume by up to 900 times dependin g on the cargo, making their transportation more efficient and economical.

We operate in one business segment. As of December 31, 2025, we owned and operated 57 vessels, eight of which were commercially managed through the independent Unigas Pool, and we commercially managed the other 49 vessels employing them under a combination of time charters, COA's and voyage charters on the spot market. As of December 31, 2025, 29 vessels were employed under time charters (December 31, 2024: 32 vessels), one was employed under a contract of affreightment (December 31, 2024: one vessel) and 19 were employed in the spot market (December 31, 2024: 14 vessels). Our 49 operated vessels earned an average time charter equivalent rate of approximately $30,110 per vessel per day ($915,832 per vessel per calendar month) during the year ended December 31, 2025, compared to approximately $28,826 per vessel per day ($876,776 per vessel per calendar month) for the year ended December 31, 2024.

Our Ethylene Export Terminal, owned by the Export Terminal Joint Venture, includes an ethylene cryogenic storage tank with a capacity of 30,000 tons, and has the capacity to export approximately 1.55 million tons of ethylene per year and load ethylene-capable gas carriers at rates of 1,000 tons per hour. Since January 2026, two new offtake contracts related to the Ethylene Export Terminal's available ethylene volumes have been signed by new customers, and we continue to expect that additional capacity will be contracted during 2026. Until further offtake contracts are signed, volumes will be sold and made available on a spot contract basis.

Fleet Renewal

On August 23, 2024, the Company entered into contracts to build the Original Two Newbuild Vessels. As part of the agreements then made, the Company held an option to build two additional vessels of the same specification and price. On November 21, 2024, the Company exercised the option and entered into contracts to build the Additional Two Newbuild Vessels. The total Four Ethylene Newbuild Vessels are scheduled to be delivered to the Company in March 2027, July 2027, November 2027 and January 2028 respectively, at an average shipyard price of $102.9 million per vessel. The Four Ethylene Newbuild Vessels will be able to carry a wide variety of gas products, ranging from complex petrochemical gases, including ethylene and ethane, to LPG and clean ammonia. Additionally, the Four Ethylene Newbuild Vessels will be fitted with dual-fuel engines for ethane, a low-carbon intensity transitional fuel, and made retrofit-ready for using ammonia as a fuel in the future, and additionally they will be capable of transiting through both the former and the new Panama Canal locks, providing enhanced flexibility.

The Company expects to finance the cost of the Four Ethylene Newbuild Vessels using debt and cash on hand, and the Company is well-progressed with arranging such third-party debt finance for all of the four vessels. The Company has signed a short-term time charter contract for one of its Four Ethylene Newbuild Vessels.

On January 7, 2025, the Company entered into an agreement to acquire three German-built 17,000 cubic meter capacity, ethylene-capable liquefied gas vessels (the "Purchased Vessels"). On February 19, 2025, the Company acquired the first of the three Purchased Vessels, now renamed Navigator

Hyperion for $27.4 million. On February 24, 2025, the Company acquired the second of the Purchased Vessels, now renamed Navigator Titan for $27.4 million. On March 17, 2025, the Company acquired the third of the Purchased Vessels, now renamed Navigator Vesta , for $29.2 million.

On February 7, 2025, the Company entered into a $74.6 million Senior Secured Term Loan (the "February 2025 Facility") with Nordea Bank Abp, to partially finance the purchase price of the three Purchased Vessels and used cash on hand to pay the remainder of the purchase price. The February 2025 Facility is initially non-amortizing, bears interest at a rate of Term SOFR plus 180 basis points and matures after 18 months. At that time, the borrower has an option to extend the February 2025 Facility for a further 18 months on payment of a $25 million balloon. Should the borrower take the extension option the February 2025 Facility will become amortizing with repayments made on the basis of an age-adjusted 20 to 0 years repayment profile and bear interest at Term SOFR plus 180 basis points.

On July 17, 2025, the Company announced that it had entered into a joint venture agreement with Amon Gas. The Amon Joint Venture intends to acquire two newbuild 51,530 cubic-meter capacity ammonia-fueled, ice-class, liquefied ammonia carriers, which will also be capable of carrying liquefied petroleum gas ("the Two Ammonia Newbuild Vessels"). On December 31, 2025, the Company owned 61% of the Amon Joint Venture, and Amon Gas owned 39%. Under the terms and conditions of the investment, the Company expects to own 79.5% of the Amon Joint Venture and Amon Gas expects to own 20.5% when the vessels are delivered in 2028.

The Amon Joint Venture has entered into contracts with Nantong CIMC Sinopacific Offshore & Engineering Co., Ltd. to build the Two Ammonia Newbuild Vessels, with deliveries scheduled to take place in June and October 2028 respectively, at an average yard price of $87 million per vessel. Each of the Two Ammonia Newbuild Vessels has been awarded a NOK 90 million (approx. $9 million) investment grant from the Norwegian government agency Enova to be drawn down in accordance with the agreed terms over the course of the vessels' construction period. In addition to the Enova Grant, it is expected that the Amon Joint Venture will finance the remainder of the purchase price of the Two Ammonia Newbuild Vessels through commercial bank finance, with the remainder sourced from capital contributions from the Company and Amon Gas. The Company expects to finance its share of the capital contributions from available cash resources.

Once delivered, subject to customary conditions, each of the Two Ammonia Newbuild Vessels is expected to be operated by the Amon Joint Venture pursuant to a five-year time charter with Yara International ASA ("Yara").

During 2025, the Company sold two vessels, Navigator Venus, a 2000-built 22,085 cbm ethylene-capable semi-refrigerated handysize vessel and Navigator Gemini, a 2009-built 20,750 cbm semi-refrigerated handysize vessel.

Legal Overview

The Company in 2026 intends to seek shareholder approval in connection with a potential change in its corporate domicile from the Marshall Islands to England and Wales (the "Company Redomiciliation"). In connection with the Company Redomiciliation, the Company also has plans to redomicile various of its subsidiaries to England and Wales and / or Denmark and has formed new English and Danish subsidiaries and plans to move applicable assets of its various subsidiaries to the newly formed entities (the "Subsidiary Redomiciliations" and, together with the Company Redomiciliation, the "Redomiciliations"). The Company expects that the Redomiciliations will better align the Company's corporate structure with its current and future business activities and financing plans. Our Board of Directors (the "Board") has not yet approved the Company Redomiciliation, which will also need to be put before a meeting of the Company's shareholders. If shareholder approval of the Company Redomiciliation is received and the Redomiciliations are ultimately completed, we do not expect that the Redomiciliations will have a material impact on our employees, our day-to-day business and operations, or our services to customers. We do not yet know when the Company Redomiciliation will be presented to the Company's shareholders, if at all. However, we have been working to present the matter to the Company's shareholders at our next Annual General Meeting, which we expect to take place in or around June 2026.Nothing in this report should be construed as an offer to sell, or the solicitation of an offer to buy, any securities in connection with the potential Redomiciliations, nor an agreement or promise that any redomiciliation will occur, nor is it a solicitation of any vote, consent or approval in connection with the potential Company Redomiciliation.

If the planned Company Redomiciliation is not completed on the expected schedule, or if the planned Company Redomiciliation is not completed at all, trading in our common stock could be negatively affected. The market prices of our common stock currently and in the period prior to completion of the Company Redomiciliation (or failing to complete the Company Redomiciliation) may reflect a market assumption that the Company Redomiciliation will be completed. If the Company Redomiciliation is not completed, this could result in a negative perception by the stock market of the Company generally and a decline in the market price of our common stock.

_[...truncated at ~10,000 chars of this document]_

## 9. 20-F Item 4 - Information on the Company (20-F_2026-03-12_item4_business.md)

Item 4. | Information on the Company

A. | History and Development of the Company

General

Navigator Holdings Limited., which is also commercially known as Navigator Gas, was formed in 1997 as an Isle of Man public limited company for the original purpose of building and operating a fleet of five semi-refrigerated, ethylene-capable liquefied gas carriers. In March 2008, we redomiciled as a corporation in the Republic of the Marshall Islands and we maintain our principal executive offices at 10 Bressenden Place, London, SW1E 5DH, United Kingdom. Our telephone number at that address is +44 20 7340 4850. Our agent for service of process in the United States is Puglisi & Associates and its address is 850 Library Avenue, Suite 204, Newark, Delaware, 19711.

In November 2013, we completed our initial public offering of 13,800,000 shares of our common stock, comprising 9,030,000 new shares of common stock and certain selling shareholders offered 4,770,000 shares of common stock.

In August 2021, we issued 21,202,671 shares of our common stock to Naviera Ultranav Limitada as consideration for the acquisition of the fleet and businesses of Ultragas ApS ("Ultragas" and such transaction, the "Ultragas Transaction"). As of December 31, 2025, we had 65,250,444 shares of our common stock outstanding. Please see "Item 7—Major Shareholders and Related Party Transactions."

As of December 31, 2025 we own and operate 57 liquefied gas carriers, including the world's largest fleet of handysize liquefied gas carriers. We also own a 50% share in an ethylene export marine terminal at M organ's Point, Texas (the "Ethylene Export Terminal") through a joint venture (the "Export Terminal Joint Venture"). The Ethylene Export Terminal throughput capacity is approximately 1.55 million tons per annum.

The Company in 2026 intends to seek shareholder approval in connection with a potential change in its corporate domicile from the Marshall Islands to England and Wales (the "Company Redomiciliation"). In connection with the Company Redomiciliation, the Company also has plans to redomicile various of its subsidiaries to England and Wales and / or Denmark and has formed new English and Danish subsidiaries and plans to move applicable assets of its various subsidiaries to the newly formed entities (the "Subsidiary Redomiciliations" and, together with the Company Redomiciliation, the "Redomiciliations"). The Company expects that the Redomiciliations will better align the Company's corporate structure with its current and future business activities and financing plans.

Our Board of Directors (the "Board") has not yet approved the Company Redomiciliation, which will also need to be put before a meeting of the Company's shareholders. If shareholder approval of the Company Redomiciliation is received and the Redomiciliations are ultimately completed, we do not expect that the Redomiciliations will have a material impact on our employees, our day-to-day business and operations, or our services to customers. We do not yet know when the Company Redomiciliation will be presented to the Company's shareholders, if at all. However, we have been working to present the matter to the Company's shareholders at our next Annual General Meeting, which we expect to take place in or around June 2026.

Nothing in this report should be construed as an offer to sell, or the solicitation of an offer to buy, any securities in connection with the potential Redomiciliations, nor an agreement or promise that any redomiciliation will occur, nor is it a solicitation of any vote, consent or approval in connection with the potential Company Redomiciliation.

Our shares of common stock are traded on the New York Stock Exchange under the ticker symbol "NVGS."

A copy of this Annual Report on Form 20-F can be obtained, free of charge, on our website at www.navigatorgas.com, or by writing to our principal executive office. The SEC maintains a website that contains reports, proxy and information statements, and other information regarding issuers that file

electronically with the SEC at http://www.sec.gov. Information contained on any website referenced in this Annual Report on Form 20-F is not incorporated by reference herein.

B. | Business Overview

We play a vital role in the liquefied gas supply chain for energy companies, industrial consumers and commodity traders, with our sophisticated vessels providing an efficient and reliable 'floating pipeline' between the parties. We carry LPG for major international energy companies, state-owned utilities and reputable commodities traders. LPG, which consists of propane and butane, is a relatively clean alternative energy source with more than 1,000 applications, including as a heating, cooking and transportation fuel, and as a petrochemical and refinery feedstock. LPG is a by-product of oil refining and natural gas extraction and shale gas, principally from the U.S.

We also carry petrochemical gases for numerous industrial users. Petrochemical gases, including ethylene, propylene, butadiene and vinyl chloride monomer, are derived from the cracking of petroleum feedstocks such as ethane, LPG and naphtha and are primarily used as raw materials in various industrial processes like the manufacture of plastics, vinyl, and rubber, with a wide application of end uses. Our vessels also carry ammonia for the producers of fertilizers, a main use of ammonia for the agricultural industry, and for ammonia traders.

Our Fleet and Terminal Assets

On December 31, 2025 we were the owner and operator of 57 liquefied gas carriers, which includes the world's largest fleet of handysize liquefied gas carriers. We also own a 50% share in an ethylene export marine terminal at Morgan's Point, Texas on the Houston Ship Channel (the "Ethylene Export Terminal") through a joint venture (the "Export Terminal Joint Venture").

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

- **CALL PERIOD: 2026Q1** (call dated 2026-05-06)
- **Recency:** STALE: this call covers 2026Q1, but the latest earnings release in this pack (section 7, 6-K_2026-08-04_part-ii-second-quarter-2026-conference-call.md) covers 2026Q2. Everything said below predates those results — do not read it as commentary on the current quarter.
- **File:** transcript_2026Q1_2026-05-06.md
- **Type:** EARNINGS PRESS RELEASE ONLY, not the call — no Q&A, no unscripted management commentary. Do not attribute call quotes to this.
- **Source:** https://www.sec.gov/Archives/edgar/data/1581804/000162828026030922/q12026navigatorholdingsltd.htm

6-K

1

q12026navigatorholdingsltd.htm

6-K

Document
UNITED STATES
SECURITIES AND EXCHANGE COMMISSION
WASHINGTON, D.C. 20549

Form 6-K

REPORT OF FOREIGN PRIVATE ISSUER
PURSUANT TO RULE 13a-16 OR 15d-16
UNDER THE SECURITIES EXCHANGE ACT OF 1934
For the Quarter Ended March 31, 2026
Commission File Number 001-36202

NAVIGATOR HOLDINGS LTD.
(Translation of registrant’s name into English)

c/o NGT Services (UK) Ltd
10 Bressenden Place,
London, SW1E 5DH,
United Kingdom
(Address of principal executive office)

Indicate by check mark whether the registrant files or will file annual reports under cover of Form 20-F or Form 40-F.
Form 20-F
☒
Form 40-F
☐

1
NAVIGATOR HOLDINGS Ltd.
REPORT ON FORM 6-K FOR THE THREE MONTHS ENDED MARCH 31, 2026
INDEX
PAGE
PART I. Management’s Discussion and Analysis of Financial Condition and Results of Operations for the three months ended March 31, 2026, and Unaudited Condensed Consolidated Financial Statements
Important Information Regarding Forward-Looking Statements
3
Quantitative and Qualitative Disclosures About Market Risk
19
Unaudited Condensed Consolidated Financial Statements
Unaudited Condensed Consolidated Statements of Operations for the three months ended March 31, 2026, and 2025
F-
1
Unaudited Condensed Consolidated Statements of Comprehensive Income for the three months ended March 31, 2026, and 2025
F-
2
Unaudited Condensed Consolidated Balance Sheets as of March 31, 2026, and December 31, 2025
F-
3
Unaudited Condensed Consolidated Statements of Stockholders’ Equity for the three months ended March 31, 2026, and 2025
F-
4
Unaudited Condensed Consolidated Statements of Cash Flows for the three months ended March 31, 2026, and 2025
F-
5
Our Fleet
F-
18
Part II. First Quarter 2026 Conference Call Details
29
Signatures
30
The Information under “Part I. Management’s Discussion and Analysis of Financial Condition and Results of Operations for the three months ended March 31, 2026, and Unaudited Condensed Consolidated Financial Statements” of this report on Form 6-K is incorporated by reference into the following registration statements of the registrant: Form F-3 (File No. 333-272980) originally filed with the Securities and Exchange Commission on June 28, 2023; and Form S-8 (File No. 333-278593) originally filed with the Securities and Exchange Commission April 10, 2024.
2
PART I. Management’s Discussion and Analysis of Financial Condition and Results of Operations for the three months ended March 31, 2026, and Unaudited Condensed Consolidated Financial Statements
IMPORTANT INFORMATION REGARDING FORWARD-LOOKING STATEMENTS

_[...truncated at ~3,000 chars of this document]_

## 11. Document availability

**Annual report form:** 20-F (foreign private issuer)

| role | source item | file |
|---|---|---|
| Business description | 20-F Item 4 - Information on the Company | 20-F_2026-03-12_item4_business.md |
| MD&A / management commentary | 20-F Item 5 - Operating and Financial Review and Prospects (MD&A) | 20-F_2026-03-12_item5_operating_review.md |
| Risk factors | 20-F Item 3.D - Risk Factors | 20-F_2026-03-12_item3d_risks.md |

**Present:** meta.json, form4_summary.md, 6-K_2026-08-04_part-ii-second-quarter-2026-conference-call.md, 20-F_2026-03-12_item5_operating_review.md, 20-F_2026-03-12_item4_business.md, transcript_2026Q1_2026-05-06.md

**Missing:** current-period call material (STALE)

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
