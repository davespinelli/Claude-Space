# Triage pack — ACDC · ProFrac Holding Corp.

_Generated 2026-09-05 03:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** ACDC · **Name:** ProFrac Holding Corp.
- **CIK:** 0001881487
- **SIC:** 1389 — Oil & Gas Field Services, NEC
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/ACDC

**Fetcher warnings for this ticker:** 10-K 2026-03-13: heading split missed Item 1 - Business; 10-Q 2026-08-06: MD&A heading not detected, wrote truncated full text

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** ProFrac Holding Corp.
- **CIK:** 1,881,487 · **SIC:** 1389 (Oil & Gas Field Services, NEC) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 5.12 |
| mktcap | $932.5M |
| ev | $1.8B |
| ev_ebit | n/a |
| fcf | $19.6M |
| fcf_yield | 2.1% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -12.4% |
| net_debt | $899.4M |
| net_debt_ebit | n/a |
| cash | $18.8M |
| ltd | $918.2M |
| equity | $542.5M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $1.9B |
| revenue_prior | $2.2B |
| rev_growth | -11.4% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$225.8M |
| net_income | -$355.5M |
| cfo | $189.5M |
| capex | $169.9M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 13.6% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 182,122,762 |
| shares_py | 160,280,185 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 18.2% |
| r6m | -3.6% |
| off_52w_high | -36.5% |
| adv20 | $8.4M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.31 |
| r_ev_ebit | 0.00 |
| r_roic | 0.10 |
| r_rev_growth | 0.09 |
| r_buyback | 0.10 |
| score | 0.17 |

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
| rank | 472 |

**Screen rationale:** 12-1 momentum 18.2%


## 3. Share count trend

- Shares outstanding: **182,122,762** (CY2026Q2I) vs **160,280,185** prior year (CY2025Q2I)
- Change: **13.6%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-06** — Item 5.02 (officer / director change or comp arrangement): Johnathan L. Wilks ") notified the Company that he would resign as Chief Executive Officer of the Company, and from each other
- **2026-07-06** — Item 1.01 (Entry into Material Definitive Agreements): limited liability company (the " Borrower ") and an indirect subsidiary of ProFrac Holding Corp. (the " Company "),
- **2026-07-06** — Item 1.02 (Termination of a Material Definitive Agreement): outstanding obligations under, and terminated, that certain Credit Agreement, dated as of March 4, 2022, by and among the Borrower, Holdings,
- **2026-04-13** — Item 5.02 (Departure of Directors or Certain): Officers; Election of Directors; Appointment of Certain Officers; Compensatory Arrangements of Certain Officers.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 2,014,454 sh / $9,753,790 vs sells 0 sh / $0 -> net $9,753,790 (BUYING).
Distinct insiders buying (code P): 4. Largest buy: Wilks Dan H. / THRC Holdings, LP / THRC Management, LLC bought 517,669 sh @ $4.86 ($2,515,354) on 2026-08-10.

Form 4 filings parsed: 12; transaction rows: 18 (open-market buys 10, sales 0).

| code | rows |
|---|---|
| A | 5 |
| D | 1 |
| J | 2 |
| P | 10 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'Second Quarter 2026 Results'; skipped 9 forward-looking-statement block(s); 7 block(s) of pre-heading matter dropped._

## EX-99.1 - EXHIBIT 99.1 (tm2622356d1_ex99-1.htm)

Second Quarter 2026 Results

· | Total revenue was $498 million compared to first quarter revenue of $450 million

· | Net loss was $75 million compared to net loss of $81 million in the first quarter

· | Adjusted EBITDA¹ was $69 million compared to $54 million in the first quarter; 14% of revenue in the second quarter compared to 12% of revenue in the first quarter

· | Net cash provided by operating activities was $23 million compared to $9 million in the first quarter

· | Capital expenditures totaled $32 million compared to $41 million in the first quarter

· | Free cash flow² was negative $8 million compared to negative $25 million in the first quarter

"Our second quarter results extended the momentum we built during
the first quarter, reflecting the continued strength of our operating model and the discipline we've applied throughout this cycle against
a market backdrop that was broadly stronger sequentially. Volatility has defined the broader energy landscape in recent months, and if
anything, we believe that only reinforces the structural case for domestic energy security as a durable tailwind for our business. At
the same time, it's a reminder of why flexibility matters across every facet of our business," stated Executive Chairman, Matt Wilks.

