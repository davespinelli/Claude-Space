# Triage pack — EVTC · EVERTEC, Inc.

_Generated 2026-09-04 13:14 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** EVTC · **Name:** EVERTEC, Inc.
- **CIK:** 0001559865
- **SIC:** 7374 — Services-Computer Processing & Data Preparation
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/EVTC

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** EVERTEC, Inc.
- **CIK:** 1,559,865 · **SIC:** 7374 (Services-Computer Processing & Data Preparation) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 30.57 |
| mktcap | $1.8B |
| ev | $2.8B |
| ev_ebit | 15.0x |
| fcf | $203.7M |
| fcf_yield | 11.2% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 9.2% |
| net_debt | $961.2M |
| net_debt_ebit | 5.2x |
| cash | $260.7M |
| ltd | $1.2B |
| equity | $641.4M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $931.8M |
| revenue_prior | $845.5M |
| rev_growth | 10.2% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $186.4M |
| net_income | $145.0M |
| cfo | $227.0M |
| capex | $23.3M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -6.6% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 59,752,542 |
| shares_py | 63,982,005 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -8.3% |
| r6m | 6.9% |
| off_52w_high | -11.2% |
| adv20 | $11.2M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.74 |
| r_ev_ebit | 0.58 |
| r_roic | 0.68 |
| r_rev_growth | 0.66 |
| r_buyback | 0.91 |
| score | 0.71 |

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
| rank | 51 |

**Screen rationale:** buying back stock -6.6%


## 3. Share count trend

- Shares outstanding: **59,752,542** (CY2026Q2I) vs **63,982,005** prior year (CY2025Q2I)
- Change: **-6.6%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-05-20** — Item 1.01 (Entry into a Material Definitive Agreement): On May 18, 2026, Evertec, Inc. ("Evertec" or the "Company"), Evertec Group, LLC ("Borrower"), a wholly-owned indirect subsidiary of Evertec, and other Loan Parties (as defined in the Existing Credit Agreement (as defined below)) party thereto, entered into a...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 16,202 sh / $427,999 vs sells 48,056 sh / $1,477,248 -> net $-1,049,249 (SELLING).
Distinct insiders buying (code P): 1. Largest buy: SMITH BRIAN JOHN bought 16,202 sh @ $26.42 ($427,999) on 2026-06-12.

Form 4 filings parsed: 12; transaction rows: 12 (open-market buys 1, sales 5).

| code | rows |
|---|---|
| A | 5 |
| F | 1 |
| P | 1 |
| S | 5 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-04_2-02-results.md)

_Extraction: started at the first release heading, 'EVERTEC REPORTS SECOND QUARTER 2026 RESULTS'; skipped 10 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (ex991063026.htm)

EVERTEC REPORTS SECOND QUARTER 2026 RESULTS

Raises Full-Year 2026 Outlook

Increases share repurchase authorization

Signs strategic agreements with Transbank and Clip

SAN JUAN, PUERTO RICO – August 4, 2026 – EVERTEC, Inc. (NYSE: EVTC) ("Evertec" or the "Company") today announced results for the second quarter ended June 30, 2026.

Second Quarter 2026 Highlights and Recent Highlights

• Revenue increased 20% to $274.8 million, approximately 16% on a constant currency basis

• GAAP Net Income attributable to common shareholders was $5.4 million, or $0.09 per diluted share

• Adjusted EBITDA increased 18% to $109.3 million and Adjusted earnings per common share increased 18% to $1.05

• Returned $50.1 million to shareholders through share repurchases and dividends

• Advanced EVERTEC's growth strategy in Latin America through agreements with Transbank in Chile and Clip in Mexico

• Increased the share repurchase authorization to $150 million

• Raised full-year 2026 Revenue and Adjusted earnings per common share outlook

Mac Schuessler, President and Chief Executive Officer stated "We delivered a strong second quarter, reflecting organic growth across our business, the contributions from our recent acquisitions, and the continued execution of our strategy. Given our strong first-half performance and outlook for the remainder of the year, we are raising our full-year guidance and remain focused on executing our strategy."

Second Quarter 2026 Results

