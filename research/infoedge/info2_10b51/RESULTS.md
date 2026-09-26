# INFO-2. Do insiders' cancelled trading plans predict returns? Pre-registered study

*Run 2026-09-26 by `scripts/returns.py` (every number below is in `results.json`). Disclosures: 10-Q/10-K filings from August 2023 to June 2026. Returns: trading days +1 to +60 after each filing, prices to 2026-09-25. Spec and deviations: `PREREG.md`.*

## The short answer

| Test | Answer | Mean abnormal return, days +1 to +60 | t (clustered by filing month) | Sign in each half | Events |
|---|---|---|---|---|---|
| **Primary.** A CEO, CFO or director cancels a sell plan early | **No** | +1.83% (+1.63% after the 0.2% cost) | 0.84 (0.75 after cost) | + / + (+0.94%, +2.69%) | 337 |
| Secondary. The same, companies under $2B | No | +4.74% | 1.11 | + / + (+7.52%, +1.99%) | 151 |
| Secondary. Large new sell plans (top 20% by planned shares / shares outstanding), expected negative | No | +0.56% (wrong sign) | 0.45 | + / - (+1.40%, -0.28%) | 2,065 |

The bar was t >= 2.5 with the expected sign in both halves. Nothing comes close. The primary has 337 priced events, so the pre-registered power warning (fewer than 150) does not apply. But the returns are noisy (standard deviation 35% per event), so only an effect of about 5.5% or more over 60 days could have cleared the bar.

The two lines requested after INFO-5, next to the headline:

| Primary, days +1 to +60 | Mean | t |
|---|---|---|
| Against the size-and-industry benchmark (headline) | +1.83% | 0.84 |
| Against IWM (under $2B) / SPY (the rest) only | +0.37% | 0.18 (halves -2.14% / +2.81%) |
| Same companies on random dates in the same year (placebo) | +2.65% | 1.14 |
| **Event minus placebo** | **-1.09%** | **-0.37** |
| Event minus placebo, IWM/SPY | -1.63% | -0.60 |

After an early cancellation, the stocks did no better than the same stocks on ordinary days. The small positive headline is the ordinary drift of these companies, not the cancellation.

## What was tested

Since mid-2023, Item 408(a) of Regulation S-K has required companies to say in each 10-Q and 10-K which officers and directors adopted or terminated a Rule 10b5-1 trading plan. The idea: an insider who cancels a sell plan early may know good news is coming, and the market may miss a few lines in "Other Information". The event is each early termination of a plan that included sales, by a CEO, CFO or director, dated by the filing date of the 10-Q/10-K.

## Data: how the events were built

- **The APIs don't carry the tags.** The companyfacts and frames APIs have no `ecd` facts (Apple's companyfacts holds only `dei` and `us-gaap`; the ecd frames return 404). The Item 408 tags are dimensional (one context per person), and those APIs drop dimensional facts.
- **Source used instead: the SEC Financial Statement and Notes data sets** (23 bulk files, 2023q2 to 2026-08, in `cache/fsn/`). They carry every XBRL fact of every 10-Q/10-K, including `ecd:Rule10b51ArrTrmntdFlag`, `ecd:Rule10b51ArrAdoptedFlag`, `ecd:TrdArrIndName`, `ecd:TrdArrIndTitle`, the adoption, termination and expiration dates, `ecd:TrdArrDuration`, `ecd:TrdArrSecuritiesAggAvailAmt` and the text block, with the person as the dimension member.
- **Tagging was phased in.** Share of 10-Q/10-K filings with the ecd flags: 34% in 2023 H2, 65% in 2024 H1, 75% in 2024 H2, 89-92% from 2025 (`data/coverage_by_month.csv`). The first Item 408 disclosures appear in filings from July 2023 (periods from Q2 2023), as expected.
- **Untagged filings were read as text.** EDGAR full-text search found 3,097 untagged 10-Q/10-Ks mentioning "10b5-1", plus 218 missing from the data sets. A text parser read their Item 5 / Item 9B. The parser was first checked against 400 tagged filings with known answers: precision 85% (34 of 40), recall 48%. That clears the pre-set 80% rule, so text events join the sample. They add only 3 primary events, because most untagged filings are funds, trusts, SPACs and small companies with nothing to report.
- **Classification of the 1,584 disclosed terminations** (one row per person per filing; `data/terminations.csv`, rules in PREREG D2):

