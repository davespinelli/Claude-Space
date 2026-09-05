# Triage pack — KRNT · Kornit Digital Ltd.

_Generated 2026-09-05 00:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** KRNT · **Name:** Kornit Digital Ltd.
- **CIK:** 0001625791
- **SIC:** 3555 — Printing Trades Machinery & Equipment
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/KRNT

**Fetcher warnings for this ticker:** 10-K 2026-03-26: heading split missed Item 1 - Business, Item 1A - Risk Factors; no 10-Q in recent filings; no proxy (DEF 14A) in recent filings

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Kornit Digital Ltd.
- **CIK:** 1,625,791 · **SIC:** 3555 (Printing Trades Machinery & Equipment) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 16.05 |
| mktcap | $743.0M |
| ev | $707.5M |
| ev_ebit | n/a |
| fcf | $3.4M |
| fcf_yield | 0.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -4.0% |
| net_debt | -$35.5M |
| net_debt_ebit | n/a |
| cash | $35.5M |
| ltd | $0.00 |
| equity | $712.6M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $208.2M |
| revenue_prior | $203.8M |
| rev_growth | 2.1% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$34.6M |
| net_income | -$13.5M |
| cfo | $24.6M |
| capex | $21.3M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 0.5% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 46,290,822 |
| shares_py | 46,051,461 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 16.4% |
| r6m | 2.4% |
| off_52w_high | -11.0% |
| adv20 | $5.0M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.23 |
| r_ev_ebit | 0.00 |
| r_roic | 0.20 |
| r_rev_growth | 0.42 |
| r_buyback | 0.56 |
| score | 0.33 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2025Q4I |
| shares_period | CY2025Q4I |
| shares_py_period | CY2024Q4I |
| capex_missing | False |
| ltd_missing | True |

**Other screen columns**

| metric | value |
|---|---|
| rank | 379 |

**Screen rationale:** debt data missing (net cash unverified); 12-1 momentum 16.4%


## 3. Share count trend

- Shares outstanding: **46,290,822** (CY2025Q4I) vs **46,051,461** prior year (CY2024Q4I)
- Change: **0.5%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No 8-K filings fetched for this ticker._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 12,420 sh / $235,246 -> net $-235,246 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 4; transaction rows: 6 (open-market buys 0, sales 6).

| code | rows |
|---|---|
| S | 6 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release

_Not available: no 8-K with a readable release exhibit was fetched. Current-quarter results are unknown from this pack._

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-26_item7_mdna.md)

_Extraction: no Overview/Results heading found; took the start of Item 7._

ITEM
7. Major Shareholders and Related Party Transactions .

A.
Major Shareholders

The
following table sets forth information with respect to the beneficial ownership of our ordinary shares as of February 17, 2026 by:

● | each person or entity known by us to own beneficially 5% or more of our outstanding ordinary shares;

● | each of our directors and executive officers individually; and

● | all of our executive officers and directors as a group.

The
beneficial ownership of our ordinary shares is determined in accordance with the rules of the SEC and generally includes any ordinary
shares over which a person exercises sole or shared voting or investment power, or the right to receive the economic benefit of ownership.
For purposes of the table below, we deem ordinary shares issuable pursuant to options that are currently exercisable or exercisable within
60 days of February 17, 2026 to be outstanding and to be beneficially owned by the person holding the options for the purposes of computing
the percentage ownership of that person, but we do not treat them as outstanding for the purpose of computing the percentage ownership
of any other person. Except where otherwise indicated, we believe, based on information furnished to us by such owners, that the beneficial
owners of the ordinary shares listed below have sole investment and voting power with respect to such shares. The number of record holders
in the United States is not representative of the number of beneficial holders nor is it representative of where such beneficial holders
are resident since many of these ordinary shares were held by brokers or other nominees.

Unless
otherwise noted below, each shareholder's address is c/o Kornit Digital Ltd., 12 Ha'Amal Street, Rosh -Ha'Ayin 4809246,
Israel.