Revenue. Total revenue for the quarter ended June 30, 2026 was $274.8 million, an increase of 20%, compared with $229.6 million in the prior year quarter driven by organic growth across most of the Company's segments, contributions from the recent acquisitions completed in the current and prior year and favorable foreign currency fluctuations. Constant currency revenue amounted to $265.7 million representing growth of 16%. Merchant acquiring revenue benefited from higher sales volume, higher non-transactional revenues and an improvement in spread. Payments Puerto Rico revenue benefited from higher POS transactions and growth in ATH Movil, primarily in ATH Movil Business, as well as a non-recurring volume-based benefit recognized during the quarter. Latin America revenue benefited from the contributions of recent acquisitions, and continued organic growth across the region. Revenue also benefited from foreign currency exchange rate fluctuations of $9.1 million, primarily in Brazil. Business Solutions revenue contracted mainly as a result of the 10% discount to Popular that came into effect in the fourth quarter of 2025.

Net Income attributable to common shareholders. For the quarter ended June 30, 2026, GAAP Net Income attributable to common shareholders was $5.4 million or $0.09 per diluted share, compared with $40.5 million or $0.62 per diluted share in the prior year quarter. The decrease was driven in part by certain non-recurring items, including impairment charges associated with the Company's strategic decision to exit an equity method investment, as well as costs related to cybersecurity incident response and remediation activities. The quarter also reflected costs associated with recent acquisitions, including integration related costs, higher depreciation and amortization related to acquired intangible assets, and increased interest expense resulting from higher outstanding debt balances, following recent acquisitions. Income tax expense was also higher, primarily driven by discrete tax items, including taxes associated with a dividend distribution used to partially fund the Dimensa acquisition and a valuation allowance recorded against capital losses generated by the exit of the equity investment, as well as a greater proportion of taxable income generated in higher-tax foreign jurisdictions. While these items impacted reported GAAP results,

the Company continued to generate strong underlying operating performance, as reflected in its adjusted results and continued growth across its core businesses.

Adjusted EBITDA and Adjusted EBITDA Margin . For the quarter ended June 30, 2026, Adjusted EBITDA was $109.3 million, an increase of $16.8 million when compared to the prior year quarter, driven by the increase in revenues. Adjusted EBITDA margin (Adjusted EBITDA as a percentage of total revenue) was 39.8%, compared with 40.3% in the prior year. The modest decrease primarily reflects the higher contribution from the Latin America segment.

Adjusted Net Income and Adjusted earnings per common share . For the quarter ended June 30, 2026, Adjusted Net Income was $64.8 million, an increase of $7.1 million when compared with $57.7 million in the prior year quarter. The increase is primarily driven by the higher Adjusted EBITDA, partially offset by a higher adjusted effective tax rate, primarily reflecting the higher contribution from the Latin America segment, higher operating depreciation and amortization expense, and the impact from non-controlling interest associated with the Tecnobank acquisition completed in the fourth quarter of 2025. Adjusted earnings per common share was $1.05, an increase of 18% compared with $0.89 in the prior year quarter, driven by the Adjusted Net Income results and a lower share count reflecting the impact of share repurchases completed during the current and prior year.

Share Repurchase

During the three months ended June 30, 2026, the Company repurchased 1,907,437 shares of its common stock at an average price of $24.68 per share for a total of $47.1 million.

On July 31, 2026, the Company's Board of Directors approved an increase to the share repurchase authorization to an aggregate $150 million, while maintaining the current expiration date of December 31, 2027. Prior to this authorization increase, approximately $83.0 million remained available under the program. The Company may repurchase shares in the open market, through accelerated share repurchase programs, 10b5-1 plans, or in privately negotiated transactions, subject to business opportunities and other factors.

2026 Outlook

The Company's revised financial outlook for 2026 is as follows:

• We now expect revenue between $1,085 million and $1,095 million representing growth of approximately 16.4% to 17.5%, an increase from our previous expectation of 15.1% to 16.4%. Constant currency growth is now expected to be between 14.5% to 15.6%.