"We believe we are well positioned for the future, given the
tighter market backdrop and growing operator demand for higher-specification equipment after years of attrition in the industry. We're
seeing pricing increases layering in for the third quarter in hydraulic fracturing, and we're taking a thoughtful, disciplined approach
in the back half of the year and into RFP season, which is commencing very early this year. High-spec fleets are in high demand and the
market for that equipment continues to tighten. We believe these factors will drive improvement in our frac calendar in the back half
of 2026."

"We remain committed to our cost optimization program, and our
continued investment in differentiated technology strengthens the value we deliver to customers and supports our returns through the cycle.
To that end, we continue to execute on our fleet upgrade program to allow us to lean further into the momentum we see building in the
industry. We believe the investments we're making today position us well through the balance of the year and beyond," concluded
Mr. Wilks.

Outlook

In Stimulation Services , ProFrac
expects third quarter 2026 results to improve on second quarter performance, driven by pricing increases and steady utilization. RFP season
conversations are also unfolding earlier than typical demonstrating potential equipment tightness into 2027.

In Proppant Production , ProFrac
expects approximately flat results on stable volumes in the third quarter. The Company continues to navigate incremental competitive pricing
pressure in the proppant market, particularly in West Texas, while remaining focused on operational improvements and leveraging the potential
it sees in stronger markets, including the Haynesville and South Texas.

Business Segment Information

The Stimulation Services segment
generated revenues of $430 million in the second quarter, which resulted in $39 million of Adjusted EBITDA and a margin of 9%.

The Proppant Production segment
generated revenues of $121 million in the second quarter, which resulted in $6 million of Adjusted EBITDA and a margin of 5%. Approximately
87% of the Proppant Production segment's second quarter 2026 revenue was intercompany.

The Manufacturing segment generated
revenues of $48 million in the second quarter, which resulted in $6 million of Adjusted EBITDA and a margin of 13%. Approximately 82%
of the Manufacturing segment's second quarter 2026 revenue was intercompany.

Flotek Industries, Inc. ("Flotek")
generated revenues of $102 million in the second quarter, which resulted in $19 million of Adjusted EBITDA and a margin of 19%. Approximately
58% of Flotek's second quarter 2026 revenue was intercompany.

Other Business Activities generated
revenues of $3.6 million in the second quarter, which resulted in $0.4 million of Adjusted EBITDA and a margin of 11%.

Capital Expenditures and Capital Allocation

Cash capital expenditures totaled $32 million
in the second quarter, down from $41 million reported in first quarter 2026.

For full year 2026, ProFrac maintains its expectation
that capital expenditures will be in the range of $155 million to $185 million, which includes Flotek's current capital expenditure
plan. Excluding Flotek, the Company expects capital expenditures to be in a range of $145 million to $175 million for 2026.

Balance Sheet and Liquidity

Total principal debt outstanding as of June 30,
2026 was approximately $1.10 billion; net debt³ outstanding was approximately $1.08 billion.

Total cash and cash equivalents as of June 30,
2026 was approximately $19 million, of which approximately $5 million was related to Flotek and not accessible by the Company.

As of June 30, 2026 the Company had approximately
$72 million of liquidity, including approximately $14 million of cash and cash equivalents, excluding Flotek, and $58 million of availability
under its asset-based credit facility.

Subsequent to quarter-end, on July 1, 2026, the
Company refinanced and replaced its existing $275 million asset-based revolving credit facility with a new $300 million asset-based revolving
credit facility that extends its debt maturity profile and provides enhanced borrowing base terms to support additional liquidity and
financial flexibility.

As of July 1, 2026, the maximum availability under
the new ABL credit facility was limited to our eligible borrowing base of approximately $243 million, with $173 million of borrowings
outstanding, resulting in approximately $71 million of remaining availability.

Management and Board Transitions

Effective Friday, August 7, 2026, Ladd Wilks will
resign his position of Chief Executive Officer of ProFrac. We are excited to announce that Ladd will continue to serve the Company as
a member of the Board of Directors, replacing Mr. Sergei Krylov. Matt Wilks will take on the newly combined role of Chief Executive Officer
and Executive Chairman.

"I am honored to transition from my role
as the Chief Executive Officer of ProFrac to a member of the Board of Directors. I look forward to continuing as an active leader of the
Company in this new capacity. ProFrac isn't just a company to me, it's part of our family's legacy, and I remain committed
to supporting its lasting success. I also thank Mr. Krylov for his years of dedication and service to ProFrac and for the thoughtful and
diligent stewardship he has brought to ProFrac's board throughout his tenure," stated Ladd Wilks.