| Class | Count | How it is decided | In the primary? |
|---|---|---|---|
| Replacement / modification | 577 | Same person adopted a new plan in the same filing, dated on or after the termination (556), or the text says the plan was modified, amended or replaced (21). Legally a modification is a termination plus an adoption. The insider still sells. | No (robustness line) |
| Expired / completed | 68 | Text says the plan ended by its terms, all shares were sold or options fully exercised (55); termination on or after the tagged scheduled end (7); "expired" (6). | No |
| Early | 939 | Tagged scheduled end after the termination date (172); text gives a later scheduled end (250); or a plain "terminated" with no expiry or replacement wording (517). | Yes, if CEO/CFO/director |

  Other filters: 297 "termination" flags dated after the filing date were really the scheduled end of a newly adopted plan tagged with the wrong element, so they are not terminations; 29 stale re-disclosures were dropped (termination more than 100 days before the period end); 18 repeats of the same person and date in a later filing were dropped; 20 purchase-only plans were dropped.
- **Primary events:** 435 early terminations by a CEO, CFO or director (165 CEO, 101 CFO, 131 director among the priced ones; one person can hold several roles). 389 have a complete 60-day window (filed by 2026-07-01). 337 have Yahoo prices, in 311 filings across 31 filing months.

## Primary: early cancellations by CEOs, CFOs and directors

**Answer: No.** Mean abnormal return +1.83% over days +1 to +60 (t = 0.84). After the 0.2% cost: +1.63% (t = 0.75). The median is -3.07% and only 45% of events beat their benchmark, so a few big winners pull the mean up. The largest were FibroGen, ThredUp, Insmed, Sweetgreen and Caribou, each +140% to +230%.

**How much to trust it.**

- **Halves:** +0.94% (166 events, Aug 2023 to Feb 2025, t = 0.51) and +2.69% (171 events, Mar 2025 to Jun 2026, t = 0.67). Right sign in both, but far from the bar.
- **Placebo:** the same companies on 5 random dates each, in the same calendar year, earned +2.65%. Event minus placebo is -1.09% (t = -0.37). Placebo dates after the event only: event minus placebo +3.02% (t = 1.23), first half -0.52%, second half +6.55%.
- **IWM / SPY benchmark:** +0.37% (t = 0.18). The halves switch sign (-2.14%, +2.81%).
- **Missing companies:** 52 of the 389 events (13%) have no Yahoo price, because the stock no longer trades. Assuming each lost 30% gives -2.43% (t = -1.42). Assuming each gained 15% gives +3.59% (t = 1.78). Either way it is short of 2.5.
  - Most of the missing companies were later taken over. `data/missing_price_deal_check.csv` finds merger-proxy or tender-offer filings for 7 events inside the 60-day window (Deciphera, Alpine Immune, EngageSmart x2, Soleno, XOMA, Centessa; some of those deals were announced before the event), 32 later, and 17 before the event. Even +60% on each of the 7 would add only about 1 point to the mean.
- **Other cuts** (information only):

| Cut | Events | Mean | t |
|---|---|---|---|
| XBRL-tagged events only | 334 | +1.32% | 0.61 |
| Days +2 to +60 (skip the first day) | 337 | +1.73% | 0.86 |
| Winsorized at 1% / 99% | 337 | +1.37% | 0.66 |
| One event per filing | 311 | +2.28% | 0.99 |
| CEO or CFO only | 265 | +2.00% | 0.77 |
| Early terminations by any officer or director | 709 | +3.88% | 1.69 (halves +6.98% / +0.86%) |
| Replacements only (terminate and re-adopt) | 215 | +3.40% | 1.35 |
| Early plus replacements | 552 | +2.44% | 1.37 |

**For picking stocks.** A CEO, CFO or director cancelling a sell plan is not a buy signal. The effect is a couple of points at most and no larger than what the same stocks earn on random dates.

## Secondary: companies under $2B