• We now expect Adjusted earnings per common share to be between $3.94 to $4.04 representing growth of approximately 8.8% to 11.7%, an increase from our previous expectation of 6.6% to 9.9%. On a constant currency basis, growth is expected to be between 7.2% to 10.0%.

• We continue to expect Adjusted EBITDA margin of 39% to 40%

• We continue to expect capital expenditures to be approximately $90 million

• We continue to expect an adjusted effective tax rate of approximately 11% to 12%

Earnings Conference Call and Audio Webcast

The Company will host a conference call to discuss its second quarter 2026 financial results today at 4:30 p.m. ET. Hosting the call will be Mac Schuessler, President and Chief Executive Officer, and Karla Cruz-Jusino, Chief Financial Officer. The conference call can be accessed live over the phone by dialing (800) 715-9871 or for international callers by dialing (646) 307-1963. A replay will be available one hour after the end of the conference call and can be accessed by dialing (855) 669-9658 or (412) 317-0088 for international callers; the pin number is 6110327. The replay will be available through Tuesday, August 11, 2026. The call will be webcast live from the Company's website at www.evertecinc.com under the Investor Relations section or directly at http://ir.evertecinc.com. A supplemental slide presentation that accompanies this call and webcast can be found on the investor relations website at ir.evertecinc.com and will remain available after the call.

About Evertec

EVERTEC, Inc. (NYSE: EVTC) is a leading full-service transaction processor and financial technology provider in Latin America, Puerto Rico and the Caribbean, providing a broad range of merchant acquiring, payment services and business process management services. Evertec owns and operates the ATH® network, one of the leading personal identification number ("PIN") debit networks in Latin America. In addition, the Company manages a system of electronic payment networks and offers a comprehensive suite of services for core banking, cash processing and fulfillment in Puerto Rico, that process over ten billion transactions annually. The Company also offers financial technology outsourcing in all the regions it serves. Based in

Puerto Rico, the Company operates in 26 Latin American countries and serves a diversified customer base of leading financial institutions, merchants, corporations and government agencies with "mission-critical" technology solutions. For more information, visit www.evertecinc.com.

Use of Non-GAAP Financial Information

The non-GAAP measures referenced in this earnings release are supplemental measures of the Company's performance and are not required by, or presented in accordance with, accounting principles generally accepted in the United States of America ("GAAP"). They are not measurements of the Company's financial performance under GAAP and should not be considered as alternatives to total revenue, net income or any other performance measures derived in accordance with GAAP or as alternatives to cash flows from operating activities, as indicators of operating performance or as measures of the Company's liquidity. In addition to GAAP measures, management uses these non-GAAP measures to focus on the factors the Company believes are pertinent to the daily management of the Company's operations and believes that they are also frequently used by analysts, investors and other stakeholders to evaluate companies in our industry. These measures have certain limitations in that they do not include the impact of certain expenses that are reflected in our condensed consolidated statements of operations that are necessary to run our business. Other companies, including other companies in our industry, may not use these measures or may calculate these measures differently than as presented herein, limiting their usefulness as comparative measures.

Reconciliations of the non-GAAP measures to the most directly comparable GAAP measure are included at the end of this earnings release. These non-GAAP measures include Constant currency revenue, EBITDA, Adjusted EBITDA, Adjusted Net Income, Adjusted Earnings per common share, and Constant Currency Adjusted Earnings per common share, each as defined below.

Constant currency revenue represents reported revenue excluding the impact of fluctuations in foreign currency exchange rates in the current period. Constant currency revenue is calculated by applying prior-year period foreign currency exchange rates to current-period revenue.

EBITDA is defined as earnings before interest, taxes, depreciation and amortization.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-02_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

