# Triage pack — HPK · HighPeak Energy, Inc.

_Generated 2026-09-04 17:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** HPK · **Name:** HighPeak Energy, Inc.
- **CIK:** 0001792849
- **SIC:** 1381 — Drilling Oil & Gas Wells
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/HPK

**Fetcher warnings for this ticker:** 10-K 2026-03-11: heading split missed Item 1 - Business

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** HighPeak Energy, Inc.
- **CIK:** 1,792,849 · **SIC:** 1381 (Drilling Oil & Gas Wells) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

> **EARNINGS QUALITY FLAG — one-off items likely.**
> net income exceeds revenue; net income more than 3x operating income.
> Reported net income is not supported by the operating engine that is supposed to produce it (typical causes: gains on sale, legal settlements, deferred-tax valuation-allowance releases, bargain-purchase gains). Reconcile net income to operating income in the earnings release (section 7) before treating any earnings-based metric here as repeatable.

**Valuation**

| metric | value |
|---|---|
| price | 8.29 |
| mktcap | $1.0B |
| ev | $2.0B |
| ev_ebit | 13.1x |
| fcf | $511.6M |
| fcf_yield | 48.8% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 4.8% |
| net_debt | $922.6M |
| net_debt_ebit | 6.2x |
| cash | $146.3M |
| ltd | $1.1B |
| equity | $1.6B |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $863.4M |
| revenue_prior | $1.1B |
| rev_growth | -22.7% |
| rev_growth_note | n/a |
| eq_flag | net income exceeds revenue; net income more than 3x operating income |
| ebit | $150.0M |
| net_income | $19.0B |
| cfo | $511.6M |
| capex | n/a |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 0.3% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 126,452,804 |
| shares_py | 126,132,288 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -10.8% |
| r6m | 55.2% |
| off_52w_high | -0.4% |
| adv20 | $3.5M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.98 |
| r_ev_ebit | 0.66 |
| r_roic | 0.50 |
| r_rev_growth | 0.03 |
| r_buyback | 0.61 |
| score | 0.55 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q2I |
| shares_period | CY2026Q2I |
| shares_py_period | CY2025Q2I |
| capex_missing | True |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 192 |

**Screen rationale:** top-quartile FCF yield 48.8%; EARNINGS QUALITY: net income exceeds revenue; net income more than 3x operating income — one-off items likely


## 3. Share count trend

- Shares outstanding: **126,452,804** (CY2026Q2I) vs **126,132,288** prior year (CY2025Q2I)
- Change: **0.3%** — roughly flat
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-06-30** — Item 1.01 (Entry into a Material Definitive Agreement): On June 30, 2026, HighPeak Energy, Inc. (the "Company"), as borrower, Fifth Third Bank, National Association, as administrative agent, the guarantors party thereto and the lenders party thereto entered into that certain Fourth Amendment to Credit Agreement...
- **2026-05-06** — Item 1.01 (Entry into a Material Definitive Agreement): On May 6, 2026, HighPeak Energy, Inc., a Delaware corporation (the "Company"), entered into a Sales Agreement (the "Sales Agreement") with Roth Capital Partners, LLC, as lead agent (the "Lead Agent") and USCA Securities LLC ("USCA," and together with the Lead...

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 12 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 12 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-10_2-02-results.md)

_Extraction: started at the first release heading, 'Second Quarter 2026 Operational Update'; skipped 12 forward-looking-statement block(s); 8 block(s) of pre-heading matter dropped._

## EX-99.1 - EXHIBIT 99.1 (ex_1000791.htm)

Second Quarter 2026 Operational Update

HighPeak's sales volumes averaged 45.3 MBoe/d during the second quarter of 2026 consisting of approximately 64% crude oil and 83% liquids.

