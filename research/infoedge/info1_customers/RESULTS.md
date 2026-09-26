# INFO-1. Hidden customer links: does a big customer's stock move predict its small supplier's next month?

*Generated 2026-09-26 by `research/infoedge/info1_customers/run_test.py` and `write_results.py`. Pre-registration and deviations: `PREREG.md` in this folder. Holding months 2010-02 .. 2026-08. Every number below is in `results.json` or `data/links_log.json`.*

## The short answer

**No.** Suppliers whose named big customers rose most in a month did better the next month than suppliers whose customers fell most, by +2.0 points a year after costs (Newey-West t = 0.57; the bar is 2.5 with the same sign in both halves). First half +6.4 points, second half -2.5 points.

| Test | Top fifth minus bottom fifth, a year (after 0.5%/yr) | NW(6) t | First half | Second half | Years top ahead | Months |
|---|---|---|---|---|---|---|
| **Primary: all suppliers, equal-weighted, size-and-industry adjusted** | +2.0 points | 0.57 | +6.4 points | -2.5 points | 9 of 17 | 198 |
| Secondary: suppliers under $2B | +1.9 points | 0.30 | +6.1 points | -2.4 points | 8 of 17 | 196 |
| Secondary: value-weighted | -1.4 points | -0.29 | +1.8 points | -4.5 points | 6 of 17 | 197 |
| Secondary: links with customer share >= 20% | +0.7 points | 0.11 | +4.4 points | -2.9 points | 7 of 17 | 197 |
| Information: suppliers $2B and over | +2.3 points | 0.64 | +2.7 points | +2.0 points | 9 of 17 | 190 |
| Information: raw returns (no benchmark) | +2.1 points | 0.57 | +5.8 points | -1.6 points | 7 of 17 | 198 |

"Points a year" is the average monthly spread times 12, after 0.5% a year of costs. Halves split the holding months in two equal parts (second half starts 2018-06-01).

**For picking stocks.** Do not buy a small supplier because its big customer's stock just had a good month, or sell it after a bad one. The customer links in 10-K text are real and can be extracted accurately, but since 2010 the supplier's next month has not reliably followed: the gap was positive before mid-2018 and slightly negative after, and it is no stronger in small caps or for the biggest customer shares.

## What was tested

Cohen and Frazzini found that when a company's big customers have a good month, its own stock tends to follow the next month, because investors are slow to connect the two. The pre-registered test: each month-end, take every supplier whose latest 10-K names at least one listed company as a customer with 10% or more of its revenue, compute the average return of those customers that month, sort suppliers into fifths by it, and hold the top fifth minus the bottom fifth for the next month. Supplier returns are measured against a size-and-industry benchmark.

## The link data

- **Documents.** Full-text search found 53,460 10-K documents (2010 to September 2026) with customer-concentration language. A phrase-template search for the alias-list companies returned the documents that name them; 19,664 documents were fetched and parsed.
- **Links.** 7,110 supplier-customer links (a 10-K naming a listed alias-list customer at 10% or more of revenue) in 5,390 10-K filings by 1,193 suppliers.
- **Most named customers:** WMT 983, AMZN 187, HD 175, T 157, F 150, VZ 141, GM 141, AAPL 141, TGT 133, SHEL 130, MCK 129, BA 124, CAH 122, AVT 117, XOM 100.
- **Extraction precision (hand check of 50 random links):** 48 of 50 fully right (96%): the named company really is a customer in 49 and the share is the latest year's share of total revenue, at 10% or more, in 48. A first sample, drawn before the prior-year rule was tightened, scored 40 of 50 (all 50 real customers, but 8 shares quoted for the prior year only); see PREREG.md Deviation 15. Details in `data/precision_labels.csv` and `data/precision_labels_round1.csv`.
- **Search recall (random discovery sample):** of 141 sampled 10-Ks in which the parser found a link, 128 (91%) were also found by the template search that feeds every other year.
- **Used in the test:** 492 suppliers were ranked at least once; 3,563 filing-customer links fed a ranking; 32,293 supplier-months; a median of 165 suppliers a month (min 31, max 185); 245 distinct customer stocks.

## Read this first: the missing-company problem

Yahoo has no prices for most companies that were later acquired or delisted, so 46.5% of supplier-months with a customer signal have no supplier price and cannot be held; 626 of the 1,118 suppliers with a signal were never priced (listed in `data/excluded_suppliers_no_price.csv`). The gap is spread evenly across the fifths (see below), and assuming every missing supplier lost 30% a year gives +1.0 points a year (t = 0.43); assuming +15% gives +0.9 points (t = 0.42). On the customer side, links to customers with no Yahoo history (Ingram Micro 2010-2016, Sprint, Dell 2013-2016, Tech Data, Walgreens, Raytheon Co. and Express Scripts before their mergers, and others) cannot produce a signal: 7,796 of 84,972 supplier-customer-months were lost that way.