EVERTEC is a leading full-service transaction-processing business and financial technology provider in Latin America, Puerto Rico and the Caribbean, providing a broad range of merchant acquiring, payment services and business solutions. We believe we are one of the largest merchant acquirers in Latin America based on total number of transactions and we also believe we are the largest merchant acquirer in the Caribbean. We serve 26 countries out of 24 offices, including our headquarters in Puerto Rico. We own and operate the ATH network, which we believe is one of the leading debit networks in Latin America. We process over ten billion transactions annually through a system of electronic payment networks in Puerto Rico and Latin America and provide a comprehensive suite of services for core banking, cash processing, fulfillment in Puerto Rico and a "one stop shop" set of products for the financial sector in Latin America, which include solutions such as core banking, investments, asset management, pension funds and consortium. Additionally, we offer managed services, managed security services and payment transactions fraud monitoring to all the regions where we do business. We serve a diversified customer base of leading financial institutions, merchants, corporations, and government agencies with "mission-critical" technology solutions that enable them to issue, process and accept transactions securely. We believe our business is well-positioned to continue to expand across the fast-growing Latin America region.

We are differentiated, in part, by our diversified business model, which enables us to provide our varied customer base with a broad range of transaction-processing services from a single source across numerous channels and geographic markets. We believe this capability provides several competitive advantages that will enable us to continue to penetrate our existing customer base with complementary new services, gain new customers, develop new sales channels, and enter new markets. We believe these competitive advantages include:

• Our ability to provide competitive products;

• Our ability to provide in one package a range of services that traditionally had to be sourced from different vendors;

• Our ability to serve customers with disparate operations in several geographies with technology solutions that enable them to manage their business as one enterprise; and

• Our ability to capture and analyze data across the transaction-processing value chain and use that data to provide value-added services that are differentiated from those offered by pure-play vendors that serve only one portion of the transaction-processing value chain (such as only merchant acquiring or only payment services).

Our broad suite of services spans the entire payment processing value chain and includes a range of front-end customer-facing solutions such as the electronic capture and authorization of transactions at the point-of-sale for both card present transactions and card-not-present transactions, as well as back-end support services such as the clearing and settlement of transactions and account reconciliation for card issuers. These include: (i) merchant acquiring services, which enable point of sales ("POS") and e-commerce merchants to accept and process electronic methods of payment such as debit, credit, prepaid and electronic benefit transfer ("EBT") cards; (ii) payment processing services, which enable financial institutions and other issuers to manage, support and facilitate the processing for credit, debit, prepaid, automated teller machines ("ATM") and EBT card programs; and (iii) business process management solutions, which provide "mission-critical" technology solutions such as core bank processing, as well as IT outsourcing and cash management services to financial institutions, corporations and governments. We provide these services through scalable, end-to-end technology platforms that we manage and operate in-house and that generate significant operating efficiencies that enable us to maximize profitability.

We sell and distribute our services primarily through a proprietary direct sales force with established customer relationships. We continue to pursue joint ventures and merchant acquiring alliances. We benefit from an attractive business model, the hallmarks of which are recurring revenue, scalability, significant operating margins and moderate capital expenditure requirements. Our revenue is predominantly recurring in nature because of the mission-critical and embedded nature of the

services we provide. In addition, we generally enter into multi-year contracts with our customers. We believe our business model should enable us to continue to grow our business organically in the primary markets we serve without significant incremental capital expenditures.

2025 Developments

On July 30, 2025 the Board approved an increase to Evertec's existing share repurchase authorization to permit future repurchases of up to an aggregate of $150 million worth of shares of the Company's common stock, par value $0.01 per share by December 31, 2026. Under the repurchase program, the Company may repurchase shares in the open market, through accelerated share repurchase programs, Rule 10b5-1 plans, or in privately negotiated transactions, subject to business opportunities and other factors.

On October 1, 2025, Evertec Brasil Informática S.A. ("Evertec BR"), a wholly-owned subsidiary of EVERTEC, Inc., completed the previously announced purchase of 75% of the share capital of Tecnobank Tecnologia Bancária S.A. ("Tecnobank"). Tecnobank is a leading fintech vendor in Brazil's digital vehicle financing contract registration sector. This transaction enhances the Company's existing product offerings.