A
description of any material relationship that our principal shareholders have had with us or any of our predecessors or affiliates within
the past three years is included under "Certain Relationships and Related Party Transactions."

The
percentages set forth below are based on 46,340,477 ordinary shares outstanding (which excludes 5,626,182 Treasury shares) as of February
17, 2026.

Except
where otherwise indicated, we believe, based on information furnished to us by such owners, that the beneficial owners of the ordinary
shares listed below have sole investment and voting power with respect to such shares. All of our shareholders, including the shareholders
listed below, have the same voting rights attached to their ordinary shares. See "ITEM 10.B Articles of Association."

A
description of any material relationship that our major shareholders have had with us or any of our predecessors or affiliates within
the past year is included under "ITEM 7.B-Related Party Transactions."

Name | Number of Shares Beneficially Held | Percent
5% or Greater Shareholders
Disciplined Growth Investors, Inc. (1) | 3,034,591 | 6.5 | %
Granahan Investment Management LLC (2) | 2,569,663 | 5.5 | %
Morgan Stanley (3) | 3,945,982 | 8.5 | %
Artisan Partners Limited Partnership (4) | 2,647,804 | 5.7
BlackRock, Inc. (5) | 2,339,199 | 5.0
Senvest Management, LLC (6) | 4,141,355 | 8.9 | %
Chicago Capital LLC (7) | 2,476,363 | 5.3 | %
Directors and Executive Officers
Yuval Cohen | 21,853 | *
Naama Halevi Davidov | 11,383 | *
Ofer Ben-Zur | 11,383 | *
Assaf Zipori | 0 | *
Stephen Nigro | 20,395 | *
Dov Ofer | 17,553 | *
Gabi Seligsohn | 56,395 | *
Ronen Samuel | 298,205 | (8) | *
Daniel Gazit | 35,965 | (9) | *
Yaaqov Mann | 108,636 | (10) | *
All Directors and Executive Officers as a Group (10 persons) | 581,768 | * (11) | 1.3 | %

* | Represents beneficial ownership of less than 1% of our outstanding ordinary shares.

(1) | The address of this shareholder is 150 South Fifth Street, Suite 2550, Minneapolis, MN 55402. The information in this row is provided as of December 31, 2025, based on a statement of beneficial ownership on Schedule 13G filed by Disciplined Growth Investors, Inc. with the SEC on February 17, 2026.

(2) | The address of this shareholder is Wyman Street, Suite 460, Waltham, MA 02451. The information in this row is provided as of December 31, 2025, based on a statement of beneficial ownership on Schedule 13G filed by Granahan Investment Management LLC with the SEC on February 17, 2026. This shareholder possesses sole dispositive power with respect to all 2,569,663 shares, and sole voting power with respect to 1,970,645 of the shares, beneficially owned by it. The subject shares are owned by various investment advisory clients of Granahan Investment Management LLC, which is deemed to be a beneficial owner of those shares due to its discretionary power to make investment decisions and/or its ability to vote with respect to those shares.