## Primary test in detail

Average return against the size-and-industry benchmark, by fifth of the customer-return signal (before costs, average monthly x 12):

| Q1 (customers fell most) | Q2 | Q3 | Q4 | Q5 (customers rose most) |
|---|---|---|---|---|
| +2.6 points | -0.4 points | +0.4 points | +3.0 points | +5.0 points |

- Before costs the spread is +2.5 points a year (NW t = 0.71); after 0.5% a year, +2.0 points (t = 0.57, plain t = 0.49). The spread was positive in 52% of months and in 9 of 17 calendar years.
- First half: +6.4 points a year (t = 1.63). Second half: -2.5 points (t = -0.46). The sign flips, so even a larger t would not have been a Yes.
- Raw returns (no benchmark): +2.1 points a year (t = 0.57).
- Missing companies by fifth: 47% of would-be bottom-fifth holdings and 48% of top-fifth holdings have no price (middle fifths 45%-47%), so survivorship barely tilts the spread.
- Ties (information only, added after the first run): suppliers that share a customer have identical signals (in a typical month the largest block, Walmart-only suppliers, is 18% of the ranked set). The pre-specified rule puts a tie on a breakpoint in the lower fifth. Using average ranks instead gives +3.2 points a year (t = 0.91), first half +8.9 points, second half -2.6 points: same answer.

Spread by calendar year (after costs, compounded):

| 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| -11.8 | +7.1 | +10.2 | -0.6 | +22.3 | +1.6 | +6.6 | +18.4 | -17.2 | -4.4 | -8.6 | -1.3 | +0.0 | -2.9 | +19.3 | -27.7 | +14.7 |

## Secondary tests

- **Suppliers under $2B (re-sorted within small suppliers):** +1.9 points a year, NW t = 0.30; first half +6.1 points, second half -2.4 points.
- **Value-weighted:** -1.4 points a year, NW t = -0.29; first half +1.8 points, second half -4.5 points.
- **Only links where the customer is 20% or more of revenue:** +0.7 points a year, NW t = 0.11; first half +4.4 points, second half -2.9 points.
- The idea says the delay should be longest in small caps. It is not: the under-$2B spread (+1.9 points) is no larger than the $2B-and-over one (+2.3 points, information only), and neither is significant. About 26% of ranked supplier-months have no research/oplev market cap, so they sit only in the primary test.

## Caveats

- Links come from 10-K text only, found by full-text search on phrase templates. On a random sample of concentration-disclosing 10-Ks the template search found 91% of the documents in which the parser found a link; tables and unusual phrasings are missed. Customers outside the 420-entry alias list (private companies, foreign companies listed only abroad, governments) are not links by design.
- Many suppliers share a customer: Walmart is the customer in about 15% of supplier-customer-months, and in a typical month the suppliers whose only listed customer is Walmart are about 18% of the ranked set and all carry the same signal. The effective number of independent customer signals each month is far smaller than the ~165 ranked suppliers suggests.
- About 46% of supplier-months with a signal have no Yahoo price (mostly companies that later delisted). The -30% / +15% bounds do not change the answer, but the priced sample leans toward survivors.
- Customer returns come only from customers with a Yahoo history in that month; links to delisted customers (Walgreens, Sprint, Tech Data, Ingram Micro 2010-2016, Dell 2013-2016, ...) are dropped.
- A link is active from the 10-K filing date until the next 10-K. Customer relationships change during the year, and the filing reports last year's share, so some active links are stale.
- Monthly Yahoo bars were used (the test is monthly). The size-and-industry benchmark falls back to IWM/SPY for about 31% of ranked supplier-months (before July 2011, financial or utility suppliers, and suppliers with no oplev June market cap).
- Cohen and Frazzini's original evidence used Compustat customer-segment data for 1980-2004. This test covers 2010-2026, after their paper was widely known; a weak result here does not say the effect never existed.

## Files

- `PREREG.md`: the locked spec copied from research/infoedge/PREREG.md, plus the Deviations recorded before any return
- `discover.py`: concentration-phrase universe (53,460 documents) and the 1,496-document discovery sample
- `aliases.py`: the 420-entry customer alias list with ticker date windows
- `search_links.py`: template full-text search (two passes), 10-K index, document fetch and parsing
- `extract.py, textutil.py`: the customer/percentage parser
- `build_links.py`: mentions to links; supplier tickers; recall check -> data/links.csv, data/links_log.json
- `precision.py`: the 50-link hand check -> data/precision_labels.csv (round 2) and data/precision_labels_round1.csv
- `run_test.py`: the monthly test -> results.json, data/monthly_spreads.csv, data/panel_supplier_months.csv.gz
- `prices.py, edgar.py`: Yahoo and SEC clients (2 requests a second to SEC); raw downloads in cache/ (gitignored)