Factors and Trends Affecting the Results of Our Operations

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations
Years ended December 31,
(In thousands) | 2025 | 2024 | Variance
Revenues | 931,818 | 845,486 | 86,332 | 10 | %
Operating costs and expenses
Cost of revenues, exclusive of depreciation and amortization shown below | 469,128 | 406,416 | 62,712 | 15 | %
Selling, general and administrative expenses | 154,164 | 145,558 | 8,606 | 6 | %
Depreciation and amortization | 122,086 | 127,846 | (5,760) | (5) | %
Total operating costs and expenses | 745,378 | 679,820 | 65,558 | 10 | %
Income from operations | 186,440 | 165,666 | 20,774 | 13 | %

Revenues

Total revenues for the year ended December 31, 2025 was $931.8 million, an increase of $86.3 million or 10% compared with $845.5 million in the prior year period driven by organic growth across all of the Company's segments and the contribution from the acquisitions completed in the fourth quarter of 2025 and 2024. Merchant acquiring revenue benefited from the positive impact from sales volume growth, an improvement in spread, and higher non-transactional revenues. Payments Puerto Rico revenue benefited from ATH Movil transaction and sales volume growth, primarily in the ATH Business as well as POS transaction growth. Latin America revenues were positively impacted by the contribution from acquisitions completed in the current and prior year, continued organic growth across the region, as well as the strong performance in Brazil. Business Solutions revenue increased as a result of higher network services, an increase in consulting services and projects completed throughout the current and prior year, partially offset by the 10% discount to Popular that came into effect in the fourth quarter of 2025.

Cost of revenues

Cost of revenues, exclusive of depreciation and amortization, for the year ended December 31, 2025 amounted to $469.1 million, an increase of $62.7 million or 15% when compared to the same period in the prior year. This increase was primarily related to the expenses associated with contractual claims related to client losses from the Pix incident in Brazil, an increase in cost of sales, an increase in personnel costs, partially due to acquisitions completed in the fourth quarter of the current and prior year coupled with higher professional services related to strategic projects and an increase in cloud services.

Selling, general and administrative

Selling, general and administrative expenses for the year ended December 31, 2025, amounted to $154.2 million, an increase of $8.6 million or 6% when compared to the same period in the prior year. This increase was mainly driven by an increase in personnel costs as well as an increase in cloud services partially offset by lower professional fees.

Depreciation and amortization

Depreciation and amortization expense for the year ended December 31, 2025 amounted to $122.1 million, a decrease of $5.8 million or 5% when compared to the same period in the prior year. The decrease was primarily driven by intangible assets that became fully amortized during the prior year, partially offset by the intangible assets recognized in recent acquisitions.

Non-operating expenses

Years ended December 31,
(In thousands) | 2025 | 2024 | Variance
Interest income | 15,035 | 13,332 | 1,703 | 13 | %
Interest expense | (68,278) | (74,733) | 6,455 | (9) | %
Gain (loss) on foreign currency remeasurement | 592 | (5,198) | 5,790 | (111) | %
Earnings from equity investees | 5,094 | 4,298 | 796 | 19 | %
Other income | 15,492 | 16,261 | (769) | (5) | %
Total non-operating expenses | (32,065) | (46,040) | 13,975 | (30) | %

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-02_item1_business.md)

Item 1. Business

Except as otherwise indicated or unless the context otherwise requires, (a) the terms "EVERTEC," "we," "us," "our," "our Company" and "the Company" refer to EVERTEC, Inc. and its subsidiaries on a consolidated basis and, (b) the term "EVERTEC Group" refers to EVERTEC Group, LLC and its predecessor entities and their subsidiaries on a consolidated basis. EVERTEC Inc.'s subsidiaries include Holdings, EVERTEC Group; EVERTEC Dominicana, SAS; Evertec Chile Holdings SpA; Evertec Chile SpA; Evertec Chile Global SpA; Evertec Chile Servicios Profesionales SpA; Paytrue S.A.; Caleidon; S.A.; Evertec Brasil Solutions Informática S.A. ("EVERTEC BR"); EVERTEC Panamá, S.A.; EVERTEC Costa Rica, S.A. ("EVERTEC CR"); Zunify Payments Ltda; EVERTEC Guatemala, S.A.; Evertec Colombia, SAS;, EVERTEC USA, LLC; OPG Technology Corp.; Evertec Placetopay, SAS ("PlacetoPay"); BBR Chile, SpA and BBR Perú, S.A.C.,(collectively "BBR"); Paysmart Pagamentos Eletronicos Ltda, Issuer Holding Ltda. and Issuer Instituição de Pagamentos Ltda (collectively "paySmart"); EVERTEC México Servicios de Procesamiento, S.A. de C.V.; Sinqia S.A.,Torq. Inovação Digital Ltda, Sinqia Tecnologia Ltda., Homie do Brasil Informática S.A., Rosk Software S.A., Lote 45 Participações S.A., and Compliasset S.A. (collectively "Sinqia"); Grandata, Inc., Grandata Mexico, S.A. de C.V., Grandata USA, Inc. and Big Data Analytics SA (collectively "Grandata"); and Nubity S.R.L., Nubity Inc., Nubity Cloud, S.A.P.I. de C.V. (collectively "Nubity") and Tecnobank Tecnologia Bancária S.A. ("Tecnobank"). Neither EVERTEC nor EVERTEC Intermediate Holdings, LLC conducts any operations other than with respect to its indirect or direct ownership of EVERTEC Group.

