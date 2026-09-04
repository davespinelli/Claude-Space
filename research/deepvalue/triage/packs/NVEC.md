# Triage pack — NVEC · NVE CORP /NEW/

_Generated 2026-09-04 17:11 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** NVEC · **Name:** NVE CORP /NEW/
- **CIK:** 0000724910
- **SIC:** 3674 — Semiconductors & Related Devices
- **Fiscal year end (MM-DD):** 03-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/NVEC

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** NVE CORP /NEW/
- **CIK:** 724,910 · **SIC:** 3674 (Semiconductors & Related Devices) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 98.56 |
| mktcap | $476.8M |
| ev | $473.9M |
| ev_ebit | 29.8x |
| fcf | $14.5M |
| fcf_yield | 3.0% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 22.1% |
| net_debt | -$2.9M |
| net_debt_ebit | -0.2x |
| cash | $2.9M |
| ltd | $0.00 |
| equity | $59.8M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $26.3M |
| revenue_prior | $25.9M |
| rev_growth | 1.8% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $15.9M |
| net_income | $15.2M |
| cfo | $16.7M |
| capex | $2.2M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 0.0% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 4,837,166 |
| shares_py | 4,837,166 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 110.1% |
| r6m | 48.8% |
| off_52w_high | -25.9% |
| adv20 | $15.0M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.37 |
| r_ev_ebit | 0.29 |
| r_roic | 0.89 |
| r_rev_growth | 0.40 |
| r_buyback | 0.67 |
| score | 0.57 |

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
| rank | 175 |

**Screen rationale:** high ROIC 22.1%; debt data missing (net cash unverified); 12-1 momentum 110.1%


## 3. Share count trend

- Shares outstanding: **4,837,166** (CY2026Q2I) vs **4,837,166** prior year (CY2025Q2I)
- Change: **0.0%** — roughly flat
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-10** — Item 5.02 (officer / director change or comp arrangement): In accordance with the Company's CEO succession plan described in our Proxy Statement on Schedule 14A and Item 5.02 of our Current Report on Form 8-K, both filed on June 22, 2026, Daniel A. Baker retired as president and chief executive officer effective at...
- **2026-06-22** — Item 5.02 (officer / director change or comp arrangement): On June 22, 2026, NVE Corporation (the "Company") announced that Daniel A. Baker, Ph.D., age 68, will retire as President and Chief Executive Officer effective at the Company's Annual Shareholders' meeting on August 6, 2026.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 28,489 sh / $3,196,685 -> net $-3,196,685 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 11; transaction rows: 30 (open-market buys 0, sales 9).

| code | rows |
|---|---|
| A | 5 |
| D | 1 |
| M | 15 |
| S | 9 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-22_2-02-results.md)

_Extraction: started at the first release heading, 'NVE Corporation Reports First Quarter Results and Announces Quarterly '; skipped 5 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99.1 - PRESS RELEASE (nve_ex99z1.htm)

NVE Corporation Reports First Quarter Results and Announces Quarterly Dividend

Revenue increases 81% and net income increases 79%

EDEN PRAIRIE, Minn.—July 22, 2026—NVE Corporation (Nasdaq: NVEC) announced today financial results for the quarter ended June 30, 2026.

Total revenue for the first quarter of fiscal 2027 increased 81% to $11.0 million from $6.10 million for the prior-year quarter. The increase was due to an 82% increase in product sales and a 53% increase in contract research and development revenue. Net income for the first quarter of fiscal 2027 increased 79% to $6.39 million, or $1.32 per diluted share, compared to $3.58 million, or $0.74 per share, for the prior-year quarter.

The company also announced a quarterly cash dividend to shareholders of $1.00 per share of common stock, payable August 31, 2026 to shareholders of record as of August 3, 2026.

"We're pleased to report exceptional growth in revenue and earnings driven by new product sales and a strong semiconductor market," said NVE President and Chief Executive Officer Daniel A. Baker, Ph.D.

NVE is a leader in the practical commercialization of spintronics, a nanotechnology that relies on electron spin rather than electron charge to acquire, store, and transmit information. The company manufactures high-performance spintronic products including sensors and couplers that are used to acquire and transmit data.