The Company averaged one (1) drilling rig and (1) one frac crew throughout the second quarter, drilled 8 gross (7.7 net) horizontal wells, completed 16 gross (16.0 net) horizontal wells and turned-in-line 8 gross (8.0 net) producing wells. On June 30, 2026, the Company had 21 gross (20.4 net) horizontal wells in progress, including 16 gross (15.6 net) horizontal wells in various stages of completion.

Second Quarter 2026 Financial Results

HighPeak reported net income of $82.3 million for the second quarter 2026, or $0.59 per diluted share, and EBITDAX (a non-GAAP financial measure defined and reconciled below) of $147.6 million, or $1.06 per diluted share.

Second quarter 2026 average realized prices were $98.82 per Bbl of crude oil, $24.14 per Bbl of NGL and negative $1.50 per Mcf of natural gas, resulting in an overall realized price of $66.11 per Boe, or 71% of the weighted average of NYMEX crude oil prices, excluding the effects of derivatives. Including the effects of derivatives, second quarter 2026 average realized prices were $76.59 per Bbl of crude oil, $24.14 per Bbl of NGL and negative $0.61 per Mcf of natural gas, resulting in an overall realized price of $52.82 per Boe. HighPeak's cash costs for the second quarter 2026 were $17.02 per Boe, including lease operating costs of $6.43 per Boe, expense workovers of $1.49 per Boe, gathering, processing and transportation expenses of $4.18 per Boe, production and ad valorem taxes of $3.22 per Boe and G&A expenses of $1.70 per Boe. As a result, the Company's unhedged EBITDAX per Boe was $49.09 per Boe.

HighPeak's total capital expenditures, excluding acquisitions, for the second quarter were $107.5 million.

Hedging

Crude oil. As of June 30, 2026 and factoring in derivative instruments entered into subsequent to quarter end, HighPeak had the following outstanding crude oil derivative instruments and the weighted average crude oil prices per barrel ("Bbl"):

Settlement Month | Settlement Year | Type of Contract | ​ | Bbls Per Day | ​ | Index | ​ | Swap Price per Bbl | ​ | ​ | Costless Collar Floor Price per Bbl | ​ | ​ | Costless Collar Ceiling Price per Bbl | ​
Crude Oil: | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​
Jul – Sep | 2026 | Costless Collar | ​ | ​ | 13,000 | ​ | WTI Cushing | ​ | — | ​ | ​ | 61.38 | ​ | ​ | 69.39 | ​
Jul – Sep | 2026 | Swap | ​ | ​ | 5,000 | ​ | WTI Cushing | ​ | 63.45 | ​ | ​ | — | ​ | ​ | — | ​
Jul – Sep | 2026 | Roll Swap | ​ | ​ | 26,011 | ​ | NYMEX WTI Roll | ​ | 4.30 | ​ | ​ | ​ | ​ | ​ | ​ | — | ​
Jul – Sep | 2026 | Basis Swap | ​ | ​ | 23,000 | ​ | Argus WTI Midland | ​ | 1.37 | ​ | ​ | — | ​ | ​ | — | ​
Oct – Dec | 2026 | Costless Collar | ​ | ​ | 10,800 | ​ | WTI Cushing | ​ | — | ​ | ​ | 61.67 | ​ | ​ | 68.52 | ​
Oct – Dec | 2026 | Swap | ​ | ​ | 5,000 | ​ | WTI Cushing | ​ | 63.45 | ​ | ​ | — | ​ | ​ | — | ​
Oct – Dec | 2026 | Roll Swap | ​ | ​ | 25,000 | ​ | NYMEX WTI Roll | ​ | 4.23 | ​ | ​ | — | ​ | ​ | — | ​
Oct – Dec | 2026 | Basis Swap | ​ | ​ | 23,000 | ​ | Argus WTI Midland | ​ | 1.37 | ​ | ​ | — | ​ | ​ | — | ​
Jan – Mar | 2027 | Costless Collar | ​ | ​ | 8,900 | ​ | WTI Cushing | ​ | — | ​ | ​ | 59.78 | ​ | ​ | 65.24 | ​
Jan – Mar | 2027 | Swap | ​ | ​ | 4,400 | ​ | WTI Cushing | ​ | 62.14 | ​ | ​ | — | ​ | ​ | — | ​
Jan – Mar | 2027 | Basis Swap | ​ | ​ | 10,000 | ​ | Argus WTI Midland | ​ | 1.00 | ​ | ​ | — | ​ | ​ | — | ​
Apr – Jun | 2027 | Costless Collar | ​ | ​ | 4,000 | ​ | WTI Cushing | ​ | — | ​ | ​ | 52.00 | ​ | ​ | 62.85 | ​
Apr – Jun | 2027 | Swap | ​ | ​ | 6,470 | ​ | WTI Cushing | ​ | 59.61 | ​ | ​ | — | ​ | ​ | — | ​
Apr – Jun | 2027 | Basis Swap | ​ | ​ | 10,000 | ​ | Argus WTI Midland | ​ | 1.00 | ​ | ​ | — | ​ | ​ | — | ​
Jul – Sep | 2027 | Swap | ​ | ​ | 8,950 | ​ | WTI Cushing | ​ | 61.46 | ​ | ​ | — | ​ | ​ | — | ​
Jul – Sep | 2027 | Basis Swap | ​ | ​ | 10,000 | ​ | Argus WTI Midland | ​ | 1.00 | ​ | ​ | — | ​ | ​ | — | ​
Oct – Dec | 2027 | Swap | ​ | ​ | 7,500 | ​ | WTI Cushing | ​ | 70.42 | ​ | ​ | — | ​ | ​ | — | ​
Oct – Dec | 2027 | Basis Swap | ​ | ​ | 10,000 | ​ | Argus WTI Midland | ​ | 1.00 | ​ | ​ | — | ​ | ​ | — | ​