Footnotes

(1) Adjusted EBITDA is a financial measure not
presented in accordance with generally accepted accounting principles ("GAAP") (a "Non-GAAP Financial Measure").
Please see "Non-GAAP Financial Measures" at the end of this news release.

(2) Free Cash Flow is a Non-GAAP Financial Measure.
Please see "Non-GAAP Financial Measures" at the end of this news release.

(3) Net Debt is a Non-GAAP Financial Measure.
Please see "Non-GAAP Financial Measures" at the end of this news release.

Conference Call

ProFrac has scheduled a conference call on August
6, 2026, at 11:00 a.m. Eastern / 10:00 a.m. Central. To register for and access the event, please click here . An archive of the
webcast will be available shortly after the call's conclusion on the IR Calendar section of ProFrac's investor relations
website for 90 days.

About ProFrac Holding Corp.

ProFrac Holding Corp. is a technology-focused,
vertically integrated, innovation-driven energy services holding company providing hydraulic fracturing, proppant production, other completion
services and other complementary products and services including distributed power generation to leading upstream oil and natural gas
companies engaged in the exploration and production ("E&P") of North American unconventional oil and natural gas resources
throughout the United States. ProFrac operates in four business segments: Stimulation Services, Proppant Production, Manufacturing, and
Flotek. For more information, please visit ProFrac's website at www.PFHoldingsCorp.com .

The presentation of Non-GAAP Financial Measures
is not intended to be a substitute for, and should not be considered in isolation from, the financial measures reported in accordance
with GAAP. The following tables present a reconciliation of the Non-GAAP Financial Measures of Adjusted EBITDA, Free Cash Flow and Net
Debt to the most directly comparable GAAP financial measure for the periods indicated.

- Tables to Follow –

ProFrac Holding
Corp.

Austin Harbour – Chief Financial Officer

Michael Messina – SVP of Finance

investors@pfholdingscorp.com

ICR, Inc.

PFHoldingsIR@icrinc.com

Source: ProFrac Holding Corp.

ProFrac Holding Corp. (NasdaqGS: ACDC)
Consolidated Balance Sheets