(Unaudited) June 30, 2026 | March 31, 2026
ASSETS
Current assets
Cash and cash equivalents | 2,896,148 | 1,714,040
Marketable securities, short-term | 18,875,009 | 18,125,060
Accounts receivable, net of allowance for credit losses of $15,000 | 6,545,713 | 3,408,941
Inventories, net | 6,673,227 | 7,082,821
Prepaid expenses and other assets | 685,921 | 1,860,415
Total current assets | 35,676,018 | 32,191,277
Fixed assets
Machinery and equipment | 13,900,632 | 13,843,799
Leasehold improvements | 2,059,853 | 2,059,853
15,960,485 | 15,903,652
Less accumulated depreciation and amortization | 12,419,993 | 12,187,643
Net fixed assets | 3,540,492 | 3,716,009
Marketable securities, long-term | 22,137,350 | 23,678,452
Right-of-use asset – operating lease | 763,080 | 793,794
Total assets | 62,116,940 | 60,379,532
LIABILITIES AND SHAREHOLDERS' EQUITY
Current liabilities
Accounts payable | 265,953 | 278,599
Accrued payroll and other | 1,037,155 | 697,611
Operating lease | 201,008 | 165,116
Total current liabilities | 1,504,116 | 1,141,326
Deferred tax liabilities | 128,217 | 248,284
Long-term operating lease liability | 704,817 | 740,423
Total liabilities | 2,337,150 | 2,130,033
Shareholders' equity
Common stock | 48,372 | 48,372
Additional paid-in capital | 19,928,818 | 19,914,769
Accumulated other comprehensive income (loss) | (72,793 | (32,010
Retained earnings | 39,875,393 | 38,318,368
Total shareholders' equity | 59,779,790 | 58,249,499
Total liabilities and shareholders' equity | 62,116,940 | 60,379,532

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-05-06_item7_mdna.md)

_Extraction: started at the Overview heading._

Overview

Our liquidity and operating capital requirements are primarily for purchases of raw materials such as foundry wafers, purchases of packaging services, and the maintenance of work-in-process inventories.

Cash and cash equivalents were $1,714,040 as of March 31, 2026, compared to $8,036,564 as of March 31, 2025. The $6,322,524 decrease in cash and cash equivalents was due to $19,348,664 of cash used in financing activities and $3,631,857 of net cash used in investing activities, partially offset by $16,657,997 of cash provided by operating activities.

Operating Activities

Net cash provided by operating activities related to product sales and research and development contract revenue was our primary source of working capital for fiscal 2026 and 2025. Net cash provided by operating activities increased to $16,657,997 for fiscal 2026 compared to $14,310,418 for fiscal 2025.

Non-cash operating lease expenses decreased $107,863 primarily due to our receipt of a $100,000 leasehold improvement allowance.

Accounts receivable decreased $180,327 primarily due to the timing of customer payments.

Inventories decreased $366,262 primarily due to increased product sales and conversion of raw materials and work-in-process inventories to finished goods to support increased product demand.

Prepaid expenses and other assets increased $1,427,001 primarily due to increased accrued bond interest and overpayment of Federal estimated taxes for fiscal 2026.

Accrued payroll and other current liabilities decreased $173,557 primarily due to the payment of federal and state taxes balance due as of March 31, 2025 in the first quarter of fiscal 2026.

Investing Activities

Net cash used in investing activities for fiscal 2026 consisted of $15,242,719 of marketable securities purchases and $2,189,138 of fixed asset purchases, partially offset by $13,800,000 in proceeds from maturities of marketable securities. Fixed asset purchases were primarily of production equipment. We expect fixed asset purchases to decrease significantly in fiscal 2027 with the completion of our expansion.

Financing Activities

Net cash used in financing activities in fiscal 2026 consisted of $19,348,664 of cash dividends paid to shareholders.

In addition to cash dividends to shareholders paid in fiscal 2026, on May 6, 2026, we announced that our Board had declared a cash dividend of $1.00 per share of Common Stock, or $4,837,166 based on shares outstanding as of March 31, 2026, to be paid May 29, 2026. We plan to fund dividends through cash provided by operating activities and proceeds from maturities of marketable securities. All future dividends will be subject to Board approval and subject to the company's results of operations, cash and marketable security balances, estimates of future cash requirements, and other factors the Board may deem relevant. Furthermore, dividends may be modified or discontinued at any time without notice.

## 9. 10-K Item 1 - Business (10-K_2026-05-06_item1_business.md)

ITEM 1. BUSINESS.

In General

NVE Corporation, referred to as NVE, we, us, or our, develops and sells devices that use spintronics, a nanotechnology that relies on electron spin rather than electron charge to acquire, store, and transmit information. We manufacture high-performance spintronic products including sensors and couplers that are used to acquire and transmit data.

NVE History and Background

NVE is a Minnesota corporation headquartered in a suburb of Minneapolis. We were founded in 1989 by James M. Daughton, Ph.D., a spintronics pioneer. Our common stock became publicly traded in 2000 through a reverse merger and became NASDAQ listed in 2003. Since our founding, we have been awarded more than $50 million in government research contracts. These contracts have helped us develop products and build our intellectual property portfolio. We have adopted a March 31 fiscal year, so fiscal years referenced in this report end March 31.

Industry Background

Much of the electronics industry is devoted to the acquisition, storage, and transmission of information. We have focused on three applications for our spintronic technology: magnetic sensors, couplers, and memories. Sensors acquire information, couplers transmit information, and memories store information. In that sense, our technology can provide the eyes, nerves, and brains of electronic systems.

Magnetic sensors can be used for many purposes including detecting the position or speed of robotics and mechanisms, or for communicating with implantable medical devices. We believe our spintronic sensors are smaller, more precise, and more reliable than competing devices.

Couplers are widely used in factory automation, providing reliable digital communication between electronic subsystems in factories. For example, couplers are used to send high-speed data between robots and central controllers. As manufacturing automation expands, there is a need for higher-speed data and more channel density. Because of their unique properties, we believe our couplers transmit more data at higher speeds and over longer distances than conventional devices.

Near-term potential MRAM applications include mission-critical storage such as military, industrial, and antitamper applications. Long term, MRAM could address the market for ubiquitous high-density memory.

Our Enabling Technology

Our designs are generally based on either giant magnetoresistance or tunneling magnetoresistance. These structures produce a large change in electrical resistance depending on the electron spin orientation in a free layer.

In giant magnetoresistance (GMR) devices, resistance changes due to conduction electrons scattering at interfaces within the devices. The GMR effect is only significant if the layer thicknesses are less than the mean free path of conduction electrons, which is approximately five nanometers. Our critical GMR conductor layers may be less than two nanometers, or five atomic layers, thick.

A more advanced type of spintronic structure we use is based on tunneling magnetoresistance (TMR). Such devices are known as Spin-Dependent Tunnel (SDT) junctions or Magnetic Tunnel Junctions (MTJs). SDT junctions use tunnel barriers that are so thin that electrons can "tunnel" through a normally insulating material to cause a resistance change. SDT barrier thicknesses can be in the range of one to four nanometers (less than ten molecular layers).

In our products, the spintronic elements are connected to integrated circuitry and encapsulated ("packaged") in much the same way as conventional integrated circuits.

Our Strategy

Our vision is to become the leading developer of practical spintronics technology and devices. Our spintronic technology provides eyes, nerves, and brains for electronic systems, breathing life and intelligence into inanimate objects. Our unique products support global trends of efficient energy conversion and smart, low-power end nodes for the "Internet of Things." To grow product sales, we plan to broaden our sensor and coupler product lines and enhance our product benefits in target markets.

Our Products and Markets

Sensor Products and Markets

Our sensor products detect the strength or gradient of magnetic fields and are often used to determine position or speed. GMR or TMR elements change electrical resistance depending on the magnetic field. In many of our devices, sensor elements are combined with foundry integrated circuitry or digital cores, and packaged in much the same way as conventional integrated circuits. Our sensors are small, highly sensitive to magnetic fields, precise, and reliable. We sell standard ("catalog") sensors, and custom sensors designed to meet customers' exact requirements.

Standard sensors

Our standard, or catalog sensors are generally used to detect the presence of a magnetic or metallic material to determine position, rotation, or speed. We believe our spintronic sensors are smaller, more precise, more reliable, and lower power than competing devices. Our major markets for standard sensors are the Industrial Internet of Things (IIoT) and the Artificial Intelligence of Things (AIoT) for factory automation.

Custom and medical sensors

Our primary custom products are sensors for medical devices, which are customized to our customers' requirements and manufactured under stringent medical device quality standards. Many are used to replace electromechanical magnetic switches. We believe our sensors have important advantages in medical devices compared to electromechanical switches, including no moving parts for inherent reliability, and being smaller, more sensitive, and more precise. Our sensors can be customized for size, range, and sensitivity to magnetic fields, electrical resistance, and embedded software.

Coupler Products and Markets

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-05-06_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-05-06_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-05-06_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-07-22_2-02-results.md, 10-K_2026-05-06_item7_mdna.md, 10-K_2026-05-06_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