The Company's crude oil derivative contracts detailed above are based on reported settlement prices on the New York Mercantile Exchange for West Texas Intermediate ("WTI Cushing") pricing, the NYMEX WTI Roll or the basis differential between WTI Cushing and Argus WTI Midland pricing which represents the premium to WTI Cushing.

Natural gas. As of June 30, 2026 and factoring in derivative instruments entered into subsequent to quarter end, the Company had the following outstanding natural gas derivative instruments and the weighted average natural gas prices payable per MMBtu.

Settlement Month | Settlement Year | Type of Contract | ​ | MMBtu Per Day | ​ | Index | ​ | Price per MMBtu | ​
Natural Gas: | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​
Jul – Sep | 2026 | Swap | ​ | ​ | 30,000 | ​ | HH | ​ | 4.300 | ​
Oct – Dec | 2026 | Swap | ​ | ​ | 30,000 | ​ | HH | ​ | 4.300 | ​
Oct – Dec | 2026 | Basis Swap | ​ | ​ | 25,000 | ​ | WAHA | ​ | (1.455
Jan – Mar | 2027 | Swap | ​ | ​ | 19,667 | ​ | HH | ​ | 4.300 | ​
Jan – Mar | 2027 | Basis Swap | ​ | ​ | 25,000 | ​ | WAHA | ​ | (1.487
Apr – Jun | 2027 | Basis Swap | ​ | ​ | 25,000 | ​ | WAHA | ​ | (1.487
Jul – Sep | 2027 | Basis Swap | ​ | ​ | 25,000 | ​ | WAHA | ​ | (1.487
Oct – Dec | 2027 | Basis Swap | ​ | ​ | 25,000 | ​ | WAHA | ​ | (1.487

The Company's natural gas derivative contracts detailed above are based on reported settlement prices on the New York Mercantile Exchange for Henry Hub ("HH") pricing and the basis differential between Henry Hub and the West Texas WAHA Hub pricing.

Conference Call

HighPeak will host a conference call and webcast on Tuesday, August 11, 2026, at 10:00 a.m. Central Time for investors and analysts to discuss its results for the second quarter of 2026. Conference call participants may register for the call here . Access to the live audio-only webcast and replay of the earnings release conference call may be found here . A live broadcast of the earnings conference call will also be available on the HighPeak Energy website at www.highpeakenergy.com under the "Investors" section of the website. A replay will also be available on the website following the call.

When available, a copy of the Company's earnings release, investor presentation and Quarterly Report on Form 10-Q may be found on its website at www.highpeakenergy.com .

About HighPeak Energy, Inc.

HighPeak Energy, Inc. is a publicly traded independent crude oil and natural gas company, headquartered in Fort Worth, Texas, focused on the acquisition, development, exploration and exploitation of unconventional crude oil and natural gas reserves in the Midland Basin in West Texas. For more information, please visit our website at www.highpeakenergy.com .

(in thousands, except per share data)

​ | ​ | Three Months Ended June 30, | ​ | ​ | Six Months Ended June 30, | ​
​ | ​ | 2026 | ​ | ​ | 2025 | ​ | ​ | 2026 | ​ | ​ | 2025 | ​
Operating revenues: | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​
Crude oil sales | ​ | 260,361 | ​ | ​ | 196,723 | ​ | ​ | 459,516 | ​ | ​ | 443,147 | ​
NGL and natural gas sales | ​ | ​ | 12,058 | ​ | ​ | ​ | 19,749 | ​ | ​ | ​ | 28,788 | ​ | ​ | ​ | 45,636 | ​
Total operating revenues | ​ | ​ | 272,419 | ​ | ​ | ​ | 216,472 | ​ | ​ | ​ | 488,304 | ​ | ​ | ​ | 488,783 | ​
Operating costs and expenses: | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​
Crude oil and natural gas production | ​ | ​ | 32,641 | ​ | ​ | ​ | 33,726 | ​ | ​ | ​ | 62,165 | ​ | ​ | ​ | 69,288 | ​
Gathering, processing and transportation | ​ | ​ | 17,234 | ​ | ​ | ​ | 16,072 | ​ | ​ | ​ | 34,967 | ​ | ​ | ​ | 30,935 | ​
Production and ad valorem taxes | ​ | ​ | 13,254 | ​ | ​ | ​ | 12,391 | ​ | ​ | ​ | 25,154 | ​ | ​ | ​ | 27,543 | ​
Exploration and abandonments | ​ | ​ | 4,444 | ​ | ​ | ​ | 1,109 | ​ | ​ | ​ | 5,186 | ​ | ​ | ​ | 1,373 | ​
Depletion, depreciation and amortization | ​ | ​ | 113,429 | ​ | ​ | ​ | 101,226 | ​ | ​ | ​ | 226,443 | ​ | ​ | ​ | 210,551 | ​
Accretion of discount | ​ | ​ | 302 | ​ | ​ | ​ | 256 | ​ | ​ | ​ | 597 | ​ | ​ | ​ | 500 | ​
General and administrative | ​ | ​ | 7,004 | ​ | ​ | ​ | 5,671 | ​ | ​ | ​ | 12,749 | ​ | ​ | ​ | 12,016 | ​
Stock-based compensation | ​ | ​ | 868 | ​ | ​ | ​ | 88 | ​ | ​ | ​ | 1,733 | ​ | ​ | ​ | 265 | ​
Total operating costs and expenses | ​ | ​ | 189,176 | ​ | ​ | ​ | 170,539 | ​ | ​ | ​ | 368,994 | ​ | ​ | ​ | 352,471 | ​
Other expense | ​ | ​ | 3,000 | ​ | ​ | ​ | 2,489 | ​ | ​ | ​ | 3,050 | ​ | ​ | ​ | 2,489 | ​
Income from operations | ​ | ​ | 80,243 | ​ | ​ | ​ | 43,444 | ​ | ​ | ​ | 116,260 | ​ | ​ | ​ | 133,823 | ​
Interest and other income | ​ | ​ | 1,032 | ​ | ​ | ​ | 361 | ​ | ​ | ​ | 1,981 | ​ | ​ | ​ | 1,171 | ​
Interest expense | ​ | ​ | (35,978 | ​ | ​ | (36,412 | ​ | ​ | (71,016 | ​ | ​ | (73,400
Gain (loss) on derivative instruments, net | ​ | ​ | 53,426 | ​ | ​ | ​ | 26,446 | ​ | ​ | ​ | (103,601 | ​ | ​ | 18,519 | ​
Income (loss) before income taxes | ​ | ​ | 98,723 | ​ | ​ | ​ | 33,839 | ​ | ​ | ​ | (56,376 | ​ | ​ | 80,113 | ​
Provision for income taxes | ​ | ​ | 16,448 | ​ | ​ | ​ | 7,663 | ​ | ​ | ​ | (11,203 | ​ | ​ | 17,602 | ​
Net income (loss) | ​ | 82,275 | ​ | ​ | 26,176 | ​ | ​ | (45,173 | ​ | 62,511 | ​
Earnings per share: | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​
Basic net income (loss) | ​ | 0.60 | ​ | ​ | 0.19 | ​ | ​ | (0.36 | ​ | 0.46 | ​
Diluted net income (loss) | ​ | 0.59 | ​ | ​ | 0.19 | ​ | ​ | (0.36 | ​ | 0.45 | ​
​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​
Weighted average shares outstanding: | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​
Basic | ​ | ​ | 125,286 | ​ | ​ | ​ | 123,930 | ​ | ​ | ​ | 125,276 | ​ | ​ | ​ | 123,922 | ​
Diluted | ​ | ​ | 126,409 | ​ | ​ | ​ | 126,095 | ​ | ​ | ​ | 125,276 | ​ | ​ | ​ | 126,169 | ​
​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​ | ​
Dividends declared per share | ​ | — | ​ | ​ | 0.04 | ​ | ​ | — | ​ | ​ | 0.08 | ​

HighPeak Energy, Inc.
Unaudited Condensed Consolidated Statements of Cash Flows
(in thousands)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-11_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

HighPeak Energy, Inc., a Delaware corporation, was formed in October 2019, is an independent crude oil and natural gas exploration and production company that explores for, develops and produces crude oil, NGL and natural gas in the Permian Basin in West Texas, more specifically, the Midland Basin. The Company's assets are located primarily in Howard and Borden Counties, Texas, and to a lesser extent Scurry and Mitchell Counties, which lie within the northeastern part of the crude oil-rich Midland Basin. As of December 31, 2025, the assets consisted of two highly contiguous leasehold positions of approximately 154,472 gross (142,560 net) acres, approximately 72% of which were held by production, with an average working interest of 92%. Our acreage is composed of two core areas, Flat Top primarily in the northern portion of Howard County extending into southern Borden County, southwest Scurry County and northwest Mitchell County and Signal Peak in the southern portion of Howard County. We operate approximately 98% of the net acreage across the Company's assets and more than 90% of the net operated acreage provides for horizontal wells with lateral lengths of 10,000 feet or greater. For the year ended December 31, 2025, approximately 85% and 15% of sales volumes from the assets were attributable to liquids (both crude oil and NGL) and natural gas, respectively. As of December 31, 2025, HighPeak Energy was developing its properties using two (2) drilling rigs and one (1) frac crew and expects to average one (1) drilling rig and one (1) frac crew during 2026 under our current development plan, depending on certain market conditions.

Recent Events

Recent management changes. In September 2025, Mr. Jack Hightower, the Company's Chief Executive Officer and Chairman of the Board retired and resigned from our Board of Directors, and on November 4, 2025, our President, Mr. Michael Hollis, was named President and Chief Executive Officer.

Concurrent with these changes, Mr. Jack Hightower also retired from managing HighPeak Energy Partners, LP and HighPeak Energy Partners II, LP (collectively, the "HighPeak Funds"), which collectively own approximately 64% of the shares of common stock of the Company. In connection with Mr. Jack Hightower's retirement, HighPeak Pure Acquisition, LLC ("Pure"), a wholly owned subsidiary of HighPeak Energy Partners, LP distributed 1,532,478 shares of common stock in full and complete redemption of Mr. Jack Hightower's interest in Pure. Following Mr. Jack Hightower's retirement, the HighPeak Funds are managed by a committee comprised of Mr. Hollis, Daniel Silver and William R. Hightower, each of whom also serve as President and Chief Executive Officer, Executive Vice President and Executive Vice President of the Company, respectively. In addition, pursuant to the Stockholder's Agreement, dated August 21, 2020, the HighPeak Funds have designated Mr. Silver to serve as their board appointee under the Stockholder's Agreement, and Mr. Silver was appointed to serve as a director of the Board effective immediately.

Debt amendments and actions taken to bolster covenant compliance. In August 2025, the Company entered into the First Term Loan Amendment and the Second Facility Amendment which amended the Term Loan Credit Agreement and the Senior Credit Facility Agreement whereby, among other things, (i) the maturity date was extended two years to September 2028, (ii) Term Loan Credit Agreement was upsized to $1.2 billion, providing additional liquidity, and (iii) the Term Loan Credit Agreement quarterly amortization payments of $30.0 million were deferred for one year such that they begin again in September 2026.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Results of operations should be read together with the Company's consolidated financial statements and related notes included in "Item 8. Financial Statements and Supplementary Data" of this Annual Report. See the Company's Annual Report on Form 10-K for the year ended December 31, 2024 filed with the SEC on March 10, 2025 for a discussion of the Company's 2024 results of operations compared with the Company's 2023 results of operations.

Sources of Revenues

The Company's revenues, which are entirely originated in the continental United States, are derived from the sale of crude oil and natural gas production and the sale of NGL that are extracted from natural gas during processing. For the years ended December 31, 2025, 2024 and 2023, revenues from our assets were derived approximately 91%, 95% and 96%, respectively, from crude oil sales and 9%, 5% and 4%, respectively, from NGL and natural gas sales.

The Company is subject to credit risk resulting from the concentration of its crude oil and natural gas receivables with significant purchasers. For the year ended December 31, 2025, sales to the Company's largest purchaser accounted for approximately 82% of the Company's total crude oil, NGL and natural gas sales revenues. The Company generally does not require collateral and does not believe the loss of this particular purchaser would materially impact its operating results, as crude oil and natural gas are fungible products with well-established markets and numerous purchasers in various regions.

The Company's revenues are presented net of certain gathering, transportation and processing expenses incurred to deliver production of its assets' crude oil, NGL and natural gas to the market. Cost levels of these expenses can vary based on the volume of crude oil, NGL and natural gas produced as well as the cost of commodity processing. Crude oil, NGL and natural gas prices are inherently volatile and are influenced by many factors outside the Company's control. To reduce the impact of fluctuations in crude oil, NGL and natural gas prices on revenues, the Company may periodically enter into derivative contracts with respect to a portion of its estimated crude oil, NGL and natural gas production through various transactions that fix or set a floor price for future prices received.

Principal Components of Cost Structure

Costs associated with producing crude oil, NGL and natural gas are substantial. Some of these costs vary with commodity prices, some trend with the type and volume of production, and others are a function of the number of wells owned. The sections below summarize the primary operating costs typically incurred:

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business

_Not available: the fetcher did not split out this section for this filing. Describe the business from the MD&A overview above instead, and say so in the note._

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | **MISSING** |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-11_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-11_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-10_2-02-results.md, 10-K_2026-03-11_item7_mdna.md

**Missing:** 10-K Item 1 - Business (business description), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