Company Overview

EVERTEC is a leading full-service transaction-processing business and financial technology provider in Latin America, Puerto Rico and the Caribbean, providing a broad range of merchant acquiring, payment services and business solutions. We believe we are one of the largest merchant acquirers in Latin America based on total number of transactions and we also believe we are the largest merchant acquirer in the Caribbean. We serve 26 countries out of 24 offices, including our headquarters in Puerto Rico. We own and operate the ATH network, which we believe is one of the leading debit networks in Latin America. We process over ten billion transactions annually through a system of electronic payment networks in Puerto Rico and Latin America and provide a comprehensive suite of services for core banking, cash processing, fulfillment in Puerto Rico and a "one stop shop" set of products for the financial sector in Latin America, which include solutions such as core banking, investments, asset management, pension funds and consortium. Additionally, we offer managed services, managed security services and payment transactions fraud monitoring to all the regions where we do business. We serve a diversified customer base of leading financial institutions, merchants, corporations, and government agencies with "mission-critical" technology solutions that enable them to issue, process and accept transactions securely. We believe our business is well-positioned to continue to expand across the fast-growing Latin America region.

We are differentiated, in part, by our diversified business model, which enables us to provide our varied customer base with a broad range of transaction-processing services from a single source across numerous channels and geographic markets. We believe this capability provides several competitive advantages that will enable us to continue to penetrate our existing customer base with complementary new services, gain new customers, develop new sales channels, and enter new markets. We believe these competitive advantages include:

• Our ability to provide competitive products;

• Our ability to provide in one package a range of services that traditionally had to be sourced from different vendors;

• Our ability to serve customers with disparate operations in several geographies with technology solutions that enable them to manage their business as one enterprise; and

• Our ability to capture and analyze data across the transaction-processing value chain and use that data to provide value-added services that are differentiated from those offered by pure-play vendors that serve only one portion of the transaction-processing value chain (such as only merchant acquiring or only payment services).

Our broad suite of services spans the entire payment processing value chain and includes a range of front-end customer-facing solutions such as the electronic capture and authorization of transactions at the point-of-sale for both card present transactions and card-not-present transactions, as well as back-end support services such as the clearing and settlement of transactions and account reconciliation for card issuers. These include: (i) merchant acquiring services, which enable point of sales ("POS") and e-commerce merchants to accept and process electronic methods of payment such as debit, credit, prepaid and electronic benefit transfer ("EBT") cards; (ii) payment processing services, which enable financial institutions and other issuers to manage, support and facilitate the processing for credit, debit, prepaid, automated teller machines ("ATM") and EBT card programs; and (iii) business process management solutions, which provide "mission-critical" technology solutions such as core bank processing, as well as IT outsourcing and cash management services to financial institutions, corporations and governments.

We provide these services through scalable, end-to-end technology platforms that we manage and operate in-house and that generate significant operating efficiencies that enable us to maximize profitability.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-02_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-02_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-02_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-04_2-02-results.md, 10-K_2026-03-02_item7_mdna.md, 10-K_2026-03-02_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