**Answer: No.**
- Mean +4.74% (t = 1.11; 151 events; halves +7.52% / +1.99%).
- Event minus placebo +3.36% (t = 0.75). Against IWM: event minus placebo +2.67% (t = 0.61).
- Companies of $2B and over: -0.54% (t = -0.27).
- The small-company number is the largest point estimate in the study, but it rests on 151 noisy events and fades in the second half.

## Secondary: large new sell plans

**Answer: No.**
- **Events:** 14,377 tagged Rule 10b5-1 sell-plan adoptions. 11,271 have planned shares, cover-page shares outstanding and a full window; 106 ratios above 50% were dropped as tagging errors. The top 20% plan to sell at least 0.20% of shares outstanding (the median plan is 0.04%). 2,255 events, 2,065 priced.
- **Result:** mean +0.56% (t = 0.45). That is the wrong sign: the stocks did slightly better than their benchmark, not worse.
  - Against IWM/SPY: -1.77% (t = -1.32; both halves negative).
  - Missing-company bounds: -2.02% (t = -1.82) if the 190 missing lost 30%; +1.77% if they gained 15%.
- **Why the placebo line looks significant but isn't a signal.** Event minus placebo is -5.69% (t = -2.82, both halves negative). The reason is that insiders adopt sell plans after their stock has risen.
  - Placebo dates before the adoption earned +8.84% (t = 5.63).
  - Placebo dates after it earned +2.07%.
  - Event minus after-only placebo is -0.58% (t = -0.32).
  - So the gap is the run-up before the decision to sell, not a drop afterwards.

## Caveats

1. **Survivor-built prices.** Yahoo has no prices for delisted stocks. That drops 13% of primary events, and most of them were takeover targets, where a cancelled sell plan would matter most. The -30% / +15% bounds and the deal check above say this cannot turn the answer, but the measured effect is biased towards zero for exactly the cases the idea is about. The benchmark universe (5,473 priced filers) is survivor-built too. The placebo line controls for that.
2. **Classification is rule-based.** "Early" includes 517 plain "terminated" disclosures with no stated reason (some may be administrative or completed plans). Replacements are detected only within the same filing, so an insider who re-adopts next quarter still counts as early. The event-level classification is in `data/terminations.csv`, with `trm_reason`.
3. **Coverage.** The XBRL tags cover only a third of filings in 2023 H2. The text parser recovers under half of the untagged terminations (recall 48%), so the first half of the sample is thinner (166 events against 171 over a shorter span).
4. **Timing.** Event day 0 is the EDGAR filing date. For filings accepted after the close, day +1 includes the overnight reaction; the +2 to +60 line removes it and nothing changes.
5. **Market cap** (for size groups and the $2B split) = split-adjusted Yahoo close x the filing's cover-page shares, corrected for later splits. Dividend adjustment makes it slightly low.

## Files and how to rerun

Scripts (`scripts/`, in order):
1. `fetch_fsn.py`: bulk notes data sets.
2. `extract_fsn.py`: ecd and dei facts.
3. `build_events.py`: person-level records and classification.
4. `tickers.py`.
5. `fts_candidates.py`, `fetch_docs.py`, `validate_text.py`, `parse_text.py`: text path.
6. `events.py`.
7. `fetch_prices.py`: Yahoo, per ticker, throttled; run as 4 partitions.
8. `returns.py`.
9. `missing_deals.py`.
10. `report.py`.

All SEC traffic went through `scripts/sec.py`: at most 2 requests a second, cached, User-Agent "Claude Space research dspinjr@gmail.com".

Data (`data/`):
- `terminations.csv`, `adoptions.csv.gz`: events.
- `event_returns_*.csv`: per-event returns, with placebos.
- `missing_prices_terminations.csv`, `price_coverage.csv`: price gaps.
- `text_validation.csv`: text-parser check.
- `coverage_by_month.csv`: tagging coverage.

Raw downloads, about 15 GB (notes zips about 9 GB, filing documents, full-text search pages, Yahoo files), are in `cache/`, which is gitignored. Delete `cache/fsn/` and `cache/docs/` to reclaim most of it; the extracts in `cache/extract/` are enough to rerun from `build_events.py`.