(3) | The address of this shareholder is 1585 Broadway New York, NY 10036. The information in this row is provided as of December 31, 2025, based on Amendment No. 4 to a statement of beneficial ownership on Schedule 13G filed by Morgan Stanley with the SEC on February 12, 2026. Morgan Stanley possesses shared dispositive power with respect to all of these ordinary shares, and shared voting power with respect to 3,893,539 of these ordinary shares. The ordinary shares included in the beneficial ownership of this shareholder are beneficially owned, or may be deemed to be beneficially owned, by Morgan Stanley Capital Services LLC, a wholly-owned subsidiary of Morgan Stanley, and/or certain additional operating units of Morgan Stanley, its subsidiaries or affiliates whose ownership is included in Morgan Stanley's beneficial ownership report. These ordinary shares reported as beneficially owned do not include ordinary shares, if any, beneficially owned by any operating units of Morgan Stanley whose ownership of securities is disaggregated from that of certain operating units of Morgan Stanley, its subsidiaries and affiliates.
(4) | The address of this shareholder is 875 E. Wisconsin Ave., Suite 800, Milwaukee, WI 53202. The information in this row is provided as of December 31, 2025, based on a statement of beneficial ownership on Schedule 13G filed by Artisan Partners Limited Partnership with the SEC on February 3, 2026. The shares reported for this shareholder have been acquired on behalf of discretionary clients of Artisan Partners Limited Partnership, or APLP. Artisan Partners Holdings LP is the sole limited partner of APLP and the sole member of Artisan Investments GP LLC; Artisan Investments GP LLC is the general partner of APLP; Artisan Partners Asset Management Inc. is the general partner of Artisan Partners Holdings LP. APLP and its affiliated entities possess shared dispositive power with respect to all 2,647,804 of the subject shares and shared voting power with respect to 2,345,989 of such shares.
(5) | The address of this shareholder is 50 Hudson Yards, New York, NY 10001. The information in this row is provided as of September 30, 2025, based on a statement of beneficial ownership on Schedule 13G filed by BlackRock, Inc. with the SEC on October 17, 2025. BlackRock, Inc. reported sole voting power over 2,312,191 shares and sole dispositive power over 2,339,199 shares. The ordinary shares. included in the beneficial ownership of this shareholder are beneficially owned, or may be deemed to be beneficially owned, by certain business units of BlackRock, Inc. and its subsidiaries and affiliates. They do not include ordinary shares, if any, beneficially owned by other business units whose ownership of securities is disaggregated from that of the subject reporting business units.
(6) | The address of this shareholder is 540 Madison Avenue, 32 nd Floor, New York, New York 10022. The information in this row is provided as of December 31, 2025, based on a report of institutional investment manager on Form 13F filed by Senvest Management, LLC with the SEC on February 12, 2026. The ordinary shares reported in this row are held in the account of Senvest Master Fund, LP and Senvest Technology Partners Master Fund, LP, which are collectively referred to as the Senvest Investment Vehicles. Senvest Management, LLC may be deemed to beneficially own the securities held by the Senvest Investment Vehicles by virtue of Senvest Management, LLC's position as investment manager of the Senvest Investment Vehicles. Mr. Richard Mashaal may be deemed to beneficially own the securities held by the Senvest Investment Vehicles by virtue of Mr. Mashaal's status as the managing member of Senvest Management, LLC. None of the foregoing should be construed in and of itself as an admission by any of the foregoing persons or entities as to beneficial ownership of the subject ordinary shares.
(7) | The address of this shareholder is 135 South LaSalle Street, Suite 4200, Chicago, IL 60603. The information in this row is provided as of December 31, 2025, based on a report of institutional investment manager on Form 13F filed by Chicago Capital, LLC with the SEC on January 26, 2026.
(8) | Consists of (i) 101,494 ordinary shares, (ii) 147,191 ordinary shares issuable upon exercise of options that have vested or will vest within 60 days of February 17, 2026 (comprised of: 37,500 options at a $28.15 exercise price, with an expiration date of August 22, 2029; 10,350 options at a $57.79 exercise price, with an expiration date of August 12, 2030; 5,005 options at a $122.19 exercise price, with an expiration date of August 12, 2031; 20,803 options at a $35.51 exercise price, with an expiration date of August 11, 2032; 18,816 options at a $22.02 exercise price, with an expiration date of December 29, 2032; 30,328 options at a $23.00 exercise price, with an expiration date of August 12, 2033; and 24,389 options at a $16.48 exercise price, with an expiration date of August 12, 2034), and (iii) 49,520 shares underlying RSUs that have vested or will vest within 60 days of February 17, 2026.

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
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-26_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | **MISSING** |

**Present:** meta.json, form4_summary.md, 10-K_2026-03-26_item7_mdna.md

**Missing:** 8-K filings, 8-K earnings press release exhibit, 10-K Item 1 - Business (business description), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