June 30, | December 31,
(In millions) | 2026 | 2025
ASSETS
Current assets:
Cash and cash equivalents | 18.8 | 22.9
Accounts receivable, net | 334.0 | 266.8
Accounts receivable — related party, net | 5.7 | 19.9
Inventories | 174.8 | 151.3
Prepaid expenses and other current assets | 38.8 | 22.6
Total current assets | 572.1 | 483.5
Property, plant, and equipment, net | 1,350.8 | 1,464.3
Operating lease right-of-use assets, net | 128.2 | 154.3
Goodwill | 290.2 | 290.2
Intangible assets, net | 93.8 | 111.8
Deferred tax assets | 24.4 | 29.0
Other assets | 48.4 | 40.0
Total assets | 2,507.9 | 2,573.1
LIABILITIES, MEZZANINE EQUITY, AND STOCKHOLDERS' EQUITY
Current liabilities:
Accounts payable | 323.7 | 257.1
Accounts payable — related party | 50.1 | 42.2
Accrued expenses | 67.4 | 74.0
Current portion of long-term debt | 159.9 | 144.7
Current portion of long-term debt — related party | 5.4 | 5.0
Current portion of operating lease liabilities | 41.4 | 44.8
Other current liabilities | 28.8 | 28.8
Other current liabilities — related party | 0.4 | 0.8
Total current liabilities | 677.1 | 597.4
Long-term debt | 877.7 | 832.7
Long-term debt — related party | 40.5 | 42.9
Operating lease liabilities | 92.6 | 115.5
Deferred tax liabilities | 11.8 | 11.8
Tax receivable agreement liability | 82.0 | 82.0
Other liabilities | 9.1 | 10.1
Total liabilities | 1,790.8 | 1,692.4
Mezzanine equity:
Series A preferred stock | 71.5 | 68.8
Stockholders' equity:
Class A common stock | 1.8 | 1.8
Additional paid-in capital | 1,316.8 | 1,325.9
Accumulated deficit | (776.1 | (610.2
Total stockholders' equity attributable to ProFrac Holding Corp. | 542.5 | 717.5
Noncontrolling interests | 103.1 | 94.4
Total stockholders' equity | 645.6 | 811.9
Total liabilities, mezzanine equity, and stockholders' equity | 2,507.9 | 2,573.1

ProFrac Holding Corp. (NasdaqGS: ACDC)
Consolidated Statements of Operations

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-13_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

Overview

We are a vertically integrated and innovation-driven energy services holding company providing hydraulic fracturing, proppant production, other completion services and other complementary products and services to leading upstream oil and natural gas companies engaged in the exploration and production ("E&P") of North American unconventional oil and natural gas resources.

We operate in four reportable business segments: Stimulation Services, Proppant Production, Manufacturing and Flotek. Our Stimulation Services segment, which primarily relates to ProFrac LLC, owns and operates a fleet of mobile hydraulic fracturing units and other auxiliary equipment that generates revenue by providing stimulation services to our customers. Our Proppant Production segment, which primarily relates to Alpine, provides proppant to oilfield service providers and E&P companies. Our Manufacturing segment sells products such as high horsepower pumps, valves, piping, swivels, large-bore manifold systems, and fluid ends. Flotek is a leading chemistry and data technology company focused on servicing the E&P industry.

Summary Financial Results

•
Total revenue for 2025 was $1,941.8 million compared to $2,190.9 million in 2024.

•
Net loss for 2025 was $355.5 million compared to net loss of $207.8 million in 2024.

•
Cash provided by operating activities for 2025 was $189.5 million compared to $367.3 million in 2024.

•
Total principal amount of long-term debt was $1,048.1 million at December 31, 2025 compared to $1,138.9 million at December 31, 2024.

2025 Developments

In April 2025, Flotek acquired certain gas conditioning equipment from our Stimulation Services segment for total consideration of $107.5 million and our Stimulation Services segment leased these assets back from Flotek for a six year term. We believe this Flotek partnership provides ownership exposure to a highly-scalable gas quality and asset integrity business. The effects of this sale-leaseback transaction have been eliminated from our consolidated financial statements. Part of the $107.5 million consideration was a $40.0 million intercompany note payable from Flotek to our Stimulation Services segment ("Flotek PWRtek Note"). In November 2025, the Stimulation Services segment agreed to assign this note receivable to PC Energy Credit I, LLC, a related party to the Company controlled by the Wilks Parties, in exchange for cash consideration of $40.4 million, which represented the sum of the unpaid principal amount of the note and all accrued and unpaid interest on the note through the closing date.

In June and December 2025 ProFrac Holdings II, LLC issued a total $60 million aggregate principal amount of its 2029 Senior Notes at par to Beal Bank USA and Wilks Brothers, LLC, which is a Wilks Party, in a private placement to fund capital expenditures with any remaining proceeds used for general corporate purposes.

In June 2025, we amended the Alpine 2023 Term Loan. Under the terms of the amendment, the amortization payments required to be made on June 30, 2025, September 30, 2025 and December 31, 2025 were reduced from $15.0 million to $5.0 million and we will pay an exit fee of $3.4 million when the term loan is repaid. In December 2025, we amended the Alpine 2023 Term Loan. Under the terms of the amendment, the amortization payments required to be made on March 31, 2026 and June 30, 2026 were reduced from $15.0 million to $7.5 million. Additionally, the Alpine 2023 Term Loan contained a covenant commencing with the fiscal quarter ending March 31, 2026, requiring Alpine not to exceed a maximum Total Net Leverage Ratio (as defined in the Alpine Term Loan Credit Agreement) of 2.00 to 1.00. This covenant was amended to commence testing compliance with the Total Net Leverage Ratio with the fiscal quarter ending on March 31, 2028.

In June 2025, we disposed of our EKU Power Drives subsidiary in our Manufacturing Segment. We recorded a loss of $10.5 million in connection with this disposal.

In August 2025, we issued 20.6 million shares of Class A common stock, par value $0.01 per share at an offering price of $4.00 per share. The issuance of these shares generated net proceeds of $79.0 million, after deducting underwriter discounts and commissions and offering costs. The Wilks Parties bought 5.0 million shares of these Class A common stock, generating $20.0 million of gross proceeds. We used the net proceeds from this offering to repay borrowings outstanding under our 2022 ABL Credit Facility, for working capital and for other general corporate purposes.

2024 Developments

In April 2024, we acquired all of the remaining equity interests of Basin Production and Completion LLC ("BPC"). BPC is the parent company of FHE USA LLC, which manufactures equipment used in the hydraulic fracturing industry. The total purchase consideration was $39.8 million, consisting of cash consideration of $14.9 million and our pre-existing investment of $24.9 million.

In June 2024, we acquired 100% of the issued and outstanding capital stock of Advanced Stimulation Technologies, Inc. ("AST"), a pressure pumping services provider serving the Permian Basin, for total purchase consideration of $173.4 million in cash.

In June 2024, we acquired 100% of the issued and outstanding common stock of NRG Manufacturing, Inc., which manufactures equipment used in the hydraulic fracturing industry, and its affiliate, AMI US Holdings, Inc., which develops commercial software used in hydraulic fracturing industry (collectively, "NRG"), for total purchase consideration of $6.0 million in cash.

In May 2024, the Company formed a new entity, Livewire Power, LLC ("Livewire"), which began operations in October 2024. Livewire enables onsite power generation services for oilfield and non-oilfield customers that require off-grid power solutions. Livewire's power generation equipment is comprised of owned and leased natural gas reciprocating engines and turbine assets. Livewire's results of operations were immaterial for 2024.

In December 2024, we sold certain stimulation service equipment to the Wilks Parties in exchange for cash consideration of approximately $40.0 million. We now lease such equipment from the Wilks Parties in exchange for aggregate monthly lease payments totaling $44.8 million through December 2028. The cash consideration received was $26.5 million more than the carrying value of these assets. Because this sale was to an affiliate under common control, we accounted for the $26.5 million as an equity transaction recorded as a deemed contribution within our consolidated statements of changes in equity.

Recent Trends and Outlook

Our business depends on the willingness of E&P companies to make expenditures to explore for, develop, and produce oil and natural gas in the United States. The willingness of E&P companies to undertake these activities is predominantly influenced by current and expected future prices for oil and natural gas. Beginning in April 2025, oil commodity prices decreased from their near-term average through the first quarter of 2025 with increased volatility. As a result, many of our customers began reducing their activity levels and our results of operations and operating cash flows correspondingly declined compared to 2024. As described below, we have taken a number of actions to improve our liquidity. Also, as we anticipated, our results of operations in the fourth quarter 2025 increased relative to the third quarter 2025 with improved demand in Stimulation Services and Proppant Production. Although adverse weather impacted our results early in the first quarter of 2026, activity has recently increased into February and early March on a relative basis. . In the second half of 2025, we implemented initiatives to enhance the resiliency of the platform resulting in lower cash operating expenses and capital expenditures. We remain focused on financial and operational discipline and optimizing our asset base. While we have limited visibility for future demand for our products and services and continue to focus on liquidity management, we are encouraged by recent customer engagement.

We also actively monitor the effects of inflation and tariffs on our business; however, the potential effects of inflation and tariffs on our business remain uncertain at this time.

Results of Operations

Revenues

The following table summarizes revenues by reportable segment:

Year Ended December 31,
2025 | 2024
Revenues
Stimulation services | 1,682.9 | 1,914.4
Proppant production | 336.0 | 246.5
Manufacturing | 212.3 | 222.8
Flotek | 243.6 | 192.4
Other | 17.3 | 3.1
Eliminations | (550.3 | (388.3
Total revenues | 1,941.8 | 2,190.9

Stimulation Services revenues in 2025 decreased $231.5 million, or 12%, from 2024. The decrease was primarily due to a decrease in average active fleets and lower average pricing for our services in 2025.

Proppant Production revenues in 2025 increased $89.5 million, or 36%, from 2024. The increase was primarily due to higher average pricing for our proppant in 2025, which was due to a shift in intercompany sales mix from mine-gate pricing to wellsite pricing that began in the second quarter of 2025. Exclusive of this mix shift, revenues also increased due to higher sales volumes in 2025. Revenue recognized for the amortization of acquired off-market contracts was $7.6 million and $43.7 million in 2025 and 2024, respectively. Intersegment revenues for the Proppant Production segment were 64% and 26% in 2025 and 2024, respectively.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business

_Not available: the fetcher did not split out this section for this filing. Describe the business from the MD&A overview above instead, and say so in the note._

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | **MISSING** |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-13_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-13_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-03-13_item7_mdna.md

**Missing:** 10-K Item 1 - Business (business description), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
